import json
import os
import threading
import urllib.request
import urllib.parse
import time

language_codes = {
    "en": "en",
    "kn": "kn",
    "hi": "hi",
    "te": "te",
    "ta": "ta",
    "fr": "fr",
    "es": "es"
}

_CACHE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "database", "translation_cache.json"
)
_CACHE_MAX = 20000
_cache = {}
_lock = threading.Lock()
_CHUNK_SIZE = 5

def _load_cache():
    global _cache
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE, "r", encoding="utf-8") as f:
                _cache = json.load(f)
        except Exception:
            _cache = {}

def _save_cache():
    try:
        os.makedirs(os.path.dirname(_CACHE_FILE), exist_ok=True)
        with open(_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(_cache, f, ensure_ascii=False)
    except Exception:
        pass

_load_cache()

def _cache_key(lang, text):
    return "en>" + lang + "|" + text

def _google_translate(text, target):
    if not text or not text.strip(): return text
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target}&dt=t&q={urllib.parse.quote(text)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        data = json.loads(response)
        return "".join([sentence[0] for sentence in data[0]])
    except Exception as e:
        print(f"GTX Translate Error: {e}")
        return None

def _translate_batch(texts, lang):
    """One NLP API round trip for a chunk of texts, using newlines to bypass rate limit."""
    if not texts:
        return []
    
    target = language_codes.get(lang, "en")

    def translate_chunk(chunk):
        try:
            # Join by a special delimiter to translate in one single request!
            joined = " \n ".join(chunk)
            res = _google_translate(joined, target)
            if res:
                return [s.strip() for s in res.split("\n")]
            return [translate_text(t, lang) for t in chunk]
        except Exception as exc:
            print(f"Batch translate error: {exc}")
            return [translate_text(t, lang) for t in chunk]

    if len(texts) <= 1:
        return translate_chunk(texts)

    out = []
    chunks = [texts[i:i + _CHUNK_SIZE] for i in range(0, len(texts), _CHUNK_SIZE)]
    for chunk in chunks:
        out.extend(translate_chunk(chunk))
        time.sleep(0.5) # Slight delay to prevent hitting GTX limits
        
    if len(out) != len(texts):
        print("Batch split length mismatch! Falling back to individual translation.")
        out = [translate_text(t, lang) for t in texts]

    return out

def translate_text(text, lang):
    if lang == "en" or not text:
        return text

    key = _cache_key(lang, text)
    with _lock:
        if key in _cache:
            return _cache[key]

    translated = _google_translate(text, language_codes.get(lang, "en"))
    if not translated:
        translated = text

    with _lock:
        if translated != text or lang == "en":
            _cache[key] = translated
            if len(_cache) > _CACHE_MAX:
                _cache.clear()
            _save_cache()
    return translated

def translate_texts(texts, lang):
    if lang == "en":
        return list(texts)

    out = []
    missing = []

    with _lock:
        for t in texts:
            if not t or not str(t).strip():
                out.append(t)
                continue
            key = _cache_key(lang, t)
            if key in _cache:
                out.append(_cache[key])
            else:
                out.append(None)
                missing.append((key, t))

    if missing:
        missing_texts = [m[1] for m in missing]
        translated = _translate_batch(missing_texts, lang)
        
        with _lock:
            for i, (key, original) in enumerate(missing):
                t_val = translated[i] if i < len(translated) else original
                if t_val != original or lang == "en":
                    _cache[key] = t_val
                
            if len(_cache) > _CACHE_MAX:
                _cache.clear()
            _save_cache()

        missing_idx = 0
        for i in range(len(out)):
            if out[i] is None:
                out[i] = translated[missing_idx] if missing_idx < len(translated) else missing[missing_idx][1]
                missing_idx += 1

    return out

def translate_to_english(text):
    if not text or not str(text).strip():
        return text
        
    # First, detect if it's already english
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        data = json.loads(response)
        return "".join([sentence[0] for sentence in data[0]])
    except Exception as e:
        print(f"Translate to English Error: {e}")
        return text
