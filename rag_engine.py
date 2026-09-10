"""
DIP Diet RAG Agent - Vector Store & Retrieval Engine
=====================================================
Handles document embedding, vector DB (FAISS), and semantic retrieval.
"""

import os
import json
import pickle
import logging
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# ── Try importing ML dependencies gracefully ─────────────────────────────────
try:
    from sentence_transformers import SentenceTransformer
    # Verify it's a real module, not a stub
    ST_AVAILABLE = callable(getattr(SentenceTransformer, '__init__', None))
except (ImportError, AttributeError):
    ST_AVAILABLE = False
    logger.warning("sentence_transformers not available — using keyword fallback retrieval.")

try:
    import faiss
    # Verify the module is real (not a stub)
    FAISS_AVAILABLE = hasattr(faiss, 'IndexFlatIP')
    if not FAISS_AVAILABLE:
        logger.warning("faiss-cpu not functional — using in-memory cosine similarity.")
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("faiss-cpu not available — using in-memory cosine similarity.")


# ── Lightweight cosine similarity (numpy only) ────────────────────────────────
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.flatten()
    b = b.flatten()
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


# ── Simple keyword-based TF scorer (fallback when no ML libs) ─────────────────
def keyword_score(query: str, text: str) -> float:
    query_tokens = set(query.lower().split())
    text_tokens = text.lower().split()
    if not text_tokens:
        return 0.0
    matches = sum(1 for t in text_tokens if t in query_tokens)
    return matches / len(query_tokens) if query_tokens else 0.0


# ─────────────────────────────────────────────────────────────────────────────
class VectorStore:
    """
    Manages the DIP Diet knowledge vector store.
    Uses FAISS + SentenceTransformers when available; falls back to
    numpy cosine similarity or keyword scoring when dependencies are missing.
    """

    STORE_DIR = Path("./data/vector_store")
    INDEX_FILE = STORE_DIR / "faiss.index"
    META_FILE  = STORE_DIR / "metadata.pkl"
    HASH_FILE  = STORE_DIR / "kb_hash.txt"

    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.embedding_model_name = embedding_model
        self.model: Optional[object] = None
        self.index: Optional[object] = None          # faiss index or None
        self.embeddings: Optional[np.ndarray] = None  # fallback numpy matrix
        self.documents: List[Dict] = []
        self.dimension: int = 384  # MiniLM default

        self.STORE_DIR.mkdir(parents=True, exist_ok=True)
        self._load_model()

    # ── model loading ─────────────────────────────────────────────────────────
    def _load_model(self):
        if ST_AVAILABLE:
            try:
                logger.info(f"Loading embedding model: {self.embedding_model_name}")
                self.model = SentenceTransformer(self.embedding_model_name)
                test_emb = self.model.encode(["test"])
                self.dimension = test_emb.shape[1]
                logger.info(f"Embedding model loaded. Dimension: {self.dimension}")
            except Exception as e:
                logger.warning(f"Could not load SentenceTransformer: {e}")
                self.model = None
        else:
            self.model = None

    # ── embed ─────────────────────────────────────────────────────────────────
    def embed(self, texts: List[str]) -> np.ndarray:
        if self.model is not None:
            vecs = self.model.encode(texts, show_progress_bar=False,
                                     normalize_embeddings=True)
            return np.array(vecs, dtype="float32")
        # Keyword bag-of-words fallback (deterministic)
        vocab: Dict[str, int] = {}
        for text in texts:
            for tok in text.lower().split():
                if tok not in vocab:
                    vocab[tok] = len(vocab)
        dim = max(len(vocab), 1)
        mat = np.zeros((len(texts), dim), dtype="float32")
        for i, text in enumerate(texts):
            for tok in text.lower().split():
                if tok in vocab:
                    mat[i, vocab[tok]] += 1.0
            norm = np.linalg.norm(mat[i])
            if norm > 0:
                mat[i] /= norm
        return mat

    # ── build / rebuild index ─────────────────────────────────────────────────
    def build_index(self, documents: List[Dict], force: bool = False):
        """Build vector index from document dicts (each must have 'content')."""
        kb_hash = self._hash_kb(documents)

        if not force and self._cache_valid(kb_hash):
            logger.info("Loading cached vector store…")
            self._load_cached()
            return

        logger.info(f"Building vector index for {len(documents)} documents…")
        self.documents = documents
        texts = [d["content"] for d in documents]
        vecs = self.embed(texts)

        if FAISS_AVAILABLE:
            self.index = faiss.IndexFlatIP(vecs.shape[1])  # inner-product (cos sim after norm)
            self.index.add(vecs)
        else:
            self.embeddings = vecs

        self._save_cache(kb_hash)
        logger.info("Vector index built and cached.")

    # ── search ────────────────────────────────────────────────────────────────
    def search(self, query: str, top_k: int = 5,
               threshold: float = 0.3) -> List[Dict]:
        """Return top_k most relevant documents with similarity scores."""
        if not self.documents:
            return []

        if self.model is not None or FAISS_AVAILABLE:
            q_vec = self.embed([query])

            if FAISS_AVAILABLE and self.index is not None:
                k = min(top_k * 2, len(self.documents))
                scores, indices = self.index.search(q_vec, k)
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx < 0 or score < threshold:
                        continue
                    doc = dict(self.documents[idx])
                    doc["similarity_score"] = float(score)
                    results.append(doc)
                return results[:top_k]

            elif self.embeddings is not None:
                sims = [cosine_similarity(q_vec[0], self.embeddings[i])
                        for i in range(len(self.documents))]
                ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
                results = []
                for idx, score in ranked[:top_k * 2]:
                    if score < threshold:
                        continue
                    doc = dict(self.documents[idx])
                    doc["similarity_score"] = float(score)
                    results.append(doc)
                return results[:top_k]

        # Pure keyword fallback
        scored = []
        for doc in self.documents:
            score = keyword_score(query, doc.get("content", ""))
            if score >= 0.1:
                scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, doc in scored[:top_k]:
            d = dict(doc)
            d["similarity_score"] = score
            results.append(d)
        return results

    # ── persistence ───────────────────────────────────────────────────────────
    def _hash_kb(self, documents: List[Dict]) -> str:
        raw = json.dumps([d.get("id", "") + d.get("content", "")
                          for d in documents], sort_keys=True)
        return hashlib.md5(raw.encode()).hexdigest()

    def _cache_valid(self, kb_hash: str) -> bool:
        if not (self.META_FILE.exists() and self.HASH_FILE.exists()):
            return False
        if FAISS_AVAILABLE and not self.INDEX_FILE.exists():
            return False
        return self.HASH_FILE.read_text().strip() == kb_hash

    def _save_cache(self, kb_hash: str):
        with open(self.META_FILE, "wb") as f:
            pickle.dump(self.documents, f)
        if FAISS_AVAILABLE and self.index is not None:
            faiss.write_index(self.index, str(self.INDEX_FILE))
        elif self.embeddings is not None:
            np.save(str(self.STORE_DIR / "embeddings.npy"), self.embeddings)
        self.HASH_FILE.write_text(kb_hash)

    def _load_cached(self):
        with open(self.META_FILE, "rb") as f:
            self.documents = pickle.load(f)
        if FAISS_AVAILABLE and self.INDEX_FILE.exists():
            self.index = faiss.read_index(str(self.INDEX_FILE))
        else:
            emb_path = self.STORE_DIR / "embeddings.npy"
            if emb_path.exists():
                self.embeddings = np.load(str(emb_path))
        logger.info(f"Loaded {len(self.documents)} documents from cache.")

    # ── document upload ───────────────────────────────────────────────────────
    def add_documents(self, new_docs: List[Dict]):
        """Add new documents to existing store and rebuild."""
        self.documents.extend(new_docs)
        self.build_index(self.documents, force=True)

    def get_stats(self) -> Dict:
        return {
            "total_documents": len(self.documents),
            "embedding_backend": "SentenceTransformers" if self.model else "Keyword",
            "index_backend": "FAISS" if (FAISS_AVAILABLE and self.index) else "NumPy/Keyword",
            "dimension": self.dimension,
        }


# ─────────────────────────────────────────────────────────────────────────────
class DocumentProcessor:
    """Parse uploaded files into chunked document dicts for the vector store."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_text(self, text: str, source: str, section: str = "Uploaded") -> List[Dict]:
        chunks = self._chunk_text(text)
        docs = []
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"{source}_{i}",
                "source": source,
                "section": section,
                "content": chunk,
            })
        return docs

    def process_pdf(self, filepath: str) -> List[Dict]:
        try:
            import PyPDF2
            docs = []
            source = Path(filepath).stem
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    if text.strip():
                        chunks = self._chunk_text(text)
                        for i, chunk in enumerate(chunks):
                            docs.append({
                                "id": f"{source}_p{page_num}_{i}",
                                "source": source,
                                "section": f"Page {page_num + 1}",
                                "content": chunk,
                            })
            return docs
        except Exception as e:
            logger.error(f"PDF processing error: {e}")
            return []

    def process_docx(self, filepath: str) -> List[Dict]:
        try:
            from docx import Document
            source = Path(filepath).stem
            doc = Document(filepath)
            full_text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            return self.process_text(full_text, source)
        except Exception as e:
            logger.error(f"DOCX processing error: {e}")
            return []

    def process_txt(self, filepath: str) -> List[Dict]:
        try:
            source = Path(filepath).stem
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            return self.process_text(text, source)
        except Exception as e:
            logger.error(f"TXT processing error: {e}")
            return []

    def _chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunk = " ".join(words[start:end])
            if chunk.strip():
                chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks


# ─────────────────────────────────────────────────────────────────────────────
# Singleton accessor
# ─────────────────────────────────────────────────────────────────────────────
_vector_store_instance: Optional[VectorStore] = None

def get_vector_store() -> VectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        from agent_config import RAG_CONFIG
        from knowledge_base import DIP_KNOWLEDGE_BASE
        _vector_store_instance = VectorStore(
            embedding_model=RAG_CONFIG["embedding_model"]
        )
        _vector_store_instance.build_index(DIP_KNOWLEDGE_BASE)
    return _vector_store_instance
