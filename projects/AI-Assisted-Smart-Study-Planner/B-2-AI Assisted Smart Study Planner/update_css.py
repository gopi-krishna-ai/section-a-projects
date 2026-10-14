import re

with open('static/css/style.css', 'r') as f:
    css = f.read()

# Add body background
css = re.sub(r'body\s*{[^}]+}', 
    '''body {
    margin: 0;
    font-family: Inter, "Segoe UI", Arial, sans-serif;
    background: url('../bg.jpg') no-repeat center center fixed;
    background-size: cover;
    color: var(--text);
}''', css)

# Fix topbar
css = re.sub(r'\.topbar\s*{[^}]+}', 
    '''.topbar {
    color: white;
    padding: 26px 32px;
    background: rgba(23, 37, 84, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255,255,255,0.2);
}''', css)

# Make panels glass
css = re.sub(r'\.panel\s*{[^}]+}', 
    '''.panel {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 32px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.6);
}''', css)

# Make stat-card glass
css = re.sub(r'\.stat-card\s*{[^}]+}', 
    '''.stat-card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.6);
}''', css)

# Make session-card inside grid look clear
css = re.sub(r'\.session-card\s*{[^}]+}', 
    '''.session-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    font-size: 13px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}''', css)

# Subject card
css = re.sub(r'\.subject-card\s*{[^}]+}', 
    '''.subject-card {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
}''', css)

with open('static/css/style.css', 'w') as f:
    f.write(css)
print("Done")
