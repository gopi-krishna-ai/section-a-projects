import os
import re

def build_chatbot():
    with open('backend/routes.py', 'r', encoding='utf-8') as f:
        routes_code = f.read()

    # --- 1. ADD CHATBOT ROUTES ---
    chatbot_routes = """
    @app.route('/assistant')
    def assistant():
        return render_template('assistant.html')

    @app.route('/api/chat', methods=['POST'])
    def api_chat():
        user_message = request.json.get('message', '').lower()
        
        # 1. Check for greetings
        greetings = ['hello', 'hi', 'hey', 'help']
        if any(g in user_message.split() for g in greetings):
            return jsonify({
                "reply": "Hello! I am your SmartCart AI Assistant. I can help you find products, look for gifts, or filter items by price (e.g., 'find me running shoes under $50'). How can I help you today?",
                "products": []
            })
            
        # 2. Extract Price Constraints (e.g., "under 50", "< 100")
        import re
        price_limit = None
        price_match = re.search(r'(under|below|<|less than)\\s*\\$?\\s*(\\d+)', user_message)
        if price_match:
            price_limit = float(price_match.group(2))
            
        # 3. Keyword Scoring Algorithm
        stopwords = {'a', 'an', 'the', 'is', 'i', 'want', 'need', 'looking', 'for', 'find', 'me', 'some', 'under', 'below', 'with', 'and', 'or', 'to', 'buy', 'show'}
        words = set(re.findall(r'\\w+', user_message))
        keywords = words - stopwords
        
        if not keywords and not price_limit:
            return jsonify({
                "reply": "I'm not quite sure what you're looking for. Could you describe the product a bit more?",
                "products": []
            })
            
        products = Product.query.all()
        scored_products = []
        
        for p in products:
            score = 0
            search_text = f"{p.name} {p.description} {p.category.name} {p.tags}".lower()
            
            # Score based on keywords
            for kw in keywords:
                if kw in search_text:
                    score += 1
                    # Bonus if it's in the name or category
                    if kw in p.name.lower(): score += 2
                    if kw in p.category.name.lower(): score += 2
            
            if score > 0:
                # Apply price filter
                if price_limit and p.price > price_limit:
                    continue
                scored_products.append((score, p))
                
        # Sort by score descending
        scored_products.sort(key=lambda x: x[0], reverse=True)
        top_products = [p for score, p in scored_products[:3]]
        
        if top_products:
            reply_text = f"I found some great options for you based on your request!"
            if price_limit:
                reply_text += f" All under ${price_limit}."
                
            prod_data = []
            for p in top_products:
                prod_data.append({
                    "id": p.id,
                    "name": p.name,
                    "price": round(p.price, 2),
                    "image": p.image_url if p.image_url.startswith('http') else url_for('static', filename=p.image_url),
                    "category": p.category.name
                })
                
            return jsonify({
                "reply": reply_text,
                "products": prod_data
            })
        else:
            return jsonify({
                "reply": "I couldn't find any exact matches for that in our current catalog. Try adjusting your search terms or price limit!",
                "products": []
            })
"""

    if "@app.route('/assistant')" not in routes_code:
        routes_code += chatbot_routes
        with open('backend/routes.py', 'w', encoding='utf-8') as f:
            f.write(routes_code)
        print("Chatbot routes added.")

    # --- 2. CREATE ASSISTANT HTML ---
    assistant_html = """{% extends "base.html" %}
{% block content %}
<style>
    .chat-container {
        height: 600px;
        background: #f8f9fa;
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
    }
    .chat-header {
        background: linear-gradient(135deg, var(--primary), #3b82f6);
        color: white;
        padding: 20px;
        font-weight: bold;
    }
    .chat-messages {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    .message {
        max-width: 80%;
        padding: 12px 18px;
        border-radius: 20px;
        animation: fadeIn 0.3s ease;
    }
    .message.bot {
        background: white;
        align-self: flex-start;
        border-bottom-left-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        border: 1px solid rgba(0,0,0,0.05);
    }
    .message.user {
        background: var(--primary);
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 5px;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
    }
    .chat-input-area {
        padding: 20px;
        background: white;
        border-top: 1px solid rgba(0,0,0,0.05);
    }
    .bot-product-card {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 10px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        background: #fafafa;
        transition: 0.2s;
    }
    .bot-product-card:hover {
        background: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transform: translateY(-2px);
    }
    .typing-indicator {
        display: none;
        align-self: flex-start;
        background: white;
        padding: 12px 18px;
        border-radius: 20px;
        border-bottom-left-radius: 5px;
        margin-bottom: 15px;
    }
    .typing-dot {
        height: 8px; width: 8px; background: #bbb; border-radius: 50%; display: inline-block;
        animation: typing 1.4s infinite ease-in-out both; margin-right: 3px;
    }
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>

<div class="row mt-4 mb-5 justify-content-center">
    <div class="col-md-8">
        <div class="chat-container">
            <div class="chat-header d-flex align-items-center">
                <div class="bg-white rounded-circle d-flex align-items-center justify-content-center me-3 shadow-sm" style="width: 45px; height: 45px;">
                    <i class="fas fa-robot text-primary fs-4"></i>
                </div>
                <div>
                    <h5 class="mb-0">SmartCart AI Assistant</h5>
                    <small class="opacity-75"><i class="fas fa-circle text-success" style="font-size: 8px;"></i> Online and ready to help</small>
                </div>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    Hello! I'm your personal shopping assistant. Tell me what you're looking for, and I'll find the best options in our catalog. <br><br>
                    <small class="text-muted"><strong>Try asking:</strong> "Find me running shoes under $40" or "I need a powerful laptop"</small>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>
            </div>
            
            <div class="chat-input-area">
                <form id="chatForm" class="d-flex">
                    <input type="text" id="userInput" class="form-control rounded-pill px-4 py-2 me-2" placeholder="Type your message here..." autocomplete="off" required>
                    <button type="submit" class="btn btn-primary rounded-circle" style="width: 45px; height: 45px; flex-shrink: 0;">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
document.getElementById('chatForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (!message) return;
    
    // Add User Message
    addMessage(message, 'user');
    input.value = '';
    
    // Show typing
    const typing = document.getElementById('typingIndicator');
    const messagesDiv = document.getElementById('chatMessages');
    typing.style.display = 'block';
    messagesDiv.appendChild(typing);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        const data = await response.json();
        
        typing.style.display = 'none';
        
        // Add Bot Message
        let botHtml = data.reply;
        if (data.products && data.products.length > 0) {
            botHtml += '<div class="mt-2">';
            data.products.forEach(p => {
                botHtml += `
                    <div class="bot-product-card">
                        <img src="${p.image}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" class="me-3">
                        <div class="flex-grow-1">
                            <div class="fw-bold text-dark" style="font-size: 0.9rem;">${p.name}</div>
                            <div class="text-primary fw-bold">$${p.price}</div>
                        </div>
                        <a href="/product/${p.id}" class="btn btn-sm btn-dark rounded-pill px-3">View</a>
                    </div>
                `;
            });
            botHtml += '</div>';
        }
        
        addMessage(botHtml, 'bot', true);
        
    } catch (err) {
        typing.style.display = 'none';
        addMessage("Sorry, I'm having trouble connecting to the server.", 'bot');
    }
});

function addMessage(text, sender, isHtml=false) {
    const messagesDiv = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    if (isHtml) {
        msgDiv.innerHTML = text;
    } else {
        msgDiv.textContent = text;
    }
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
</script>
{% endblock %}"""

    with open('templates/assistant.html', 'w', encoding='utf-8') as f:
        f.write(assistant_html)
    print("Assistant HTML created.")

    # --- 3. ADD TO NAVBAR ---
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base_html = f.read()
        
    if "url_for('assistant')" not in base_html:
        old_nav = """<li class="nav-item">
          <a class="nav-link fw-medium" href="{{ url_for('shop') }}"><i class="fas fa-store me-1"></i> Shop</a>
        </li>"""
        new_nav = """<li class="nav-item">
          <a class="nav-link fw-medium" href="{{ url_for('shop') }}"><i class="fas fa-store me-1"></i> Shop</a>
        </li>
        <li class="nav-item">
          <a class="nav-link fw-medium text-success" href="{{ url_for('assistant') }}"><i class="fas fa-robot me-1"></i> AI Assistant</a>
        </li>"""
        base_html = base_html.replace(old_nav, new_nav)
        
        with open('templates/base.html', 'w', encoding='utf-8') as f:
            f.write(base_html)
        print("Navbar updated with Assistant link.")

if __name__ == '__main__':
    build_chatbot()
