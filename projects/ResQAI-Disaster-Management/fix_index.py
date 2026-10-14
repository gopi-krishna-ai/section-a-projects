import os

html_path = 'templates/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add link to assistant in the navbar
old_nav = '''            <span class="navbar-text text-light">
                Intelligent Disaster Relief Management System
            </span>
        </div>
    </nav>'''

new_nav = '''            <div class="collapse navbar-collapse">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active text-primary fw-bold" href="/">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/assistant"><i class="fa-solid fa-robot me-1"></i> Web Verification Assistant</a>
                    </li>
                </ul>
            </div>
            <span class="navbar-text text-light d-none d-lg-block">
                Intelligent Disaster Relief
            </span>
        </div>
    </nav>'''

content = content.replace(old_nav, new_nav)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
