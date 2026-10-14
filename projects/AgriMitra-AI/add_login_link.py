import re

with open('templates/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

admin_link = '<div style="margin-top: 20px; text-align: center;"><a href="/admin/login" style="color: #6b7280; text-decoration: none; font-size: 13px; transition: color 0.3s;"><i class="fa-solid fa-shield-halved"></i> Admin Portal</a></div>'

if 'Admin Portal' not in content:
    # Append the link right before the closing div of the login-card
    content = re.sub(r'</form>\s*</div>\s*</div>', '</form>\n' + admin_link + '\n</div>\n</div>', content)
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write(content)
print("Link added successfully.")
