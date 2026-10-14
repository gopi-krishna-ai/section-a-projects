import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from ddgs import DDGS", "from duckduckgo_search import DDGS")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
