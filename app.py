"""
DIP Diet RAG Agent - Flask Application
=======================================
Main Flask app with all routes for chatbot, dashboard,
meal planning, nutrition insights, user profiles, and admin.
"""

import os
import json
import logging
import uuid
from datetime import datetime, date
from pathlib import Path
from functools import wraps

from flask import (
    Flask, render_template, request, jsonify,
    session, redirect, url_for, flash, send_from_directory
)
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# ── Load environment ──────────────────────────────────────────────────────────
load_dotenv()

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ── Flask app factory ─────────────────────────────────────────────────────────
def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dip-diet-rag-secret-2024")
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_SIZE_MB", 50)) * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = "./data/uploads"
    CORS(app)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path("./data/vector_store").mkdir(parents=True, exist_ok=True)

    # ── Lazy-load agent on first request ─────────────────────────────────────
    _agent_cache = {}

    def get_agent():
        if "agent" not in _agent_cache:
            from ibm_agent import get_agent as _get
            _agent_cache["agent"] = _get()
        return _agent_cache["agent"]

    # ── Session helpers ───────────────────────────────────────────────────────
    def ensure_session():
        if "user_id" not in session:
            session["user_id"] = str(uuid.uuid4())
        if "chat_history" not in session:
            session["chat_history"] = []
        if "user_profile" not in session:
            session["user_profile"] = {}
        if "meal_plans" not in session:
            session["meal_plans"] = {}

    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN ROUTES
    # ═══════════════════════════════════════════════════════════════════════════

    @app.route("/")
    def index():
        ensure_session()
        return render_template("index.html",
                               profile=session.get("user_profile", {}),
                               today=date.today().strftime("%A, %d %B %Y"))

    @app.route("/dashboard")
    def dashboard():
        ensure_session()
        profile = session.get("user_profile", {})
        stats   = _build_dashboard_stats(session)
        return render_template("dashboard.html",
                               profile=profile,
                               stats=stats,
                               today=date.today().strftime("%A, %d %B %Y"))

    @app.route("/chat")
    def chat_page():
        ensure_session()
        return render_template("chat.html",
                               profile=session.get("user_profile", {}),
                               chat_history=session.get("chat_history", []))

    @app.route("/meal-planner")
    def meal_planner():
        ensure_session()
        return render_template("meal_planner.html",
                               profile=session.get("user_profile", {}),
                               meal_plans=session.get("meal_plans", {}))

    @app.route("/nutrition")
    def nutrition():
        ensure_session()
        return render_template("nutrition.html",
                               profile=session.get("user_profile", {}))

    @app.route("/lifestyle")
    def lifestyle():
        ensure_session()
        return render_template("lifestyle.html",
                               profile=session.get("user_profile", {}))

    @app.route("/substitutions")
    def substitutions():
        ensure_session()
        return render_template("substitutions.html",
                               profile=session.get("user_profile", {}))

    @app.route("/profile", methods=["GET", "POST"])
    def profile():
        ensure_session()
        if request.method == "POST":
            session["user_profile"] = {
                "name":               request.form.get("name", ""),
                "age":                request.form.get("age", ""),
                "gender":             request.form.get("gender", ""),
                "weight_kg":          request.form.get("weight_kg", ""),
                "height_cm":          request.form.get("height_cm", ""),
                "health_goals":       request.form.get("health_goals", ""),
                "health_conditions":  request.form.get("health_conditions", ""),
                "dietary_preference": request.form.get("dietary_preference", ""),
                "activity_level":     request.form.get("activity_level", ""),
                "region":             request.form.get("region", ""),
                "allergies":          request.form.get("allergies", ""),
                "updated_at":         datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            session.modified = True
            flash("Profile updated successfully! 🎉", "success")
            return redirect(url_for("dashboard"))
        return render_template("profile.html",
                               profile=session.get("user_profile", {}))

    @app.route("/admin/instructions", methods=["GET", "POST"])
    def admin_instructions():
        ensure_session()
        from agent_config import AGENT_INSTRUCTIONS
        current_instructions = AGENT_INSTRUCTIONS

        if request.method == "POST":
            new_instructions = request.form.get("instructions", "").strip()
            if new_instructions:
                try:
                    agent = get_agent()
                    agent.reload_instructions(new_instructions)
                    # Persist to agent_config.py (runtime update)
                    _save_instructions(new_instructions)
                    flash("Agent instructions updated and reloaded! ✅", "success")
                except Exception as e:
                    flash(f"Error updating instructions: {e}", "danger")
            return redirect(url_for("admin_instructions"))

        return render_template("admin_instructions.html",
                               instructions=current_instructions)

    @app.route("/about")
    def about():
        return render_template("about.html")

    # ═══════════════════════════════════════════════════════════════════════════
    # API ROUTES
    # ═══════════════════════════════════════════════════════════════════════════

    @app.route("/api/chat", methods=["POST"])
    def api_chat():
        ensure_session()
        data  = request.get_json(force=True) or {}
        query = data.get("message", "").strip()

        if not query:
            return jsonify({"error": "Empty message"}), 400

        if len(query) > 2000:
            return jsonify({"error": "Message too long (max 2000 chars)"}), 400

        try:
            agent = get_agent()
            result = agent.chat(
                query=query,
                conversation_history=session.get("chat_history", []),
                user_profile=session.get("user_profile", {}),
            )

            # Update conversation history
            history = session.get("chat_history", [])
            history.append({"role": "user", "content": query,
                             "timestamp": datetime.now().strftime("%H:%M")})
            history.append({"role": "assistant",
                             "content": result["response"],
                             "sources": result.get("sources", []),
                             "model_used": result.get("model_used", ""),
                             "timestamp": datetime.now().strftime("%H:%M")})
            # Keep last 40 messages
            session["chat_history"] = history[-40:]
            session.modified = True

            return jsonify({
                "response":        result["response"],
                "sources":         result.get("sources", []),
                "model_used":      result.get("model_used", ""),
                "retrieved_count": result.get("retrieved_count", 0),
                "timestamp":       datetime.now().strftime("%H:%M"),
            })
        except Exception as e:
            logger.exception("Chat API error")
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    @app.route("/api/chat/clear", methods=["POST"])
    def api_clear_chat():
        ensure_session()
        session["chat_history"] = []
        session.modified = True
        return jsonify({"status": "cleared"})

    @app.route("/api/meal-plan/generate", methods=["POST"])
    def api_generate_meal_plan():
        ensure_session()
        data       = request.get_json(force=True) or {}
        plan_type  = data.get("plan_type", "daily")   # daily | weekly
        condition  = data.get("condition", "general") # general | diabetes | weight_loss | heart | pcos
        profile    = session.get("user_profile", {})

        query = _build_meal_plan_query(plan_type, condition, profile)

        try:
            agent = get_agent()
            result = agent.chat(query=query,
                                conversation_history=[],
                                user_profile=profile)
            plan = {
                "type":       plan_type,
                "condition":  condition,
                "content":    result["response"],
                "sources":    result.get("sources", []),
                "model_used": result.get("model_used", ""),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            # Cache in session
            key = f"{plan_type}_{condition}"
            session["meal_plans"][key] = plan
            session.modified = True

            return jsonify(plan)
        except Exception as e:
            logger.exception("Meal plan API error")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/substitution", methods=["POST"])
    def api_substitution():
        ensure_session()
        data = request.get_json(force=True) or {}
        food = data.get("food", "").strip()
        if not food:
            return jsonify({"error": "Food item required"}), 400

        query = (f"What are the DIP Diet-approved substitutions for '{food}'? "
                 f"Provide specific alternatives with nutritional benefits.")
        try:
            agent = get_agent()
            result = agent.chat(query=query,
                                conversation_history=[],
                                user_profile=session.get("user_profile", {}))
            return jsonify({"food": food, "substitutions": result["response"],
                            "sources": result.get("sources", [])})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/nutrition-insight", methods=["POST"])
    def api_nutrition_insight():
        ensure_session()
        data      = request.get_json(force=True) or {}
        food_item = data.get("food", "").strip()
        if not food_item:
            return jsonify({"error": "Food item required"}), 400

        query = (f"Provide detailed nutritional information and health benefits "
                 f"of '{food_item}' in the context of the DIP Diet. "
                 f"Include key nutrients, recommended quantity, and any cautions.")
        try:
            agent  = get_agent()
            result = agent.chat(query=query, conversation_history=[],
                                user_profile=session.get("user_profile", {}))
            return jsonify({"food": food_item, "insight": result["response"],
                            "sources": result.get("sources", [])})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/lifestyle-tip", methods=["GET"])
    def api_lifestyle_tip():
        ensure_session()
        category = request.args.get("category", "general")
        query    = _lifestyle_query(category)
        try:
            agent  = get_agent()
            result = agent.chat(query=query, conversation_history=[],
                                user_profile=session.get("user_profile", {}))
            return jsonify({"category": category, "tip": result["response"],
                            "sources": result.get("sources", [])})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/upload-knowledge", methods=["POST"])
    def api_upload_knowledge():
        ensure_session()
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        ALLOWED = {".pdf", ".txt", ".docx"}
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED:
            return jsonify({"error": f"File type not allowed. Use: {', '.join(ALLOWED)}"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        try:
            from rag_engine import DocumentProcessor
            processor = DocumentProcessor()
            if ext == ".pdf":
                docs = processor.process_pdf(filepath)
            elif ext == ".docx":
                docs = processor.process_docx(filepath)
            else:
                docs = processor.process_txt(filepath)

            if not docs:
                return jsonify({"error": "Could not extract text from file"}), 400

            agent = get_agent()
            agent.vector_store.add_documents(docs)

            return jsonify({
                "status":    "success",
                "filename":  filename,
                "chunks":    len(docs),
                "message":   f"Successfully added {len(docs)} knowledge chunks from '{filename}'",
            })
        except Exception as e:
            logger.exception("Upload error")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/agent-stats", methods=["GET"])
    def api_agent_stats():
        try:
            agent = get_agent()
            stats = agent.get_store_stats()
            stats["watsonx_available"]  = agent.watsonx.is_available
            stats["langflow_available"] = agent.langflow.is_available
            return jsonify(stats)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # ─── Error handlers ───────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404,
                               message="Page not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", code=500,
                               message="Internal server error"), 500

    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"error": "File too large. Max size is 50MB."}), 413

    return app


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────
def _build_dashboard_stats(sess) -> dict:
    history  = sess.get("chat_history", [])
    profile  = sess.get("user_profile", {})
    plans    = sess.get("meal_plans", {})
    q_count  = sum(1 for m in history if m.get("role") == "user")
    return {
        "questions_asked":   q_count,
        "meal_plans_created": len(plans),
        "profile_complete":   _profile_completeness(profile),
        "sessions_today":     1,
    }


def _profile_completeness(profile: dict) -> int:
    fields = ["name", "age", "health_goals", "dietary_preference",
              "activity_level", "region"]
    filled = sum(1 for f in fields if profile.get(f))
    return int((filled / len(fields)) * 100)


def _build_meal_plan_query(plan_type: str, condition: str, profile: dict) -> str:
    condition_map = {
        "general":     "a generally healthy person",
        "diabetes":    "someone managing Type 2 Diabetes",
        "weight_loss": "someone aiming to lose weight",
        "heart":       "someone with hypertension or heart health concerns",
        "pcos":        "someone with PCOS",
    }
    person_desc = condition_map.get(condition, "a generally healthy person")
    region      = profile.get("region", "Indian")
    pref        = profile.get("dietary_preference", "plant-based")

    if plan_type == "weekly":
        return (
            f"Generate a complete 7-day DIP Diet weekly meal plan for {person_desc}. "
            f"Dietary preference: {pref}. Regional cuisine: {region}. "
            f"Include breakfast (fruit meal) and lunch/dinner for each day. "
            f"Rotate proteins, vegetables, and millets. Add practical cooking tips."
        )
    return (
        f"Generate a detailed DIP Diet daily meal plan for {person_desc}. "
        f"Dietary preference: {pref}. Regional cuisine: {region}. "
        f"Include morning routine, fruit breakfast, main meal, hydration schedule, "
        f"and evening routine. Include approximate nutritional information."
    )


def _lifestyle_query(category: str) -> str:
    queries = {
        "morning":   "What is the ideal DIP Diet morning routine? Give a detailed step-by-step protocol.",
        "sleep":     "How should I optimize sleep for DIP Diet success? Give practical tips.",
        "exercise":  "What exercise routine complements the DIP Diet? Include yoga and walking.",
        "mindful":   "Explain mindful eating practices in the DIP Diet context.",
        "stress":    "How does stress affect diet adherence and what are DIP Diet stress management techniques?",
        "general":   "Give me the top 5 DIP Diet lifestyle discipline tips for beginners.",
    }
    return queries.get(category, queries["general"])


def _save_instructions(new_instructions: str):
    """Persist new instructions to agent_config.py at runtime."""
    config_path = Path("agent_config.py")
    if config_path.exists():
        content = config_path.read_text(encoding="utf-8")
        # Find and replace the AGENT_INSTRUCTIONS string
        start_marker = 'AGENT_INSTRUCTIONS = """'
        end_marker   = '"""'
        start_idx = content.find(start_marker)
        if start_idx != -1:
            end_idx = content.find(end_marker, start_idx + len(start_marker))
            if end_idx != -1:
                new_content = (
                    content[:start_idx + len(start_marker)]
                    + "\n" + new_instructions + "\n"
                    + content[end_idx:]
                )
                config_path.write_text(new_content, encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug)
