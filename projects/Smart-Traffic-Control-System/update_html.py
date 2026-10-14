import os
import re

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\TrafficControlSystem'
html_path = os.path.join(base_dir, 'templates', 'dashboard.html')

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add a placeholder for ML prediction in the Analytics tab
old_analytics_html = '''<p style="font-size:24px; font-weight:bold; color:var(--accent);">Detected: <span id="vehicleCount">0</span> Vehicles</p>'''
new_analytics_html = '''<p style="font-size:24px; font-weight:bold; color:var(--accent);">Detected: <span id="vehicleCount">0</span> Vehicles</p>
                    <p style="font-size:18px; font-weight:bold; color:#10b981; margin-top:10px;">🧠 ML Optimal Green Light Time: <span id="mlOptimalTime">Waiting...</span></p>'''

content = content.replace(old_analytics_html, new_analytics_html)

# Update the JavaScript to populate it
old_js = '''                document.getElementById('vehicleCount').innerText = data.count;
                document.getElementById('processedImage').src = data.image;'''
new_js = '''                document.getElementById('vehicleCount').innerText = data.count;
                document.getElementById('processedImage').src = data.image;
                if (document.getElementById('mlOptimalTime') && data.ml_optimal_time) {
                    document.getElementById('mlOptimalTime').innerText = data.ml_optimal_time;
                }'''

content = content.replace(old_js, new_js)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

