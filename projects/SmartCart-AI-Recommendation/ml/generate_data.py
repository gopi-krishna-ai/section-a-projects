import os
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
import sys
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add parent dir to path to import app and models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from backend.models import db, Customer, Category, Product, Interaction, Order, OrderItem

CATEGORIES = [
    "Baby & Maternity", "Snacks & Chocolates", "Men's Wear", "Women's Wear", 
    "Sports", "Electronics", "Mobiles", "Laptops", "Footwear", "Beauty", 
    "Personal Care", "Home & Kitchen", "Grocery", "Books", "Bags", 
    "Watches", "Kids", "Toys", "Fitness", "Accessories"
]

BRANDS = ["Pampers", "Cadbury", "Huggies", "Nestle", "BrandE", "SmartTech", "LifeStyle", "ProGear", "HealthPlus"]

specific_products = {
    "Baby & Maternity": [
        "Pampers Premium Care Pants (Large)", "Huggies Wonder Pants", "Johnson's Baby Powder", 
        "MamyPoko Pants", "Baby Dove Lotion", "Philips Avent Bottle", "Himalaya Baby Wipes", "Chicco Stroller"
    ],
    "Snacks & Chocolates": [
        "Cadbury Dairy Milk Silk", "Ferrero Rocher", "Lays Classic Salted", 
        "Doritos Nacho Cheese", "Snickers Bar", "KitKat Dessert Delight", "Oreo Cookies", "Pringles Original"
    ],
    "Laptops": ["MacBook Air M2", "Dell XPS 13", "Lenovo ThinkPad X1", "HP Spectre x360", "Asus ROG Zephyrus", "Acer Swift 3", "Microsoft Surface Pro", "Razer Blade 15"],
    "Mobiles": ["iPhone 15 Pro", "Samsung Galaxy S24", "Google Pixel 8", "OnePlus 12", "Xiaomi 14", "Nothing Phone 2", "Sony Xperia 1 V", "Motorola Edge"]
}

def generate_products():
    print("Generating Categories and Products...")
    cat_objs = []
    for cat_name in CATEGORIES:
        cat = Category(name=cat_name, description=f"Explore the best of {cat_name}")
        db.session.add(cat)
        cat_objs.append(cat)
    db.session.commit()

    product_objs = []
    for cat in cat_objs:
        names = specific_products.get(cat.name, [f"{cat.name} Item {i}" for i in range(1, 9)])
        for i, name in enumerate(names[:8]):
            price = round(random.uniform(5.0, 50.0), 2)
            if cat.name in ["Laptops", "Mobiles", "Electronics"]:
                price = round(random.uniform(200.0, 2000.0), 2)
            
            p = Product(
                name=name,
                category_id=cat.id,
                brand=random.choice(BRANDS),
                price=price,
                discount=round(random.choice([0, 0, 5, 10, 15, 20]), 2),
                rating=round(random.uniform(4.0, 5.0), 1),
                review_count=random.randint(50, 2000),
                description=f"Premium high-quality {name}. Specially sourced to provide the best experience.",
                stock_quantity=random.randint(20, 200),
                image_url=f"https://picsum.photos/seed/{cat.id * 100 + i}/500/500",
                tags=f"{cat.name.lower()}, popular, high-quality"
            )
            db.session.add(p)
            product_objs.append(p)
    db.session.commit()
    print(f"Generated {len(CATEGORIES)} categories and {len(product_objs)} products.")
    return cat_objs, product_objs

def generate_customers():
    print("Generating Demo Customers...")
    customers = [
        {"name": "Sports Fan (Demo 1)", "email": "demo1@smartcart.com", "pref": ["Sports", "Fitness", "Footwear"]},
        {"name": "Tech Geek (Demo 2)", "email": "demo2@smartcart.com", "pref": ["Electronics", "Mobiles", "Laptops", "Accessories"]},
        {"name": "Beauty Lover (Demo 3)", "email": "demo3@smartcart.com", "pref": ["Beauty", "Personal Care", "Women's Wear"]},
        {"name": "Busy Parent (Demo 4)", "email": "demo4@smartcart.com", "pref": ["Baby & Maternity", "Home & Kitchen", "Grocery"]}
    ]
    
    cust_objs = []
    for c in customers:
        cust = Customer(
            name=c["name"],
            email=c["email"],
            password_hash=generate_password_hash("password")
        )
        db.session.add(cust)
        cust_objs.append((cust, c["pref"]))
    db.session.commit()
    return cust_objs

def generate_history(cust_objs, cat_objs, product_objs):
    print("Generating 1-year Historical Data...")
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365)
    
    interaction_types = ['VIEW', 'VIEW', 'VIEW', 'SEARCH', 'ADD_TO_CART', 'WISHLIST', 'PURCHASE']
    
    for cust, prefs in cust_objs:
        pref_cats = [c for c in cat_objs if c.name in prefs]
        other_cats = [c for c in cat_objs if c.name not in prefs]
        
        num_interactions = random.randint(150, 250)
        current_date = start_date
        
        for _ in range(num_interactions):
            current_date += timedelta(days=random.randint(1, 4), hours=random.randint(0, 23))
            if current_date > end_date:
                break
                
            if random.random() < 0.85 and pref_cats:
                cat = random.choice(pref_cats)
            else:
                cat = random.choice(other_cats)
                
            cat_prods = [p for p in product_objs if p.category_id == cat.id]
            if not cat_prods:
                continue
                
            prod = random.choice(cat_prods)
            itype = random.choice(interaction_types)
            
            db.session.add(Interaction(
                customer_id=cust.id, product_id=prod.id, category_id=cat.id,
                interaction_type=itype, timestamp=current_date
            ))
            
            if itype == 'PURCHASE':
                order = Order(customer_id=cust.id, total_amount=prod.price, date=current_date)
                db.session.add(order)
                db.session.flush()
                db.session.add(OrderItem(order_id=order.id, product_id=prod.id, quantity=1, price=prod.price))
                
        # ---------------------------------------------------------
        # SMART BEHAVIOR: "Busy Parent" Diaper + Chocolate pattern
        # ---------------------------------------------------------
        if cust.name == "Busy Parent (Demo 4)":
            baby_cat = next((c for c in cat_objs if c.name == "Baby & Maternity"), None)
            snack_cat = next((c for c in cat_objs if c.name == "Snacks & Chocolates"), None)
            
            if baby_cat and snack_cat:
                diaper = next((p for p in product_objs if "Pampers" in p.name), None)
                chocolate = next((p for p in product_objs if "Dairy Milk" in p.name), None)
                
                if diaper and chocolate:
                    # Every month on the 10th!
                    for month_offset in range(12):
                        pat_date = start_date + timedelta(days=month_offset*30)
                        pat_date = pat_date.replace(day=10)
                        
                        # Buys Diaper
                        db.session.add(Interaction(customer_id=cust.id, product_id=diaper.id, category_id=baby_cat.id, interaction_type='PURCHASE', timestamp=pat_date))
                        # Buys Chocolate on the exact same day
                        db.session.add(Interaction(customer_id=cust.id, product_id=chocolate.id, category_id=snack_cat.id, interaction_type='PURCHASE', timestamp=pat_date))

    db.session.commit()
    print("History generation complete.")

if __name__ == '__main__':
    with app.app_context():
        print("Dropping existing tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        
        cat_objs, prod_objs = generate_products()
        cust_objs = generate_customers()
        generate_history(cust_objs, cat_objs, prod_objs)
        print("Demo database successfully initialized!")
