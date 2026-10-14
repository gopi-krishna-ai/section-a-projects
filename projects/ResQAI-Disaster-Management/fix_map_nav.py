import os

files = ['templates/index.html', 'templates/assistant.html', 'templates/landing.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the old and new nav list sections
    # It's safer to just replace the specific ul block, or append the map list item
    
    if '<a class="nav-link" href="/map"' not in content and '<a class="nav-link fw-bold text-secondary" href="/map"' not in content:
        # We need to insert the map link right after the assistant link
        # Look for the assistant link end tag </li>
        
        target = 'href="/assistant"><i class="fa-solid fa-robot me-1"></i> Web Verification Assistant</a>\n                    </li>'
        target_alt = 'href="/assistant"><i class="fa-solid fa-robot me-1"></i> Web Assistant</a>\n                    </li>'
        
        insert = '''
                    <li class="nav-item">
                        <a class="nav-link fw-bold text-secondary" href="/map"><i class="fa-solid fa-earth-americas me-1"></i> Global Map</a>
                    </li>'''
                    
        if target in content:
            content = content.replace(target, target + insert)
        elif target_alt in content:
            content = content.replace(target_alt, target_alt + insert)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
