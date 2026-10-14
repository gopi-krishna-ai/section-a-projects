import random
with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

route_code = """
@app.route('/refurbished')
def refurbished():
    user = get_current_user()
    
    # Get a random sample of products to act as refurbished/recycled
    all_products = Product.query.all()
    import random
    refurbished_products = random.sample(all_products, min(12, len(all_products))) if all_products else []
    
    # Assign a mock 'recycled_by' property to each for display
    mock_names = ['Alice', 'Bob', 'Carol', 'David', 'Emma', 'Frank', 'Grace', 'Henry']
    for p in refurbished_products:
        p.recycled_by = random.choice(mock_names)
        # Reduce price by 40% for refurbished
        p.refurbished_price = int(p.price_inr * 0.6)
        
    return render_template('refurbished.html', products=refurbished_products, user=user)
"""

if 'def refurbished(' not in app_py:
    app_py = app_py.replace("@app.route('/products')", route_code + "\n@app.route('/products')")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_py)
