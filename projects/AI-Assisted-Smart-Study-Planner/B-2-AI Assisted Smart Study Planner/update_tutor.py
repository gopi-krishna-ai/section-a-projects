import re

with open('templates/tutor.html', 'r') as f:
    html = f.read()

# Add body background
html = re.sub(r'body\s*{[^}]+}', 
    '''body {
            font-family: 'Inter', sans-serif;
            background: url('/static/bg.jpg') no-repeat center center fixed;
            background-size: cover;
            margin: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }''', html)

# Fix navbar
html = re.sub(r'\.navbar\s*{[^}]+}', 
    '''.navbar {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 1rem 2rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.6);
        }''', html)

# Fix chat container
html = re.sub(r'\.chat-container\s*{[^}]+}', 
    '''.chat-container {
            flex: 1;
            max-width: 800px;
            margin: 2rem auto;
            width: 95%;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.6);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }''', html)

# Fix input area
html = re.sub(r'\.input-area\s*{[^}]+}', 
    '''.input-area {
            display: flex;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.5);
            border-top: 1px solid rgba(255, 255, 255, 0.6);
        }''', html)

# Fix msg bubbles
html = re.sub(r'\.msg-ai\s*{[^}]+}', 
    '''.msg-ai {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(102, 126, 234, 0.3);
            align-self: flex-start;
            border-bottom-left-radius: 2px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }''', html)

html = re.sub(r'\.msg-user\s*{[^}]+}', 
    '''.msg-user {
            background: rgba(102, 126, 234, 0.9);
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }''', html)

with open('templates/tutor.html', 'w') as f:
    f.write(html)
print("Done")
