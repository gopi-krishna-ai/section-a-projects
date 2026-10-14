import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_nav = """<ul class="navbar-nav me-auto">
          <li class="nav-item"><a class="nav-link fw-medium" href="{{ url_for('index') }}">Home</a></li>
          <li class="nav-item"><a class="nav-link fw-medium" href="{{ url_for('shop') }}">Shop</a></li>
          <li class="nav-item"><a class="nav-link fw-bold" href="{{ url_for('recommendations') }}" style="color: #F59E0B !important;"><i class="fas fa-sparkles"></i> AI Recommendations</a></li>
          <li class="nav-item"><a class="nav-link fw-bold text-success ms-2" href="{{ url_for('assistant') }}"><i class="fas fa-robot"></i> AI Chatbot</a></li>
          <li class="nav-item"><a class="nav-link fw-bold text-primary ms-2" href="{{ url_for('history') }}"><i class="fas fa-history"></i> AI History</a></li>
        </ul>"""

html = re.sub(r'<ul class="navbar-nav me-auto">.*?</ul>', new_nav, html, flags=re.DOTALL)

# Remove the ones from the dropdown to avoid duplicates
html = re.sub(r'<li><a class="dropdown-item py-2" href="\{\{ url_for\(\'history\'\) \}\}">.*?</a></li>', '', html)

# And remove the assistant link if it was added elsewhere
html = re.sub(r'<li class="nav-item">\s*<a class="nav-link fw-medium text-success" href="\{\{ url_for\(\'assistant\'\) \}\}">.*?</a>\s*</li>', '', html)
html = re.sub(r'<li class="nav-item">\s*<a class="nav-link fw-medium" href="\{\{ url_for\(\'shop\'\) \}\}">.*?</a>\s*</li>', '', html)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
