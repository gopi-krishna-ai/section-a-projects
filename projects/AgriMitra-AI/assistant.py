"""
assistant.py

Multilingual-aware farming assistant.

The assistant matches the user's question against a curated knowledge base of
general agricultural guidance. It responds with real, general advice written
for smallholder farmers.

OPTIONAL: if the environment variable OPENAI_API_KEY is set, the assistant
also calls the OpenAI Chat Completions API for free-form questions and uses
the knowledge base as a graceful fallback whenever the API is unavailable.

The assistant itself always returns English text; the Flask layer translates
responses into the user's selected language via translator.py.
"""

import os
import re
import threading

# ---------------------------------------------------------------------------
# Knowledge base: keyword -> answer (general guidance, no guarantees)
# ---------------------------------------------------------------------------

KNOWLEDGE_BASE = [
    {
        "keywords": ["hello", "hi", "hey", "namaste", "good morning", "good evening"],
        "answer": (
            "Hello! I am your farming assistant. You can ask me about crops, "
            "fertilizers, irrigation, soil preparation, pests, or how to use this app."
        ),
    },
    {
        "keywords": ["irrigation", "irrigate", "water", "watering", "how much water", "drip"],
        "answer": (
            "General irrigation guidance: water your crops in the early morning or "
            "late evening to reduce evaporation. The amount of water depends on the "
            "crop, soil type, and weather. Drip irrigation saves up to 50% water "
            "compared to flood irrigation. Avoid over-watering, as it can damage "
            "roots and promote fungal disease. Always monitor rainfall before irrigating."
        ),
    },
    {
        "keywords": ["soil", "prepare", "preparation", "plough", "ph", "soil test"],
        "answer": (
            "General soil preparation guidance: test your soil before planting to know "
            "its pH and nutrient levels. Most crops grow well in soil with pH between "
            "6.0 and 7.5. Plough the field 2-3 weeks before sowing, add organic compost "
            "or farmyard manure, and ensure good drainage. Loosen the soil to let roots "
            "grow easily. Avoid ploughing wet soil as it destroys soil structure."
        ),
    },
    {
        "keywords": ["fertilizer", "fertiliser", "urea", "dap", "npk", "manure", "nutrient"],
        "answer": (
            "General fertilizer guidance: use fertilizers based on a soil test and the "
            "crop's growth stage. Nitrogen (N) promotes leaf growth, Phosphorus (P) "
            "helps roots and flowering, and Potassium (K) improves crop strength and "
            "yield. Apply fertilizers in the correct ratio and avoid over-application, "
            "which can burn plants and pollute groundwater. Organic compost improves "
            "soil health over the long term. Use the Fertilizer Recommendation page in "
            "this app with your soil report values."
        ),
    },
    {
        "keywords": ["pest", "insect", "disease", "fungus", "spray", "pesticide", "insecticide"],
        "answer": (
            "General pest management guidance: inspect crops regularly for insects, "
            "yellowing leaves, or spots. Use neem-based sprays as a first line of "
            "defense. Remove and destroy infected plants to stop the spread. Spray "
            "pesticides early morning or evening, not during strong wind or rain. "
            "Always follow the dosage written on the label and keep a safe gap between "
            "spraying and harvest. If the problem is severe, consult a local agriculture officer."
        ),
    },
    {
        "keywords": ["crop", "grow", "cultivate", "planting", "sowing", "seed", "harvest"],
        "answer": (
            "General crop cultivation guidance: choose crops suited to your soil and "
            "season. Use good-quality certified seeds, sow at the right depth, and "
            "maintain proper spacing between plants. Weed the field regularly, apply "
            "fertilizers at the correct growth stage, and watch the weather forecast "
            "before sowing or harvesting. Use the Crop Recommendation page in this app "
            "with your soil values to see which crops are suitable."
        ),
    },
    {
        "keywords": ["recommendation", "recommend", "crop suggestion", "which crop", "best crop"],
        "answer": (
            "To get a crop recommendation, open the Crop Recommendation page and enter "
            "your soil values: Nitrogen (N), Phosphorus (P), Potassium (K), temperature, "
            "humidity, soil pH and rainfall. The machine learning model will suggest the "
            "most suitable crop for your conditions."
        ),
    },
    {
        "keywords": ["fertilizer recommendation", "which fertilizer", "best fertilizer", "recommend fertilizer"],
        "answer": (
            "To get a fertilizer recommendation, open the Fertilizer Recommendation page "
            "and enter your soil type, crop, moisture, temperature, humidity and the N, P, "
            "K values from your soil test. The machine learning model will suggest a suitable "
            "fertilizer."
        ),
    },
    {
        "keywords": ["app", "how to use", "use this", "help", "feature"],
        "answer": (
            "Here is how to use this app: 1) Login with your account. 2) Open Crop "
            "Recommendation and enter your soil values to see a suitable crop. 3) Open "
            "Fertilizer Recommendation to find a suitable fertilizer. 4) Ask me any "
            "farming question here. 5) Use the History page to review past "
            "recommendations. You can switch the language at the top of the page."
        ),
    },
    {
        "keywords": ["rain", "rainfall", "monsoon", "weather"],
        "answer": (
            "General weather guidance: rainfall and temperature strongly affect crop "
            "choice and fertilizer use. If heavy rain is expected, delay fertilizer "
            "application so it is not washed away. In dry weather, irrigate early "
            "morning or evening. Use the weather card on your dashboard to follow "
            "current conditions."
        ),
    },
    {
        "keywords": ["seed rate", "spacing", "sowing depth", "how deep"],
        "answer": (
            "Sowing guidance depends on the crop, but as a general rule: sow seeds at "
            "2-3 times their own width deep, keep proper row spacing for air and light, "
            "and water lightly after sowing. Check the seed packet or your local "
            "agriculture office for crop-specific seed rate and spacing."
        ),
    },
]

# Generic fallback shown when no keyword matches (and no AI API is configured)
FALLBACK_ANSWER = (
    "I am a knowledge-based assistant, so I can help best with topics like crops, "
    "fertilizers, irrigation, soil preparation, pests, and this app's features. "
    "Please rephrase your question around one of those topics."
)

_llm_lock = threading.Lock()
_llm_client = None


def _get_llm_client():
    """Lazily creates the OpenAI client only when OPENAI_API_KEY is set."""
    global _llm_client
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    with _llm_lock:
        if _llm_client is None:
            try:
                from openai import OpenAI

                _llm_client = OpenAI(api_key=api_key)
            except ImportError:
                _llm_client = False  # package not installed -> no LLM
    return _llm_client if _llm_client else None


def _match_knowledge_base(question):
    """Finds the best matching knowledge-base entry for a question."""
    normalized = question.lower().strip()
    best = None
    best_score = 0
    for entry in KNOWLEDGE_BASE:
        score = 0
        for keyword in entry["keywords"]:
            if re.search(r"\b" + re.escape(keyword) + r"\b", normalized) or keyword in normalized:
                score += 1
        if score > best_score:
            best_score = score
            best = entry
    if best_score > 0:
        return best["answer"]
    return None


def _ask_llm(question, language_hint):
    """Optional LLM call. Returns None on any failure so callers can fall back."""
    client = _get_llm_client()
    if not client:
        return None
    try:
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful agricultural assistant for small farmers "
                        "in India. Give simple, practical, general guidance. Answer in "
                        f"{language_hint}. Keep answers under 120 words. Never claim "
                        "guaranteed yields."
                    ),
                },
                {"role": "user", "content": question},
            ],
            max_tokens=300,
            timeout=20,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def get_assistant_reply(question, language="en"):
    """
    Returns an assistant reply for the question as (reply, source).

    Priority: knowledge base match -> optional LLM (if OPENAI_API_KEY set) -> fallback.
    The reply is English unless the LLM is used (which may answer in the
    requested language).
    """
    question = (question or "").strip()
    if not question:
        return (
            "Please type or speak a question. For example: "
            "'Which crop is good for my soil?' or 'When should I irrigate?'",
            "fallback",
        )

    kb_answer = _match_knowledge_base(question)

    # For the app's own features and clear knowledge-base topics,
    # prefer the curated answer (always available, offline).
    if kb_answer and not os.environ.get("OPENAI_API_KEY", "").strip():
        return kb_answer, "knowledge-base"

    # With an API key: let the LLM answer first, fall back to the knowledge base.
    llm_answer = _ask_llm(question, _language_name(language))
    if llm_answer:
        return llm_answer, "llm"
    if kb_answer:
        return kb_answer, "knowledge-base"
    return FALLBACK_ANSWER, "knowledge-base"


def _language_name(code):
    names = {
        "en": "English",
        "hi": "Hindi",
        "kn": "Kannada",
        "ta": "Tamil",
        "te": "Telugu",
    }
    return names.get(code, "English")
