"""
DIP Diet RAG Agent - IBM WatsonX AI & Langflow Integration
===========================================================
Handles IBM WatsonX AI model calls, IBM Langflow workflow execution,
and the full RAG pipeline (retrieve → augment → generate).
"""

import os
import json
import logging
import requests
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

DISCLAIMER = (
    "\n\n---\n"
    "⚠️ **Disclaimer:** This information is for general educational purposes only "
    "and is not a substitute for professional medical advice, diagnosis, or treatment. "
    "Please consult your doctor or a registered dietitian before making significant "
    "dietary or lifestyle changes, especially if you have any medical condition."
)


# ─────────────────────────────────────────────────────────────────────────────
# IBM WatsonX AI Client
# ─────────────────────────────────────────────────────────────────────────────
class WatsonXClient:
    """
    Calls IBM WatsonX AI (ibm-watsonx-ai) for text generation.
    Falls back to a rule-based response if credentials are not configured.
    """

    def __init__(self):
        self.api_key      = os.getenv("IBM_WATSONX_API_KEY", "")
        self.project_id   = os.getenv("IBM_WATSONX_PROJECT_ID", "")
        self.url          = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self._model       = None
        self._available   = False
        self._iam_token   = None
        self._init_client()

    def _init_client(self):
        if not self.api_key or not self.project_id:
            logger.warning("IBM WatsonX credentials not configured — using fallback mode.")
            return
        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as Params
            from agent_config import MODEL_CONFIG

            creds = Credentials(api_key=self.api_key, url=self.url)
            params = {
                Params.TEMPERATURE:         MODEL_CONFIG["temperature"],
                Params.MAX_NEW_TOKENS:      MODEL_CONFIG["max_new_tokens"],
                Params.TOP_P:               MODEL_CONFIG["top_p"],
                Params.REPETITION_PENALTY:  MODEL_CONFIG["repetition_penalty"],
            }
            self._model = ModelInference(
                model_id=MODEL_CONFIG["model_id"],
                credentials=creds,
                project_id=self.project_id,
                params=params,
            )
            self._available = True
            logger.info(f"WatsonX client initialised with model: {MODEL_CONFIG['model_id']}")
        except ImportError:
            logger.warning("ibm-watsonx-ai package not installed — using fallback.")
        except Exception as e:
            logger.warning(f"WatsonX init error: {e} — using fallback.")

    def generate(self, prompt: str) -> Tuple[str, str]:
        """Returns (response_text, model_used)."""
        if self._available and self._model:
            try:
                result = self._model.generate_text(prompt=prompt)
                return result, "IBM Granite (WatsonX)"
            except Exception as e:
                logger.error(f"WatsonX generation error: {e}")
        return None, "fallback"

    @property
    def is_available(self) -> bool:
        return self._available


# ─────────────────────────────────────────────────────────────────────────────
# IBM Langflow / Orchestrate Client
# ─────────────────────────────────────────────────────────────────────────────
class LangflowClient:
    """
    Calls IBM Langflow or IBM Orchestrate API for advanced workflow execution.
    Optional — used when IBM_LANGFLOW_API_URL is configured.
    """

    def __init__(self):
        self.api_url  = os.getenv("IBM_LANGFLOW_API_URL", "")
        self.flow_id  = os.getenv("IBM_LANGFLOW_FLOW_ID", "")
        self.api_key  = os.getenv("IBM_LANGFLOW_API_KEY", "")
        self._available = bool(self.api_url and self.flow_id)
        if self._available:
            logger.info(f"Langflow client configured: {self.api_url}")

    def run_flow(self, query: str, context: str,
                 history: List[Dict]) -> Optional[str]:
        """Execute an IBM Langflow workflow and return the response text."""
        if not self._available:
            return None
        try:
            payload = {
                "input_value": query,
                "output_type": "chat",
                "input_type": "chat",
                "tweaks": {
                    "context": context,
                    "chat_history": history[-6:],  # last 6 turns
                }
            }
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            url = f"{self.api_url}/{self.flow_id}"
            resp = requests.post(url, json=payload, headers=headers, timeout=45)
            resp.raise_for_status()
            data = resp.json()
            # Langflow response structure
            output = (
                data.get("outputs", [{}])[0]
                    .get("outputs", [{}])[0]
                    .get("results", {})
                    .get("message", {})
                    .get("text", "")
            )
            return output if output else None
        except Exception as e:
            logger.error(f"Langflow API error: {e}")
            return None

    @property
    def is_available(self) -> bool:
        return self._available


# ─────────────────────────────────────────────────────────────────────────────
# Prompt Builder
# ─────────────────────────────────────────────────────────────────────────────
def build_rag_prompt(query: str,
                     retrieved_docs: List[Dict],
                     conversation_history: List[Dict],
                     user_profile: Dict,
                     agent_instructions: str) -> str:
    """Construct the full RAG prompt for the LLM."""

    # Format retrieved context
    context_blocks = []
    for doc in retrieved_docs:
        source = doc.get("source", "Unknown")
        section = doc.get("section", "")
        score = doc.get("similarity_score", 0)
        content = doc.get("content", "")
        context_blocks.append(
            f"[Source: {source} — {section} | Relevance: {score:.2f}]\n{content}"
        )
    context_text = "\n\n".join(context_blocks) if context_blocks else "No specific context retrieved."

    # Format conversation history
    history_lines = []
    for turn in conversation_history[-8:]:
        role = turn.get("role", "user")
        msg  = turn.get("content", "")
        history_lines.append(f"{'User' if role == 'user' else 'Assistant'}: {msg}")
    history_text = "\n".join(history_lines) if history_lines else "None"

    # Format user profile
    profile_text = _format_profile(user_profile)

    prompt = f"""<|system|>
{agent_instructions}

## USER PROFILE
{profile_text}

## RETRIEVED KNOWLEDGE CONTEXT
{context_text}

## CONVERSATION HISTORY
{history_text}
<|end_of_text|>
<|user|>
{query}
<|end_of_text|>
<|assistant|>
"""
    return prompt


def _format_profile(profile: Dict) -> str:
    if not profile:
        return "No profile information available."
    lines = []
    if profile.get("name"):
        lines.append(f"Name: {profile['name']}")
    if profile.get("age"):
        lines.append(f"Age: {profile['age']}")
    if profile.get("health_goals"):
        lines.append(f"Health Goals: {profile['health_goals']}")
    if profile.get("dietary_preference"):
        lines.append(f"Dietary Preference: {profile['dietary_preference']}")
    if profile.get("health_conditions"):
        lines.append(f"Health Conditions: {profile['health_conditions']}")
    if profile.get("activity_level"):
        lines.append(f"Activity Level: {profile['activity_level']}")
    if profile.get("region"):
        lines.append(f"Region/Cuisine: {profile['region']}")
    return "\n".join(lines) if lines else "Profile not fully set up."


# ─────────────────────────────────────────────────────────────────────────────
# Fallback Response Engine (no AI credentials needed)
# ─────────────────────────────────────────────────────────────────────────────
def fallback_response(query: str, retrieved_docs: List[Dict],
                      user_profile: Dict) -> str:
    """
    Generates a structured response from retrieved docs when no LLM is available.
    """
    q_lower = query.lower()

    if retrieved_docs:
        # Synthesise response from top retrieved docs
        lines = ["Based on the DIP Diet knowledge base, here is what I found:\n"]
        for i, doc in enumerate(retrieved_docs[:3], 1):
            source  = doc.get("source", "DIP Diet Guide")
            section = doc.get("section", "")
            content = doc.get("content", "")
            # Take first 250 words of content
            words = content.split()[:120]
            excerpt = " ".join(words)
            if len(content.split()) > 120:
                excerpt += "…"
            lines.append(f"**{i}. {section}** *(Source: {source})*\n{excerpt}\n")

        response = "\n".join(lines)

        # Add source citations
        sources = list({doc.get("source", "") for doc in retrieved_docs[:3] if doc.get("source")})
        if sources:
            response += f"\n**Sources:** {', '.join(sources)}"
    else:
        # Generic DIP Diet response
        response = _generic_dip_response(q_lower)

    return response + DISCLAIMER


def _generic_dip_response(query: str) -> str:
    """Rule-based generic responses for common DIP Diet questions."""
    if any(k in query for k in ["what is dip", "dip diet", "explain dip"]):
        return (
            "**The DIP Diet** (Disciplined Intelligent Personalized Diet) is a whole-food, "
            "plant-based eating protocol that emphasizes:\n"
            "- **Two meals a day** (fruit breakfast + balanced lunch/dinner)\n"
            "- **No refined foods** (no sugar, maida, or refined oils)\n"
            "- **50% raw foods** on the plate\n"
            "- **Morning sunlight** and daily physical activity\n"
            "- **Mindful eating** practices\n\n"
            "It has been shown to support weight management, blood sugar control, "
            "and overall metabolic health."
        )
    if any(k in query for k in ["meal plan", "daily plan", "what to eat"]):
        return (
            "**Sample DIP Diet Daily Plan:**\n\n"
            "🌅 **Morning (6-7 AM):** Warm water + lemon, 20-min walk, sunlight\n\n"
            "🍎 **Meal 1 (8-10 AM — Fruit Meal):**\n"
            "- 2 bananas + 1 papaya + 1 guava + pomegranate\n"
            "- 10 soaked almonds + 5 walnuts\n\n"
            "🥗 **Meal 2 (1-2 PM — Main Meal):**\n"
            "- Large salad (cucumber, tomato, carrot, sprouts)\n"
            "- 2 whole wheat rotis\n"
            "- 1 bowl dal (moong/masoor)\n"
            "- 1 cooked vegetable dish\n\n"
            "💧 **Hydration:** 8-10 glasses of water between meals\n"
            "🚶 **Evening:** Light walk, herbal tea"
        )
    if any(k in query for k in ["substitute", "replace", "instead of", "alternative"]):
        return (
            "**DIP Diet Food Substitutions:**\n\n"
            "| Instead of | Use |\n"
            "|---|---|\n"
            "| Refined sugar | Dates, jaggery, ripe banana |\n"
            "| Maida (white flour) | Whole wheat atta, ragi, besan |\n"
            "| White rice | Brown rice, millets (ragi, jowar, bajra) |\n"
            "| Refined oil | Water sautéing, minimal cold-pressed oil |\n"
            "| Dairy milk | Soy milk, oat milk, peanut milk |\n"
            "| Commercial snacks | Roasted chana, makhana, fresh fruit |\n"
            "| Ghee/butter | Minimal avocado or nut butters |"
        )
    if any(k in query for k in ["diabetes", "blood sugar", "sugar"]):
        return (
            "**DIP Diet for Diabetes Management:**\n\n"
            "Key recommendations:\n"
            "- Focus on **low-glycemic whole foods**: bitter gourd, fenugreek, amla\n"
            "- Choose **whole grains**: ragi, oats, barley over white rice/bread\n"
            "- **Soak 1 tbsp fenugreek seeds** overnight and drink water in the morning\n"
            "- Walk **15 minutes after meals** to reduce blood sugar spikes\n"
            "- Include **cinnamon, turmeric, and ginger** daily\n"
            "- Avoid fruit juices — eat whole fruits with fiber\n\n"
            "⚠️ Monitor blood sugar regularly and consult your physician."
        )
    if any(k in query for k in ["protein", "enough protein"]):
        return (
            "**Plant Protein Sources in DIP Diet:**\n\n"
            "- **Dal (lentils/pulses):** 9g protein per cup cooked\n"
            "- **Chickpeas/Rajma:** 9g protein per cup cooked\n"
            "- **Tofu:** 8g per 100g\n"
            "- **Soya:** 11g per 100g\n"
            "- **Sprouts (moong):** 3g per cup\n"
            "- **Whole grains:** 3-5g per serving\n\n"
            "A 70kg person needs ~56g/day (sedentary). A balanced DIP Diet with "
            "legumes at each meal easily meets this requirement."
        )
    return (
        "Thank you for your DIP Diet question! I'm here to help you with:\n\n"
        "🥗 **Meal planning** — daily and weekly DIP-compliant meal suggestions\n"
        "🔄 **Food substitutions** — healthier swaps for common Indian foods\n"
        "💊 **Nutrition guidance** — protein, vitamins, minerals on plant-based diet\n"
        "🏥 **Health conditions** — DIP Diet for diabetes, PCOS, heart health\n"
        "🌿 **Lifestyle tips** — morning routine, sleep, mindful eating\n\n"
        "Please ask a specific question and I'll provide detailed guidance based on "
        "DIP Diet principles!"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main RAG Agent
# ─────────────────────────────────────────────────────────────────────────────
class DIPDietRAGAgent:
    """
    Orchestrates the full RAG pipeline:
      1. Retrieve relevant documents from the vector store
      2. Build augmented prompt
      3. Generate response via IBM WatsonX or Langflow
      4. Fall back to structured response if no LLM available
    """

    def __init__(self):
        from rag_engine import get_vector_store
        from agent_config import AGENT_INSTRUCTIONS, RAG_CONFIG
        self.vector_store       = get_vector_store()
        self.agent_instructions = AGENT_INSTRUCTIONS
        self.rag_config         = RAG_CONFIG
        self.watsonx            = WatsonXClient()
        self.langflow           = LangflowClient()
        logger.info("DIP Diet RAG Agent initialised.")
        logger.info(f"  WatsonX available: {self.watsonx.is_available}")
        logger.info(f"  Langflow available: {self.langflow.is_available}")

    def chat(self, query: str,
             conversation_history: List[Dict],
             user_profile: Dict) -> Dict:
        """
        Full RAG pipeline. Returns a dict with:
          - response (str)
          - sources (list)
          - model_used (str)
          - retrieved_count (int)
        """
        # 1. Retrieve
        retrieved = self.vector_store.search(
            query,
            top_k=self.rag_config["top_k_retrieval"],
            threshold=self.rag_config["similarity_threshold"],
        )

        sources = [
            {"source": d.get("source", ""), "section": d.get("section", ""),
             "score": round(d.get("similarity_score", 0), 3)}
            for d in retrieved
        ]

        # 2. Try IBM Langflow first (advanced workflow)
        if self.langflow.is_available:
            context = "\n\n".join(d.get("content", "") for d in retrieved)
            lf_response = self.langflow.run_flow(query, context, conversation_history)
            if lf_response:
                return {
                    "response": lf_response + DISCLAIMER,
                    "sources": sources,
                    "model_used": "IBM Langflow / Orchestrate",
                    "retrieved_count": len(retrieved),
                }

        # 3. Try IBM WatsonX
        if self.watsonx.is_available:
            prompt = build_rag_prompt(
                query, retrieved, conversation_history,
                user_profile, self.agent_instructions
            )
            wx_response, model_name = self.watsonx.generate(prompt)
            if wx_response:
                return {
                    "response": wx_response + DISCLAIMER,
                    "sources": sources,
                    "model_used": model_name,
                    "retrieved_count": len(retrieved),
                }

        # 4. Fallback structured response
        fb_response = fallback_response(query, retrieved, user_profile)
        return {
            "response": fb_response,
            "sources": sources,
            "model_used": "DIP Diet Knowledge Base (Structured Response)",
            "retrieved_count": len(retrieved),
        }

    def reload_instructions(self, new_instructions: str):
        """Hot-reload agent instructions without restarting the app."""
        self.agent_instructions = new_instructions
        logger.info("Agent instructions reloaded.")

    def get_store_stats(self) -> Dict:
        return self.vector_store.get_stats()


# ─────────────────────────────────────────────────────────────────────────────
# Singleton accessor
# ─────────────────────────────────────────────────────────────────────────────
_agent_instance: Optional[DIPDietRAGAgent] = None

def get_agent() -> DIPDietRAGAgent:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = DIPDietRAGAgent()
    return _agent_instance
