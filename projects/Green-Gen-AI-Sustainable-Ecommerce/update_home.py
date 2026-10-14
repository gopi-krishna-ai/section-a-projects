with open('templates/home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

shop_by_category_pattern = """<!-- Shop by Category -->
<div class="bg-white py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-2xl font-extrabold tracking-tight text-gray-900 mb-6">Shop by Category</h2>
        <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
            {% for cat in categories %}
            <a href="{{ url_for('product_catalog', category=cat) }}" class="relative rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm flex items-center space-x-3 hover:border-green-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-green-500 transition-colors">
                <div class="flex-1 min-w-0">
                    <span class="absolute inset-0" aria-hidden="true"></span>
                    <p class="text-sm font-medium text-gray-900 text-center">{{ cat }}</p>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</div>"""

new_shop_by_category = """<!-- Shop by Category -->
<div class="bg-gray-50 py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
            <h2 class="text-3xl font-extrabold tracking-tight text-gray-900">Explore Sustainable Categories</h2>
            <p class="mt-4 max-w-2xl mx-auto text-xl text-gray-500">Discover products that align with your eco-friendly lifestyle.</p>
        </div>
        <div class="grid grid-cols-2 gap-6 sm:grid-cols-3 lg:grid-cols-6">
            {% set cat_icons = {
                'Computers': 'fa-laptop',
                'Footwear': 'fa-shoe-prints',
                'Pens & Stationery': 'fa-pen-nib',
                'Sports & Fitness': 'fa-dumbbell',
                'Jewellery': 'fa-gem',
                'Mobiles & Accessories': 'fa-mobile-screen-button'
            } %}
            {% set cat_colors = ['bg-emerald-100 text-emerald-600', 'bg-teal-100 text-teal-600', 'bg-cyan-100 text-cyan-600', 'bg-sky-100 text-sky-600', 'bg-blue-100 text-blue-600', 'bg-indigo-100 text-indigo-600'] %}
            
            {% for cat in categories %}
            <a href="{{ url_for('product_catalog', category=cat) }}" class="group relative rounded-2xl bg-white p-6 shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 flex flex-col items-center border border-gray-100 overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-br from-green-50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                
                {% set icon = cat_icons.get(cat, 'fa-box-open') %}
                {% set color_class = cat_colors[loop.index0 % cat_colors|length] %}
                
                <div class="relative z-10 w-16 h-16 mb-4 rounded-full flex items-center justify-center {{ color_class }} shadow-sm group-hover:scale-110 transition-transform duration-300">
                    <i class="fa-solid {{ icon }} text-2xl"></i>
                </div>
                
                <p class="relative z-10 text-sm font-bold text-gray-800 text-center uppercase tracking-wider">{{ cat }}</p>
                <div class="mt-3 relative z-10 flex items-center text-xs text-green-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    Shop Now <i class="fa-solid fa-arrow-right ml-1"></i>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</div>"""

if shop_by_category_pattern in home_html:
    home_html = home_html.replace(shop_by_category_pattern, new_shop_by_category)
else:
    print("Could not find exact block to replace")

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(home_html)
