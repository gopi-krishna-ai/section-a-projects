import re

with open('static/js/common.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '"https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Various_seeds.jpg/320px-Various_seeds.jpg"', 
    '"https://placehold.co/200x200?text=Seeds+Premium"'
)
content = content.replace(
    '"https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sunflower_seeds.jpg/320px-Sunflower_seeds.jpg"', 
    '"https://placehold.co/200x200?text=Seeds+Pro"'
)
content = content.replace(
    '"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Pumpkin_seeds_in_a_bowl.jpg/320px-Pumpkin_seeds_in_a_bowl.jpg"', 
    '"https://placehold.co/200x200?text=Seeds+Standard"'
)

content = content.replace(
    '"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Fertilizer.jpg/320px-Fertilizer.jpg"', 
    '"https://placehold.co/200x200?text=Organic+Fertilizer"'
)
content = content.replace(
    '"https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Mineral_Fertilizer.JPG/320px-Mineral_Fertilizer.JPG"', 
    '"https://placehold.co/200x200?text=Mineral+Mix"'
)
content = content.replace(
    '"https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Compost_01.jpg/320px-Compost_01.jpg"', 
    '"https://placehold.co/200x200?text=Compost"'
)

# And fallback for old img that are wikipedia links in localStorage
cart_migration = """
// Migrate old cart items
cart = cart.map(item => {
    if (item.price && !item.basePrice) item.basePrice = item.price;
    if (!item.qty) item.qty = 1;
    if (!item.unit) item.unit = 'kg';
    if (item.img && item.img.includes('wikimedia')) item.img = 'https://placehold.co/200x200?text=' + encodeURIComponent(item.title);
    return item;
});
"""

content = content.replace(
    """// Migrate old cart items
cart = cart.map(item => {
    if (item.price && !item.basePrice) item.basePrice = item.price;
    if (!item.qty) item.qty = 1;
    if (!item.unit) item.unit = 'kg';
    return item;
});""",
    cart_migration
)

with open('static/js/common.js', 'w', encoding='utf-8') as f:
    f.write(content)
