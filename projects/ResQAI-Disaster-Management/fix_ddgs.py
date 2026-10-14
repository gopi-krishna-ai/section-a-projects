import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("DDGS().text(search_query, max_results=3)", "DDGS().text(search_query, max_results=3, backend='lite')")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
