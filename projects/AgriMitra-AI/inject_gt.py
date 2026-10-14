import os

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('<body')
if idx != -1:
    end_body = html.find('>', idx) + 1
    widget = '''
<div id="google_translate_element" style="display:none;"></div>
<script type="text/javascript">
function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en', autoDisplay: false}, 'google_translate_element');
}
</script>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
'''
    html = html[:end_body] + widget + html[end_body:]
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Done")
