import os

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

widget_html = '''
    <!-- Chatbot Widget -->
    <div id="chatbot-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; align-items: flex-end;">
        <div id="chat-window" style="display: none; width: 320px; height: 400px; background: white; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); flex-direction: column; overflow: hidden; margin-bottom: 15px;">
            <div style="background: #059669; color: white; padding: 15px; font-weight: bold; display: flex; justify-content: space-between; align-items: center;">
                <span><i class="fas fa-robot"></i> Green Gen AI</span>
                <button onclick="document.getElementById('chat-window').style.display='none'" style="background: none; border: none; color: white; cursor: pointer;"><i class="fas fa-times"></i></button>
            </div>
            <div id="chat-messages" style="flex: 1; padding: 15px; overflow-y: auto; background: #f9fafb; display: flex; flex-direction: column; gap: 10px;">
                <div style="background: #e5e7eb; padding: 10px; border-radius: 10px; border-bottom-left-radius: 0; align-self: flex-start; max-width: 85%; font-size: 0.9em; color: #1f2937;">
                    Hi! I'm the Green Gen AI. Ask me to find products to see their eco-scores and prices!
                </div>
            </div>
            <div style="padding: 10px; background: white; border-top: 1px solid #e5e7eb; display: flex;">
                <input type="text" id="chat-input" placeholder="Type a message..." style="flex: 1; padding: 8px; border: 1px solid #d1d5db; border-radius: 20px; outline: none; padding-left: 15px;" onkeypress="if(event.key === 'Enter') sendChatMessage()">
                <button onclick="sendChatMessage()" style="background: #059669; color: white; border: none; border-radius: 50%; width: 35px; height: 35px; margin-left: 10px; cursor: pointer; display: flex; justify-content: center; align-items: center;"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <button id="chat-toggle" onclick="toggleChat()" style="background: #059669; color: white; border: none; border-radius: 50%; width: 60px; height: 60px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); cursor: pointer; font-size: 1.5rem; display: flex; justify-content: center; align-items: center; transition: transform 0.2s;">
            <i class="fas fa-comment-dots"></i>
        </button>
    </div>

    <script>
        function toggleChat() {
            const win = document.getElementById('chat-window');
            if (win.style.display === 'none') {
                win.style.display = 'flex';
                document.getElementById('chat-input').focus();
            } else {
                win.style.display = 'none';
            }
        }

        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message to UI
            addChatMessage(message, 'user');
            input.value = '';
            
            // Show typing indicator
            const typingId = addChatMessage('<i class="fas fa-ellipsis-h" style="animation: blink 1s infinite;"></i>', 'bot');
            
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({query: message})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById(typingId).remove();
                addChatMessage(data.reply, 'bot', true);
            })
            .catch(err => {
                document.getElementById(typingId).remove();
                addChatMessage("Sorry, I'm having trouble connecting to the server.", 'bot');
            });
        }
        
        function addChatMessage(content, sender, isHtml = false) {
            const messages = document.getElementById('chat-messages');
            const div = document.createElement('div');
            const id = 'msg-' + Date.now();
            div.id = id;
            div.style.padding = '10px';
            div.style.borderRadius = '10px';
            div.style.maxWidth = '85%';
            div.style.fontSize = '0.9em';
            div.style.lineHeight = '1.4';
            
            if (sender === 'user') {
                div.style.background = '#059669';
                div.style.color = 'white';
                div.style.alignSelf = 'flex-end';
                div.style.borderBottomRightRadius = '0';
                if (!isHtml) div.textContent = content;
                else div.innerHTML = content;
            } else {
                div.style.background = '#e5e7eb';
                div.style.color = '#1f2937';
                div.style.alignSelf = 'flex-start';
                div.style.borderBottomLeftRadius = '0';
                if (!isHtml) div.textContent = content;
                else div.innerHTML = content;
            }
            
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
            return id;
        }
    </script>
'''

idx = html.find('</body>')
if idx != -1:
    html = html[:idx] + widget_html + html[idx:]
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected widget into base.html")
else:
    print("Could not find </body>")
