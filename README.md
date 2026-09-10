# DIP Diet RAG Agent

An AI-powered **DIP Diet Nutrition Assistant** built with Python Flask, IBM WatsonX AI, IBM Langflow, and Retrieval-Augmented Generation (RAG) using a FAISS vector database.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and fill in your IBM WatsonX credentials
```

### 3. Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

---

## 🔑 IBM WatsonX AI Configuration

Edit `.env` with your credentials:

```env
IBM_WATSONX_API_KEY=your_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Get credentials at: [IBM Cloud WatsonX](https://cloud.ibm.com/watsonx)

> **Note:** Without credentials, the app runs in **Structured Fallback Mode** — it still retrieves from the knowledge base and provides structured answers, just without LLM generation.

---

## 🔧 IBM Langflow / Orchestrate (Optional)

For advanced workflow orchestration:

```env
IBM_LANGFLOW_API_URL=https://your-langflow-instance.ibm.com/api/v1/run
IBM_LANGFLOW_FLOW_ID=your_flow_id
IBM_LANGFLOW_API_KEY=your_api_key
```

---

## 📁 Project Structure

```
├── app.py                   # Flask application & all routes
├── ibm_agent.py             # IBM WatsonX AI + Langflow integration + RAG pipeline
├── rag_engine.py            # FAISS vector store + document processor
├── knowledge_base.py        # Curated DIP Diet knowledge (28 documents)
├── agent_config.py          # AGENT_INSTRUCTIONS + model/RAG configuration
├── wsgi.py                  # WSGI entry point (gunicorn)
├── requirements.txt
├── .env.example
├── templates/
│   ├── base.html            # Base template with navbar + footer
│   ├── index.html           # Landing page
│   ├── chat.html            # AI Chatbot interface
│   ├── dashboard.html       # Personalized dashboard
│   ├── meal_planner.html    # Daily/weekly meal plan generator
│   ├── nutrition.html       # Nutrition insights lookup
│   ├── substitutions.html   # Food substitution finder
│   ├── lifestyle.html       # Lifestyle guide & tips
│   ├── profile.html         # User profile form
│   ├── admin_instructions.html  # AGENT_INSTRUCTIONS editor
│   ├── about.html
│   └── error.html
├── static/
│   ├── css/style.css        # Full custom stylesheet
│   ├── js/app.js            # Global JS
│   ├── js/chat.js           # Chat interface JS
│   └── js/meal_planner.js   # Meal planner JS
└── data/
    ├── vector_store/        # FAISS index + metadata (auto-generated)
    ├── uploads/             # Uploaded knowledge files
    └── knowledge_base/      # Additional knowledge documents
```

---

## 🥗 Features

| Feature | Description |
|---------|-------------|
| **AI Chatbot** | RAG-powered Q&A using IBM WatsonX AI + FAISS vector search |
| **Meal Planner** | Daily/weekly DIP Diet plans for 5 health conditions |
| **Food Substitutions** | AI-powered healthy swaps for any ingredient |
| **Nutrition Insights** | Detailed nutritional profiles of DIP Diet foods |
| **Lifestyle Guide** | Morning routines, sleep, yoga, mindful eating tips |
| **User Profiles** | Personalization by health goals, conditions, region |
| **Agent Instructions** | Editable AGENT_INSTRUCTIONS for custom behavior |
| **Knowledge Upload** | Upload PDF/DOCX/TXT to expand the knowledge base |
| **Source Citations** | All responses cite knowledge base sources |
| **Medical Disclaimer** | Prominent disclaimers on all health-related content |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Flask Route (app.py)
    │
    ▼
DIPDietRAGAgent (ibm_agent.py)
    │
    ├─► VectorStore.search() (rag_engine.py + FAISS)
    │         └─► Returns top-K relevant DIP Diet chunks
    │
    ├─► Build RAG Prompt (retrieved context + history + profile)
    │
    ├─► IBM Langflow API (if configured)
    │   └─► Returns workflow-generated response
    │
    ├─► IBM WatsonX AI - Granite (if credentials set)
    │   └─► Returns LLM-generated response
    │
    └─► Structured Fallback (always available)
          └─► Returns knowledge-retrieved structured answer
```

---

## ✏️ Customizing the Agent

1. Navigate to **Agent Settings** (⚙️ icon in navbar)
2. Edit the `AGENT_INSTRUCTIONS` text directly in the browser
3. Click **Save & Reload Agent** — changes take effect immediately
4. The instructions control: tone, DIP Diet knowledge, safety rules, food preferences, response format

---

## 📤 Adding Knowledge

Upload DIP Diet books, blogs, diet plans, or nutrition guides:

1. Click **Upload Knowledge** in the chat interface
2. Select PDF, DOCX, or TXT files (max 50MB)
3. The system automatically chunks, embeds, and indexes the content
4. New knowledge is immediately available for RAG retrieval

---

## 🛡️ Medical Disclaimer

This application provides **general nutrition and wellness information only** and is **not a substitute for professional medical advice**. Always consult a qualified physician or registered dietitian before making dietary changes.

---

## 🚀 Production Deployment

```bash
gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

---

## 📄 License

Educational & wellness purposes. Not for commercial use without permission.
