with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """<a href="{{ url_for('product_catalog') }}" class="text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-green-500 text-sm font-medium">Shop</a>"""

replacement = """<a href="{{ url_for('product_catalog') }}" class="text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-green-500 text-sm font-medium">Shop</a>
                        <a href="{{ url_for('refurbished') }}" class="text-gray-500 hover:text-emerald-600 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-emerald-500 text-sm font-medium"><i class="fa-solid fa-recycle mr-1"></i> Refurbished</a>"""

html = html.replace(target, replacement)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
