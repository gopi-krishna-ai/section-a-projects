import os
import re

base_dir = r'C:\Users\krish\OneDrive\Desktop\section a\01_GuardPath_AI_Updated\B-1-GuardPath AI\templates'

for filename in ['landing.html', 'login.html', 'history.html']:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove everything between <style> and </style>
    content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
