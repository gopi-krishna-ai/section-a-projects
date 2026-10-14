import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    content = f.read()
if 'admin: "/admin"' not in content:
    content = content.replace('profile: "/profile",', 'profile: "/profile",\n        admin: "/admin",')
    with open('static/js/common.js', 'w', encoding='utf-8') as f:
        f.write(content)

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

admin_li = """
            {% if current_user and current_user.userid == 'admin' %}
            <li data-page="admin" role="button" tabindex="0">
                <i class="fa-solid fa-screwdriver-wrench"></i>
                <span id="menuAdmin">Admin Panel</span>
            </li>
            {% endif %}
            <li data-page="logout" role="button" tabindex="0">
"""
if 'data-page="admin"' not in html:
    html = html.replace('<li data-page="logout" role="button" tabindex="0">', admin_li)
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
