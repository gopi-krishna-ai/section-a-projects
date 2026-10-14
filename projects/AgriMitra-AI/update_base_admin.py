import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("current_user.userid == 'admin'", "current_user.userid == 'admin@agrimitra'")
content = content.replace('current_user.userid == "admin"', 'current_user.userid == "admin@agrimitra"')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('base.html updated')
