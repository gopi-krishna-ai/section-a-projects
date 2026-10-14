import re
with open('static/js/dashboard.js', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace any non-ascii character before 'C' for temperature
content = re.sub(r'[^a-zA-Z0-9\s"\'+\-]C', '&deg;C', content)
content = content.replace('AC', '&deg;C')

# Fix corrupted strings like 'dY"?'
content = content.replace('dY"?', '<i class="fa-solid fa-location-dot"></i>')

# Specifically fix the known line in dashboard.js if regex didn't catch it
content = re.sub(r'"C"', '"&deg;C"', content)
content = re.sub(r'"\?C"', '"&deg;C"', content)
content = re.sub(r'innerHTML = `.*? \$\{city\}', 'innerHTML = `<i class="fa-solid fa-location-dot"></i> ${city}', content)
content = re.sub(r'innerHTML = `.*? \$\{parseFloat\(lat\)', 'innerHTML = `<i class="fa-solid fa-location-dot"></i> ${parseFloat(lat)', content)

with open('static/js/dashboard.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
