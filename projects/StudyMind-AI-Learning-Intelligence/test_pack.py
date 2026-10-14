import urllib.request, json
try:
    res = json.loads(urllib.request.urlopen('http://127.0.0.1:5600/api/study/doc_4347612220').read().decode())
    print(f"Concepts: {len(res.get('concepts', []))}")
    print(f"Flashcards: {len(res.get('flashcards', []))}")
    print(f"Quiz: {len(res.get('quiz', []))}")
    print(f"Summary Extractive: {len(res.get('summary_extractive', []))}")
    print(f"Summary Abstractive Length: {len(res.get('summary_abstractive') or '')}")
except Exception as e:
    print(e)
