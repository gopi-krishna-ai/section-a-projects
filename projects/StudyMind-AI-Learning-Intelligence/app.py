"""
AI Learning Intelligence for Notes and PDF Analysis
Flask web application entry point.
"""

import os
import socket
import secrets

import joblib
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

from utils import document_engine as de
from utils import library
from utils import llm_client
from utils.auth import register_user, verify_user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
BENCHMARK_PATH = os.path.join(BASE_DIR, "model", "qa_benchmark.pkl")

ALLOWED = {".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".txt", ".md"}
MAX_MB = 25

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["MAX_CONTENT_LENGTH"] = MAX_MB * 1024 * 1024


def benchmark():
    if os.path.exists(BENCHMARK_PATH):
        try:
            return joblib.load(BENCHMARK_PATH)
        except Exception:
            return {}
    return {}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            return render_template("login.html", error="Please enter both username and password.")
            
        if action == "register":
            if register_user(username, password):
                session["user"] = username
                return redirect(url_for("workspace"))
            else:
                return render_template("login.html", error="Username already exists.")
                
        elif action == "login":
            if verify_user(username, password):
                session["user"] = username
                return redirect(url_for("workspace"))
            else:
                return render_template("login.html", error="Invalid username or password.")
                
    if "user" in session:
        return redirect(url_for("workspace"))
        
    return render_template("login.html")


@app.route("/workspace")
def workspace():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("index.html",
                           benchmark=benchmark(),
                           ocr_available=de.ocr_available())


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/api/documents")
def api_documents():
    return jsonify({"rows": library.list_documents()})


@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file was uploaded."}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "No file selected."}), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ALLOWED:
        return jsonify({"error": f"Unsupported file type '{ext}'. "
                                  f"Allowed: {', '.join(sorted(ALLOWED))}"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe = secure_filename(f.filename)
    path = os.path.join(UPLOAD_DIR, safe)
    f.save(path)

    doc = library.add_document(path, safe)
    if "error" in doc:
        return jsonify(doc), 400
    return jsonify({"id": doc["id"], "name": doc["name"], "pages": doc["pages"],
                    "words": doc["words"], "language": doc["language"],
                    "ocr_pages": doc["ocr_pages"], "topic_count": len(doc["topics"])})


@app.route("/api/documents/<doc_id>", methods=["DELETE"])
def api_delete(doc_id):
    if not library.delete_document(doc_id):
        return jsonify({"error": "Document not found."}), 404
    return jsonify({"deleted": True})


@app.route("/api/study/<doc_id>")
def api_study(doc_id):
    pack = library.study_pack(doc_id)
    if "error" in pack:
        return jsonify(pack), 404
    return jsonify(pack)


@app.route("/api/ask", methods=["POST"])
def api_ask():
    d = request.get_json(silent=True) or {}
    q = (d.get("question") or "").strip()
    if not q:
        return jsonify({"error": "Please enter a question."}), 400
    result = library.ask(q, doc_id=d.get("doc_id") or None)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)




@app.route("/api/llm/status")
def api_llm_status():
    return jsonify(llm_client.status())


@app.route("/api/ask-ai", methods=["POST"])
def api_ask_ai():
    d = request.get_json(silent=True) or {}
    q = (d.get("question") or "").strip()
    if not q:
        return jsonify({"error": "Please enter a question."}), 400
    use_docs = bool(d.get("use_docs", True))
    doc_id = d.get("doc_id") or None

    context = None
    source = None
    sources = []
    if use_docs:
        hits = library.semantic_search(q, doc_id=doc_id, top_k=5)
        if hits:
            context = "\n\n".join(f"[Page {h['page']}] {h['text']}" for h in hits)
            source = {"doc_name": hits[0]["doc_name"], "page": hits[0]["page"], "doc_id": hits[0]["doc_id"]}
            sources = hits

    st = llm_client.status()
    if not (st.get("available") and st.get("installed")):
        return jsonify({
            "error": "Local LLM is not ready. Install/start Ollama and run the configured model, or use the document-only Ask mode.",
            "setup": "ollama run llama3.2:3b"
        }), 503

    try:
        answer = llm_client.answer(q, context=context, doc_name=(source or {}).get("doc_name"))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 503
    return jsonify({
        "answer": answer,
        "mode": "documents + AI" if context else "general AI",
        "model": llm_client.OLLAMA_MODEL,
        "source": source,
        "sources": sources,
    })


@app.route("/api/search", methods=["POST"])
def api_search():
    d = request.get_json(silent=True) or {}
    q = (d.get("query") or "").strip()
    if not q:
        return jsonify({"error": "Please enter a search query."}), 400
    return jsonify({"rows": library.semantic_search(q, doc_id=d.get("doc_id") or None,
                                                     top_k=int(d.get("top_k", 6)))})


@app.route("/api/explain", methods=["POST"])
def api_explain():
    d = request.get_json(silent=True) or {}
    term = (d.get("term") or "").strip()
    doc_id = d.get("doc_id")
    if not term or not doc_id:
        return jsonify({"error": "A term and a document are required."}), 400
    result = library.explain_concept(doc_id, term)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)


@app.route("/api/benchmark")
def api_benchmark():
    return jsonify(benchmark())


def find_free_port(preferred, attempts=20):
    """First genuinely usable port at or after `preferred`.

    A killed server can leave a stale LISTENING socket on Windows that accepts
    connections then resets them, which the browser reports as "could not reach
    the server". Probing with a real connect() skips those dead sockets.
    """
    for port in range(preferred, preferred + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.4)
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                continue
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder:
                binder.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                binder.bind(("127.0.0.1", port))
            return port
        except OSError:
            continue
    raise RuntimeError(f"No free port in range {preferred}-{preferred + attempts}.")


if __name__ == "__main__":
    chosen = find_free_port(int(os.environ.get("PORT", 5600)))
    print("\n" + "=" * 68)
    print("  AI Learning Intelligence for Notes and PDF Analysis")
    print(f"  Open this in your browser:  http://127.0.0.1:{chosen}/")
    print("  (first request loads the AI models - allow a few seconds)")
    print("=" * 68 + "\n")
    app.run(debug=True, port=chosen, use_reloader=False)
