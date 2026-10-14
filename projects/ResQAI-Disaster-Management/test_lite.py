from duckduckgo_search import DDGS
print(DDGS().text("hurricane updates", max_results=3, backend="lite"))
