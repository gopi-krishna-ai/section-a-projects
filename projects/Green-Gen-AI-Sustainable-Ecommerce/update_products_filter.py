import re

with open('templates/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

category_filter = """            <div class="border-b border-gray-200 py-6">
              <h3 class="-my-3 flow-root">
                <span class="font-medium text-gray-900">Category</span>
              </h3>
              <div class="pt-6">
                <div class="grid grid-cols-2 gap-3">
                  {% set cat_images = {
                    'Clothing': '1515886657613-9f3515b0c78f',
                    'Footwear': '1549298916-b5a932d56a31',
                    'Home Decor & Festive Needs': '1513694203232-719a280e022f',
                    'Beauty and Personal Care': '1596462502278-27bf840dda00',
                    'Computers': '1517336714731-489689fd1ca8',
                    'Kitchen & Dining': '1556910103-1c02745aae4d',
                    'Toys & School Supplies': '1596461404969-9ae70f2830c1',
                    'Watches': '1523170335258-f5ed11844a49'
                  } %}
                  
                  <button type="submit" name="category" value="" class="relative h-20 rounded-lg overflow-hidden group focus:outline-none focus:ring-2 focus:ring-green-500">
                      <div class="absolute inset-0 bg-gray-200"></div>
                      <div class="absolute inset-0 bg-gray-900 bg-opacity-40 group-hover:bg-opacity-50 transition-all {% if not request.args.get('category') %}ring-4 ring-inset ring-green-500{% endif %}"></div>
                      <div class="absolute inset-0 flex items-center justify-center p-2 text-center">
                          <span class="text-white text-xs font-bold shadow-sm">All Categories</span>
                      </div>
                  </button>
                  
                  {% for cat in categories %}
                  {% set img_id = cat_images.get(cat, '1542601906990-b4d3fb778b09') %}
                  <button type="submit" name="category" value="{{ cat }}" class="relative h-20 rounded-lg overflow-hidden group focus:outline-none focus:ring-2 focus:ring-green-500 shadow-sm">
                      <img src="https://images.unsplash.com/photo-{{ img_id }}?auto=format&fit=crop&w=200&q=80" alt="{{ cat }}" class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
                      <div class="absolute inset-0 bg-gray-900 bg-opacity-40 group-hover:bg-opacity-50 transition-all {% if request.args.get('category') == cat %}ring-4 ring-inset ring-green-500 bg-opacity-60{% endif %}"></div>
                      <div class="absolute inset-0 flex items-center justify-center p-2 text-center">
                          <span class="text-white text-xs font-bold leading-tight">{{ cat }}</span>
                      </div>
                  </button>
                  {% endfor %}
                </div>
              </div>
            </div>"""

# Remove the hidden input for category so it doesn't conflict with the buttons
html = re.sub(r'\{%\s*if request\.args\.get\(\'category\'\)\s*%\}\s*<input type="hidden" name="category".*?>\s*\{%\s*endif\s*%\}', '', html, flags=re.DOTALL)

# Insert the category filter before the Eco Score filter
if '<div class="border-b border-gray-200 py-6">' in html:
    html = html.replace('<div class="border-b border-gray-200 py-6">', category_filter + '\n\n            <div class="border-b border-gray-200 py-6">', 1)

with open('templates/products.html', 'w', encoding='utf-8') as f:
    f.write(html)
