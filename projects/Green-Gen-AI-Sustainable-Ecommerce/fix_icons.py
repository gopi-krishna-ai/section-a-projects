import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = """            {% set cat_icons = {
                'Clothing': 'fa-shirt',
                'Footwear': 'fa-shoe-prints',
                'Home Decor & Festive Needs': 'fa-couch',
                'Beauty and Personal Care': 'fa-spa',
                'Computers': 'fa-laptop',
                'Kitchen & Dining': 'fa-utensils',
                'Toys & School Supplies': 'fa-puzzle-piece',
                'Watches': 'fa-clock'
            } %}"""

# Find the {% set cat_icons ... %} block and replace it
html = re.sub(r'\{%\s*set\s+cat_icons\s*=\s*\{.*?\}\s*%\}', replacement, html, flags=re.DOTALL)

# Let's also adjust the grid for 8 items: change lg:grid-cols-6 to lg:grid-cols-4 so it makes a nice 2x4 or 4x2 grid
html = html.replace('lg:grid-cols-6', 'lg:grid-cols-4')

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
