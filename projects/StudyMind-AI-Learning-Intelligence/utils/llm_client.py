"""Optional local LLM client using Ollama.

The app remains usable without Ollama: document retrieval/QA still works.
When Ollama is available, it provides open-ended answers and can ground answers
in retrieved document passages when useful.
"""
import json
import os
import urllib.error
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "120"))


def status():
    req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
    try:
        with urllib.request.urlopen(req, timeout=4) as r:
            data = json.loads(r.read().decode("utf-8"))
        models = [m.get("name", "") for m in data.get("models", [])]
        installed = OLLAMA_MODEL in models or any(x.split(":")[0] == OLLAMA_MODEL.split(":")[0] for x in models)
        return {"available": True, "model": OLLAMA_MODEL, "installed": installed, "models": models[:30]}
    except Exception as exc:
        return {"available": False, "model": OLLAMA_MODEL, "installed": False, "error": str(exc), "models": []}


def chat(messages, temperature=0.2, num_predict=600):
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": num_predict}
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read().decode("utf-8"))
        text = ((data.get("message") or {}).get("content") or "").strip()
        if not text:
            raise RuntimeError("Ollama returned an empty response.")
        return text
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {body[:300]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError("Ollama is not running. Start Ollama and load the configured model.") from exc


def answer(question, context=None, doc_name=None):
    base = (
        "You are StudyMind, a helpful study assistant. Answer the user's question directly. "
        "You may answer general knowledge questions even when no document is provided. "
        "When document context is supplied, use it when relevant and clearly say when you are "
        "using the uploaded material. Do not invent facts that are contradicted by the context. "
        "For calculations, show concise steps. If the question is ambiguous, state the assumption."
    )
    if context:
        user = (
            f"Question: {question}\n\n"
            f"Uploaded document context ({doc_name or 'selected document'}):\n{context}\n\n"
            "Use the context when it answers the question; otherwise answer from your general knowledge "
            "and say that the answer is not directly stated in the document."
        )
    else:
        user = f"Question: {question}\n\nAnswer naturally and helpfully."
    return chat([
        {"role": "system", "content": base},
        {"role": "user", "content": user},
    ])
