import os

files = ['templates/login.html', 'templates/register.html']
for filepath in files:
    try:
        # Read the file ignoring bad bytes just to get the content
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
        
        # Replace the weird bullet points with asterisks
        content = content.replace('••••••••', '********')
        # Just to be safe, replace any other weird characters
        content = content.replace('â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢', '********')
        content = content.replace('\x95', '*')
        
        # Rewrite cleanly in utf-8
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error on {filepath}: {e}")
