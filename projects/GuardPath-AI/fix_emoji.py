import os

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI'
app_path = os.path.join(base_dir, 'app.py')

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("🚨", "***").replace("📍", "[Location]").replace("✉️", "[Message]")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)
