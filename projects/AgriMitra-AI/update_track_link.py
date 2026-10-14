import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    content = f.read()

# I don't know the exact string, let's just use regex to replace the href of Track Orders
content = re.sub(r'<a[^>]*Track Orders[^<]*</a>', r'<a href="/my-orders" style="color: var(--c-primary); text-decoration: none; font-weight: bold; font-size: 14px;">Track Orders</a>', content)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Track Orders link in common.js")
