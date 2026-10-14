import os

for file in ['templates/index.html', 'templates/assistant.html']:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update nav links to point to dashboard correctly
    content = content.replace('href="/">Dashboard</a>', 'href="/dashboard">Dashboard</a>')
    
    # Add Logout button
    if 'href="/logout"' not in content:
        content = content.replace(
            '''            <span class="navbar-text text-secondary fw-bold d-none d-lg-block">
                Intelligent Disaster Relief
            </span>''',
            '''            <div class="d-flex ms-auto">
                <a href="/logout" class="btn btn-outline-danger btn-sm fw-bold">Logout</a>
            </div>'''
        )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
