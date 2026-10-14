import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

route_code = '''
# --- CHATBOT FEATURE ---
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    query = data.get('query', '').lower()
    
    if not query:
        return jsonify({"reply": "I'm the Green Gen AI assistant! Ask me for a product to see its eco-score and price."})
        
    # Search for products matching the query
    # We do a basic search in name or category
    from models import Product
    import re
    
    # Simple extraction of keywords to search
    words = [w for w in query.split() if len(w) > 3 and w not in ["show", "find", "need", "want", "some", "product", "with", "price", "score"]]
    if not words:
        words = query.split()
        
    search_term = words[0] if words else query
    
    products = Product.query.filter(
        db.or_(
            Product.name.ilike(f"%{search_term}%"),
            Product.category.ilike(f"%{search_term}%")
        )
    ).limit(3).all()
    
    if not products:
        return jsonify({"reply": f"I couldn't find any products matching '{search_term}'. Try searching for things like 'shirt', 'laptop', or 'shoe'."})
        
    reply_html = f"<p>Here are some <strong>{search_term}</strong> options I found:</p><div style='display:flex; flex-direction:column; gap:10px; margin-top:10px;'>"
    
    for p in products:
        reply_html += f"""
        <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; background: white;">
            <p style="font-weight:bold; margin-bottom: 5px;">{p.name}</p>
            <p style="margin-bottom: 5px; font-size: 0.9em;">
                <span style="color: #059669;"><i class="fas fa-leaf"></i> Eco Score: {p.eco_score}/10</span> | 
                <span style="color: #4b5563;"><i class="fas fa-tag"></i> ₹{p.price_inr}</span>
            </p>
            <a href="/product/{p.id}" style="display: inline-block; background: #059669; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 0.85em;">View Product</a>
        </div>
        """
    reply_html += "</div>"
    
    return jsonify({"reply": reply_html})

'''

idx = content.find('if __name__ ==')
content = content[:idx] + route_code + content[idx:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app.py")
