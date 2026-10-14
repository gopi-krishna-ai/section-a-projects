from duckduckgo_search import DDGS
try:
    response = DDGS().chat("Hello, who are you?", model="gpt-4o-mini")
    print("Success:", response)
except Exception as e:
    print("Error:", e)
