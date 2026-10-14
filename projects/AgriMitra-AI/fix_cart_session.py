import re

# Inject user ID in base.html
with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a global JS variable for user_id right before common.js is loaded
if 'window.USER_ID = ' not in content:
    content = content.replace('<script src="/static/js/common.js?v=4"></script>',
                              '<script>window.USER_ID = "{{ current_user.id if current_user else \'guest\' }}";</script>\n    <script src="/static/js/common.js?v=4"></script>')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update common.js to use USER_ID in CART_KEY
with open('static/js/common.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Currently it might be `let cart = JSON.parse(localStorage.getItem('agriCart')) || [];`
# Let's dynamically define getCartKey()
js_patch = """
function getCartKey() {
    return 'agriCart_' + (window.USER_ID || 'guest');
}

function saveCart() {
    localStorage.setItem(getCartKey(), JSON.stringify(cart));
    updateCartIcon();
}

function loadCart() {
    cart = JSON.parse(localStorage.getItem(getCartKey())) || [];
    updateCartIcon();
}
"""

# Find where cart is initialized
# Usually: let cart = JSON.parse(localStorage.getItem('agriCart')) || [];
js_content = re.sub(r'let cart = JSON\.parse\(localStorage\.getItem\(\'agriCart\'\)\) \|\| \[\];', 'let cart = []; loadCart();', js_content)
js_content = re.sub(r'localStorage\.setItem\(\'agriCart\'', 'localStorage.setItem(getCartKey()', js_content)
js_content = js_content.replace("localStorage.setItem('agriCart', JSON.stringify(cart));", "saveCart();")
js_content = js_content.replace("localStorage.removeItem('agriCart');", "localStorage.removeItem(getCartKey());")

if 'function getCartKey()' not in js_content:
    js_content = js_patch + "\n" + js_content

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Patched cart to be user-specific.")
