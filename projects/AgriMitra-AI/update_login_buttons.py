import re

with open('templates/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """
        <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 15px;">
            <button id="loginBtn" onclick="login()" aria-label="Log in as User">
                <i class="fa-solid fa-user"></i> LOGIN AS USER
            </button>
            <button type="button" id="adminLoginBtn" onclick="window.location.href='/admin/login'" aria-label="Log in as Admin" style="background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                <i class="fa-solid fa-shield-halved"></i> LOGIN AS ADMIN
            </button>
        </div>
"""

# Replace the single LOGIN button with the dual buttons
content = re.sub(
    r'<button id="loginBtn" onclick="login\(\)" aria-label="Log in">\s*LOGIN\s*</button>',
    replacement,
    content
)

# Also let's remove the subtle "Admin Portal" link from the bottom since we now have a prominent button
content = re.sub(
    r'<div style="margin-top: 20px; text-align: center;"><a href="/admin/login".*?</a></div>',
    '',
    content,
    flags=re.DOTALL
)

with open('templates/login.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Login buttons updated successfully!')
