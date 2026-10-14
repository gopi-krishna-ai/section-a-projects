import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace chat function to integrate wikipedia for natural language answering
old_chat = '''@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '').strip()
    
    filler_words = ["what", "tell", "me", "about", "is", "there", "any", "news", "on", "happened", "in", "the", "verify", "can", "you", "search", "for", "details", "of", "a", "was", "most", "first", "half", "year", "causing"]
    
    # Check if it's a follow-up question
    is_follow_up = any(w in user_msg.lower() for w in ["what about", "how many", "who", "when", "why", "more", "details"])
    
    if is_follow_up and chat_memory['last_topic']:
        search_query = f"{chat_memory['last_topic']} {user_msg}"
        display_topic = f"{chat_memory['last_topic']} (Follow-up)"
    else:
        words = [w for w in user_msg.replace(',', '').replace('.', '').split() if w.lower() not in filler_words and len(w) > 2]
        search_query = " ".join(words[:5]) + " disaster news updates"
        display_topic = " ".join(words[:5]) if words else "the disaster"
        chat_memory['last_topic'] = " ".join(words[:5]) # Save to memory
    
    response_html = f"<strong>Conversational Analysis for:</strong> <em>{display_topic}</em><br><br>"
    
    try:
        results = DDGS().text(search_query, max_results=3)
        if not results:
            response_html += "<span class='text-warning'>I searched my live databases but couldn't find verified reports. Could you provide a more specific location or name for the disaster?</span>"
        else:
            response_html += "Here is the structured intelligence based on live reports:<br><br>"
            for i, res in enumerate(results):
                title = res.get('title', 'Unknown Title')
                url = res.get('href', '#')
                body = res.get('body', '')
                
                response_html += f"<strong>{i+1}. {title}</strong><br>"
                response_html += f"<em>Summary:</em> {body} <br>"
                response_html += f"<a href='{url}' target='_blank' class='text-primary fw-bold text-decoration-none'>[Read Full Report &rarr;]</a><br><br>"
            
            response_html += "<strong>Memory Updated:</strong> I have saved this topic to memory. You can ask follow-up questions like <em>'How many casualties?'</em> or <em>'Any updates?'</em> without restating the disaster name."
            
    except Exception as e:
        response_html = f"<span class='text-danger fw-bold'>Warning: Live search API rate limit triggered.</span><br><br>"
        response_html += f"<strong>Offline AI Memory Analysis for '{display_topic}':</strong><br>"
        response_html += f"Based on your query context, this event has triggered our offline heuristic analyzer. However, live URL verification is temporarily paused to prevent server spam.<br><br>"
        
    return jsonify({'response': response_html})'''

new_chat = '''import wikipedia

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '').strip()
    
    filler_words = ["what", "tell", "me", "about", "is", "there", "any", "news", "on", "happened", "in", "the", "verify", "can", "you", "search", "for", "details", "of", "a", "was", "most", "first", "half", "year", "causing", "explain"]
    
    is_follow_up = any(w in user_msg.lower() for w in ["what about", "how many", "who", "when", "why", "more", "details"])
    
    if is_follow_up and chat_memory.get('last_topic'):
        topic = chat_memory['last_topic']
        search_query = f"{topic} {user_msg}"
        display_topic = f"{topic} (Follow-up)"
    else:
        words = [w for w in user_msg.replace(',', '').replace('.', '').split() if w.lower() not in filler_words]
        topic = " ".join(words[:5]) if words else "the disaster"
        search_query = topic + " disaster news updates"
        display_topic = topic
        chat_memory['last_topic'] = topic
    
    response_html = ""
    
    # 1. Conversational AI Answer (via Wikipedia)
    try:
        wiki_summary = wikipedia.summary(topic, sentences=3)
        response_html += f"<strong>AI Analysis:</strong><br><span style='color: #cbd5e1;'>{wiki_summary}</span><br><br>"
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            wiki_summary = wikipedia.summary(e.options[0], sentences=2)
            response_html += f"<strong>AI Analysis:</strong><br><span style='color: #cbd5e1;'>{wiki_summary}</span><br><br>"
        except:
            pass
    except Exception:
        pass # Fallback if no definition found
    
    response_html += f"<strong>Live Intelligence Feed for:</strong> <em>{display_topic}</em><br><br>"
    
    # 2. Live Web Proof (via DuckDuckGo)
    try:
        results = DDGS().text(search_query, max_results=3)
        if not results:
            response_html += "<span class='text-warning'>I searched my live databases but couldn't find verified reports. Could you provide a more specific location or name for the disaster?</span>"
        else:
            for i, res in enumerate(results):
                title = res.get('title', 'Unknown Title')
                url = res.get('href', '#')
                body = res.get('body', '')
                
                response_html += f"<strong>{i+1}. {title}</strong><br>"
                response_html += f"<em>Summary:</em> {body} <br>"
                response_html += f"<a href='{url}' target='_blank' class='text-primary fw-bold text-decoration-none'>[Read Full Report &rarr;]</a><br><br>"
            
            response_html += "<hr><span class='text-muted' style='font-size:12px;'><strong>Memory Updated:</strong> I saved this topic. You can ask follow-ups like <em>'How many casualties?'</em>.</span>"
            
    except Exception as e:
        if not response_html:
            response_html += f"<span class='text-danger fw-bold'>Warning: Live search API rate limit triggered.</span><br><br>"
            response_html += f"<strong>Offline AI Analysis for '{display_topic}':</strong><br>"
            response_html += f"Based on your query context, this event has triggered our offline heuristic analyzer. However, live URL verification is temporarily paused to prevent server spam.<br><br>"
        else:
            response_html += f"<span class='text-muted' style='font-size:12px;'>*Live breaking news URLs are currently paused to prevent API rate limits.*</span>"
            
    return jsonify({'response': response_html})'''

content = content.replace(old_chat, new_chat)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
