import os
import re

for root, _, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace {{ something.price_inr }} with {{ something.price_inr | int }} if it's not already there
            new_content = re.sub(r'\{\{\s*([a-zA-Z0-9_]+)\.price_inr\s*\}\}', r'{{ \1.price_inr | int }}', content)
            
            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
