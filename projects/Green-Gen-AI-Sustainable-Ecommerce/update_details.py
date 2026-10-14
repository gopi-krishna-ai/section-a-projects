with open('templates/product_details.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """                <div class="mt-8 flex gap-4">
                    <button onclick="addToCart('{{ product.id }}')" class="flex-1 bg-green-600 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm transition-colors">
                        Add to Cart
                    </button>
                    <a href="{{ url_for('customize', product_id=product.id) }}" class="flex-1 bg-white border border-gray-300 rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm transition-colors">
                        <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> 3D Customize
                    </a>
                </div>"""

replacement = """                <div class="mt-8 flex flex-col gap-4">
                    <div class="flex gap-4">
                        <button onclick="addToCart('{{ product.id }}')" class="flex-1 bg-green-600 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm transition-colors">
                            Add to Cart
                        </button>
                        <a href="{{ url_for('customize', product_id=product.id) }}" class="flex-1 bg-white border border-gray-300 rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm transition-colors">
                            <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> 3D Customize
                        </a>
                    </div>
                    {% if user and user.is_admin %}
                    <form action="{{ url_for('remove_product', product_id=product.id) }}" method="POST" onsubmit="return confirm('Are you sure you want to completely remove this product from the database?');">
                        <button type="submit" class="w-full bg-red-100 border border-transparent rounded-md py-3 px-8 flex items-center justify-center text-base font-medium text-red-700 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 shadow-sm transition-colors">
                            <i class="fa-solid fa-trash mr-2"></i> Delete Product (Admin)
                        </button>
                    </form>
                    {% endif %}
                </div>"""

html = html.replace(target, replacement)
with open('templates/product_details.html', 'w', encoding='utf-8') as f:
    f.write(html)
