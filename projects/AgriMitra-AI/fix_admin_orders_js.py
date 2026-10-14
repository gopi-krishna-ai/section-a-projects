import re

with open('templates/admin.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the null status issue in admin.html by providing a default
old_badge = """<span style="padding:3px 8px; border-radius:12px; background:${o.status.includes('Pending')?'#fef08a':(o.status.includes('Awaiting')?'#bae6fd':(o.status.includes('Location')?'#e9d5ff':'#bbf7d0'))}; color:#111; font-size:12px; font-weight:bold;">${o.status}</span>"""
new_badge = """<span style="padding:3px 8px; border-radius:12px; background:${(o.status||'Pending').includes('Pending')?'#fef08a':((o.status||'Awaiting').includes('Awaiting')?'#bae6fd':((o.status||'Location').includes('Location')?'#e9d5ff':'#bbf7d0'))}; color:#111; font-size:12px; font-weight:bold;">${o.status||'Pending Approval'}</span>"""

content = content.replace(old_badge, new_badge)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed admin.html status null reference")
