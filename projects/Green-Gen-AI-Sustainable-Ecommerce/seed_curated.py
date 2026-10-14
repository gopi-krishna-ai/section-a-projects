import os
from app import app
from models import db, User, Product

# Precise mapping of 5 base products per category with EXACT matching Unsplash IDs and realistic base prices
BASE_CATALOG = {
    "Electronics": [
        {"base_name": "Eco Smart Watch", "img_id": "1550009158-9a1f108253a6", "base_price": 4999},
        {"base_name": "Wireless Headphones", "img_id": "1505740420928-5e560c06d30e", "base_price": 1999},
        {"base_name": "Refurbished Smartphone", "img_id": "1511707171634-5f897ff02aa9", "base_price": 12999},
        {"base_name": "Eco Laptop Stand", "img_id": "1527443154391-42bff736d0e1", "base_price": 899},
        {"base_name": "Bluetooth Speaker", "img_id": "1608043152269-7b010b25d2c2", "base_price": 2499}
    ],
    "Personal Care": [
        {"base_name": "Bamboo Toothbrush", "img_id": "1600180583258-6d9bde19fd21", "base_price": 199},
        {"base_name": "Natural Soap Bar", "img_id": "1600857544200-b2f666a9a2a7", "base_price": 299},
        {"base_name": "Organic Shampoo", "img_id": "1535585209827-a1a7a2dfb426", "base_price": 450},
        {"base_name": "Eco Cotton Swabs", "img_id": "1626296181977-848e42fba5af", "base_price": 150},
        {"base_name": "Natural Body Lotion", "img_id": "1556228578-0d85b1a4d571", "base_price": 399}
    ],
    "Bags": [
        {"base_name": "Canvas Tote Bag", "img_id": "1544816155105-01e4a1fa6252", "base_price": 499},
        {"base_name": "Recycled Backpack", "img_id": "1553062407-98eeb64c6a62", "base_price": 1499},
        {"base_name": "Vegan Messenger Bag", "img_id": "1590874103328-eaac2bea4214", "base_price": 2999},
        {"base_name": "Upcycled Duffle Bag", "img_id": "1550346387-9bb329b3664d", "base_price": 2499},
        {"base_name": "Cork Handbag", "img_id": "1584916201218-f4242ceb4809", "base_price": 1999}
    ],
    "Accessories": [
        {"base_name": "Bamboo Sunglasses", "img_id": "1511499767150-a48a237f0083", "base_price": 999},
        {"base_name": "Wooden Watch", "img_id": "1524805452296-608b49e6fbc1", "base_price": 1999},
        {"base_name": "Cork Wallet", "img_id": "1625902029377-506e6761fa34", "base_price": 799},
        {"base_name": "Organic Cotton Scarf", "img_id": "1606503153289-53600f7236d8", "base_price": 499},
        {"base_name": "Recycled Material Belt", "img_id": "1624233772836-829d5b0c9f13", "base_price": 599}
    ],
    "Stationery": [
        {"base_name": "Recycled Notebook", "img_id": "1517842645767-0639046229ea", "base_price": 299},
        {"base_name": "Bamboo Pens", "img_id": "1586075010923-2dd4570fb338", "base_price": 149},
        {"base_name": "Eco Sticky Notes", "img_id": "1580582236940-b74c2e6f4df3", "base_price": 99},
        {"base_name": "Wooden Desk Organizer", "img_id": "1523450001312-faa4e2fbc137", "base_price": 499},
        {"base_name": "Plantable Pencils", "img_id": "1503719812480-a6d1a63f350b", "base_price": 129}
    ],
    "Kitchen": [
        {"base_name": "Coconut Shell Bowl", "img_id": "1556910115-460d3fc6b16d", "base_price": 399},
        {"base_name": "Bamboo Cutlery", "img_id": "1583847268964-b28ce7f4df8c", "base_price": 299},
        {"base_name": "Glass Storage Jars", "img_id": "1602143400508-3cb7217965be", "base_price": 599},
        {"base_name": "Wooden Cutting Board", "img_id": "1598904712423-da6fbdccda86", "base_price": 899},
        {"base_name": "Stainless Water Bottle", "img_id": "1600860551061-3a137fc36737", "base_price": 799}
    ]
}

# Variations to expand 5 products to 20 per category
VARIATIONS = [
    {"suffix": "Classic", "price_mod": 0, "eco_mod": 80},
    {"suffix": "Pro", "price_mod": 500, "eco_mod": 85},
    {"suffix": "Lite", "price_mod": -100, "eco_mod": 75},
    {"suffix": "Premium Edition", "price_mod": 1000, "eco_mod": 95}
]

def seed_db():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        
        # Add Users
        users = [
            User(username='alice', name='Alice (Eco-Conscious)', green_points=120, persona='Eco-friendly', is_admin=False),
            User(username='bob', name='Bob (Tech Lover)', green_points=50, persona='Electronics lover', is_admin=False),
            User(username='carol', name='Carol (Fashionista)', green_points=300, persona='Sustainable fashion', is_admin=False),
            User(username='admin', name='Admin User', green_points=0, persona='System Administrator', is_admin=True)
        ]
        db.session.add_all(users)
        
        product_count = 1
        for category, base_items in BASE_CATALOG.items():
            for item in base_items:
                for var in VARIATIONS:
                    # Construct precise product
                    name = f"{item['base_name']} - {var['suffix']}"
                    price = item['base_price'] + var['price_mod']
                    
                    # Ensure price doesn't drop too low for cheap items
                    if price < 50:
                        price = item['base_price']
                        
                    eco_score = var['eco_mod']
                    img_url = f"https://images.unsplash.com/photo-{item['img_id']}?auto=format&fit=crop&q=80&w=600"
                    
                    p = Product(
                        id=f"PROD_{product_count:04d}",
                        name=name,
                        category=category,
                        material_type="Eco-Friendly Material",
                        recycled_content_pct=80.0,
                        recyclability_pct=90.0,
                        manufacturing_process="Sustainable",
                        packaging_type="Recycled Cardboard",
                        packaging_recyclable_pct=100.0,
                        carbon_footprint_kg=1.5,
                        eco_label="Certified Green",
                        price_inr=float(price),
                        eco_score=float(eco_score),
                        image_url=img_url,
                        description=f"A premium sustainable {name.lower()} designed to minimize environmental impact without compromising quality."
                    )
                    db.session.add(p)
                    product_count += 1
                
        db.session.commit()
        print("Successfully seeded EXACT matched products with clean retail pricing!")

if __name__ == "__main__":
    seed_db()
