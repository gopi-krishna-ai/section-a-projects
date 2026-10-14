import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

js_content = js_content.replace('updateCartIcon();', 'updateCartBadge();')

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Fixed updateCartIcon -> updateCartBadge")
