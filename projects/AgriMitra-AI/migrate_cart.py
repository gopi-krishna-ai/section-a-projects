import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add migration logic to cart loading
migration_logic = """let cart = JSON.parse(localStorage.getItem('agriCart')) || [];
// Migrate old cart items
cart = cart.map(item => {
    if (item.price && !item.basePrice) item.basePrice = item.price;
    if (!item.qty) item.qty = 1;
    if (!item.unit) item.unit = 'kg';
    return item;
});
localStorage.setItem('agriCart', JSON.stringify(cart));"""

content = content.replace("let cart = JSON.parse(localStorage.getItem('agriCart')) || [];", migration_logic)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Migration logic added.")
