import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("userid != 'admin'", "userid != 'admin@agrimitra'")
content = content.replace('userid != "admin"', 'userid != "admin@agrimitra"')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('app.py updated')
