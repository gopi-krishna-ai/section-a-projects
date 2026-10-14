import os

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add the map route
old_dashboard = '''@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')'''

new_dashboard_and_map = '''@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/map')
def map_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('map.html')'''

if '@app.route(\'/map\')' not in content:
    content = content.replace(old_dashboard, new_dashboard_and_map)

# Fix Wikipedia disambiguation to be more robust
content = content.replace(
'''    try:
        wiki_summary = wikipedia.summary(topic, sentences=3)
        response_html += f"<strong>AI Analysis:</strong><br><span style='color: #cbd5e1;'>{wiki_summary}</span><br><br>"
    except wikipedia.exceptions.DisambiguationError as e:''',
'''    try:
        # Instead of risking PageError, search first
        search_res = wikipedia.search(topic)
        if search_res:
            wiki_summary = wikipedia.summary(search_res[0], sentences=3)
            response_html += f"<strong>AI Analysis:</strong><br><span style='color: #cbd5e1;'>{wiki_summary}</span><br><br>"
        else:
            raise Exception("No wiki results")
    except wikipedia.exceptions.DisambiguationError as e:'''
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
