with open('templates/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Footwear ID
html = html.replace("'Footwear': '1549298916-b5a932d56a31'", "'Footwear': '1542291026-7eec264c27ff'")

# Fix Beauty ID
html = html.replace("'Beauty and Personal Care': '1596462502278-27bf840dda00'", "'Beauty and Personal Care': '1598440947619-225228b3f11d'")

# Fix text size to prevent overlapping
html = html.replace('<span class="text-white text-xs font-bold leading-tight">{{ cat }}</span>', '<span class="text-white text-[10px] sm:text-[11px] font-bold leading-tight px-1 drop-shadow-md">{{ cat }}</span>')

# Make "All Categories" text slightly smaller too so it matches
html = html.replace('<span class="text-white text-xs font-bold shadow-sm">All Categories</span>', '<span class="text-white text-[10px] sm:text-[11px] font-bold shadow-sm px-1 drop-shadow-md">All Categories</span>')

with open('templates/products.html', 'w', encoding='utf-8') as f:
    f.write(html)
