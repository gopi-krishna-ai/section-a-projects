with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<option value="te">'
if target in html:
    idx = html.find('</option>', html.find(target)) + 9
    new_options = '\n                    <option value="ta">தமிழ்</option>\n                    <option value="fr">Français</option>\n                    <option value="es">Español</option>'
    html = html[:idx] + new_options + html[idx:]
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated base.html')
else:
    print('Target not found')
