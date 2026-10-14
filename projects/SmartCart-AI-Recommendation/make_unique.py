import os
import random

os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
from app import app
from backend.models import db, Product, Category

def make_clickable():
    # 1. Update shop.html
    with open('templates/shop.html', 'r', encoding='utf-8') as f:
        shop = f.read()
    
    # Wrap image in anchor tag
    shop = shop.replace('<div class="img-wrapper">', '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="text-decoration-none"><div class="img-wrapper">')
    shop = shop.replace('</div>\n                        <div class="card-body d-flex flex-column">', '</div></a>\n                        <div class="card-body d-flex flex-column">')
    
    # Wrap title in anchor tag
    shop = shop.replace('<h5 class="card-title text-truncate">{{ prod.name }}</h5>', '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="text-decoration-none text-dark"><h5 class="card-title text-truncate hover-primary">{{ prod.name }}</h5></a>')
    
    with open('templates/shop.html', 'w', encoding='utf-8') as f:
        f.write(shop)

    # 2. Update index.html
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index = f.read()
        
    index = index.replace('<div class="img-wrapper">', '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="text-decoration-none"><div class="img-wrapper">')
    index = index.replace('</div>\n                    <div class="card-body d-flex flex-column">', '</div></a>\n                    <div class="card-body d-flex flex-column">')
    index = index.replace('<h5 class="card-title text-truncate">{{ prod.name }}</h5>', '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="text-decoration-none text-dark"><h5 class="card-title text-truncate hover-primary">{{ prod.name }}</h5></a>')
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index)

    # 3. Update recommendations.html
    with open('templates/recommendations.html', 'r', encoding='utf-8') as f:
        recs = f.read()
        
    recs = recs.replace('<div class="img-wrapper">', '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="text-decoration-none"><div class="img-wrapper">')
    recs = recs.replace('</div>\n            <div class="card-body d-flex flex-column">', '</div></a>\n            <div class="card-body d-flex flex-column">')
    recs = recs.replace('<h5 class="card-title text-truncate">{{ prod.name }}</h5>', '<a href="{{ url_for(\'product\', product_id=prod.id) }}" class="text-decoration-none text-dark"><h5 class="card-title text-truncate hover-primary">{{ prod.name }}</h5></a>')
    
    with open('templates/recommendations.html', 'w', encoding='utf-8') as f:
        f.write(recs)
        
    # Also add hover-primary CSS to base.html
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base = f.read()
    if '.hover-primary:hover' not in base:
        base = base.replace('</style>', '    .hover-primary:hover { color: var(--primary) !important; }\n    </style>')
        with open('templates/base.html', 'w', encoding='utf-8') as f:
            f.write(base)
            
    print("UI updated to be highly clickable.")

adjectives = ["Premium", "Ultra", "Smart", "Classic", "Advanced", "Elite", "Pro", "Essential", "Luxury", "Signature", "Eco-friendly", "Compact", "Heavy-Duty", "Modern", "Vintage", "Sleek"]

descriptions = [
    "Experience uncompromised quality with our latest release. Built with durable materials, it's designed to last while providing exceptional performance.",
    "A perfect blend of style and functionality. This product has been rated 5-stars by our community for its incredible ease of use.",
    "Upgrade your lifestyle with this must-have essential. Featuring cutting-edge technology and a sleek, ergonomic design.",
    "Hand-crafted with precision. This is the ultimate choice for enthusiasts who demand nothing but the absolute best.",
    "Why settle for less? This item delivers premium results without the premium price tag. Highly recommended by top experts.",
    "A revolutionary product that adapts to your needs. Lightweight, versatile, and stunningly beautiful.",
    "Discover the difference. This top-tier item offers unparalleled reliability and is backed by a 2-year comprehensive warranty.",
    "Eco-friendly and sustainably sourced. Not only does it look great, but it's also designed with the environment in mind."
]

def make_unique():
    with app.app_context():
        products = Product.query.all()
        for p in products:
            # If the name is generic like "Sports Item 4"
            if "Item" in p.name:
                adj = random.choice(adjectives)
                cat_name = p.category.name
                
                # Generate a better specific noun based on category
                nouns = {
                    "Sports": ["Tennis Racket", "Basketball", "Yoga Mat", "Dumbbells", "Running Shoes", "Treadmill", "Jump Rope", "Protein Shaker"],
                    "Electronics": ["Wireless Earbuds", "Smartwatch", "Bluetooth Speaker", "4K Monitor", "Power Bank", "Mechanical Keyboard", "Drone", "Action Camera"],
                    "Home & Kitchen": ["Air Fryer", "Blender", "Coffee Maker", "Cookware Set", "Vacuum Cleaner", "Toaster", "Microwave", "Water Purifier"],
                    "Beauty": ["Lipstick Set", "Foundation", "Mascara", "Eyeshadow Palette", "Makeup Brushes", "Highlighter", "Nail Polish", "Blush"],
                    "Personal Care": ["Hair Dryer", "Electric Shaver", "Body Wash", "Moisturizer", "Face Wash", "Trimmer", "Shampoo", "Conditioner"],
                    "Men's Wear": ["Denim Jacket", "Polo Shirt", "Chinos", "Leather Jacket", "Sneakers", "T-Shirt", "Formal Shirt", "Jeans"],
                    "Women's Wear": ["Floral Dress", "Handbag", "High Heels", "Skirt", "Blouse", "Summer Top", "Leggings", "Cardigan"],
                    "Footwear": ["Running Sneakers", "Leather Boots", "Casual Loafers", "Formal Shoes", "Sandals", "High Heels", "Slippers", "Training Shoes"],
                    "Grocery": ["Organic Honey", "Olive Oil", "Green Tea", "Almonds", "Oats", "Pasta", "Peanut Butter", "Dark Chocolate"],
                    "Kids": ["Action Figure", "Dollhouse", "RC Car", "Building Blocks", "Puzzle Set", "Board Game", "Teddy Bear", "School Bag"],
                    "Toys": ["Lego Set", "Nerf Gun", "Barbie Doll", "Hot Wheels", "Rubik's Cube", "Play-Doh", "Monopoly", "Jigsaw Puzzle"]
                }
                
                noun_list = nouns.get(cat_name, [cat_name + " Essential", cat_name + " Kit", cat_name + " Pack", cat_name + " Set", cat_name + " Gear", cat_name + " Tool"])
                noun = random.choice(noun_list)
                
                p.name = f"{adj} {noun}"
            
            # Update description regardless
            p.description = f"{p.name}: {random.choice(descriptions)} Whether you're buying it for yourself or as a gift, it is guaranteed to impress!"
            
        db.session.commit()
        print("All products now have unique names and rich descriptions!")

if __name__ == '__main__':
    make_clickable()
    make_unique()
