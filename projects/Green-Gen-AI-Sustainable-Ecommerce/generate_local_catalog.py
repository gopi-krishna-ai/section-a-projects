import os
import random
import time
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from app import app
from models import db, User, Product

# Define 20 distinct products for each category
PRODUCTS = {
    "Electronics": [
        ("Solar Power Bank", 1999, "powerbank"),
        ("Bamboo Keyboard", 2499, "keyboard"),
        ("Refurbished Smartphone", 14999, "smartphone"),
        ("Eco Headphones", 1499, "headphones"),
        ("Smart Watch", 4999, "smartwatch"),
        ("Wooden Speaker", 2999, "speaker"),
        ("Solar Calculator", 499, "calculator"),
        ("Recycled Flash Drive", 899, "usb"),
        ("Biodegradable Phone Case", 599, "phonecase"),
        ("Energy Router", 3499, "router"),
        ("Smart Thermostat", 6999, "thermostat"),
        ("Solar Charger", 1299, "charger"),
        ("Laptop Stand", 999, "laptopstand"),
        ("Bamboo Mouse", 1199, "mouse"),
        ("Wind-up Radio", 1599, "radio"),
        ("Eco Smart Plug", 799, "plug"),
        ("Crank Flashlight", 699, "flashlight"),
        ("Solar Outdoor Light", 2199, "light"),
        ("LED Bulb", 299, "bulb"),
        ("E-Ink Tablet", 12999, "tablet")
    ],
    "Personal Care": [
        ("Bamboo Toothbrush", 149, "toothbrush"),
        ("Natural Deodorant", 399, "deodorant"),
        ("Solid Shampoo", 450, "shampoo"),
        ("Organic Cotton Swabs", 120, "cottonswabs"),
        ("Vegan Lip Balm", 199, "lipbalm"),
        ("Menstrual Cup", 899, "menstrualcup"),
        ("Reusable Makeup Pads", 299, "makeup"),
        ("Natural Soap", 250, "soap"),
        ("Biodegradable Floss", 180, "floss"),
        ("Loofah Sponge", 150, "loofah"),
        ("Wooden Comb", 199, "comb"),
        ("Organic Body Wash", 599, "bodywash"),
        ("Vegan Hand Cream", 450, "lotion"),
        ("Natural Sunscreen", 650, "sunscreen"),
        ("Reusable Razor", 899, "razor"),
        ("Organic Face Serum", 1200, "serum"),
        ("Eco Cotton Balls", 99, "cotton"),
        ("Bath Salts", 350, "bath"),
        ("Essential Oil Set", 999, "oil"),
        ("Bamboo Hairbrush", 399, "hairbrush")
    ],
    "Bags": [
        ("Canvas Tote", 499, "tote"),
        ("Recycled Backpack", 1499, "backpack"),
        ("Vegan Messenger", 2499, "messengerbag"),
        ("Upcycled Duffle", 1999, "duffle"),
        ("Cork Handbag", 2999, "handbag"),
        ("Hemp Laptop Sleeve", 999, "sleeve"),
        ("Jute Shopper", 399, "shopper"),
        ("Cotton Drawstring", 299, "drawstring"),
        ("Recycled Gym Bag", 1299, "gymbag"),
        ("Vegan Briefcase", 3499, "briefcase"),
        ("Leather Wallet", 899, "wallet"),
        ("Ocean Plastic Bag", 1599, "bag"),
        ("Organic Fanny Pack", 699, "fannypack"),
        ("Nylon Crossbody", 1199, "crossbody"),
        ("Bamboo Woven Bag", 1899, "wovenbag"),
        ("Upcycled Denim Tote", 799, "denim"),
        ("Canvas Satchel", 1499, "satchel"),
        ("Cork Clutch", 1299, "clutch"),
        ("Hemp Sling Bag", 999, "slingbag"),
        ("Reusable Produce Bag", 199, "producebag")
    ],
    "Accessories": [
        ("Bamboo Sunglasses", 999, "sunglasses"),
        ("Wooden Watch", 1999, "watch"),
        ("Cork Belt", 699, "belt"),
        ("Recycled Silver Ring", 1499, "ring"),
        ("Organic Scarf", 599, "scarf"),
        ("Hemp Beanie", 499, "beanie"),
        ("Copper Bracelet", 899, "bracelet"),
        ("Vegan Gloves", 799, "gloves"),
        ("Upcycled Tie", 599, "tie"),
        ("Stone Pendant", 1299, "pendant"),
        ("Brass Necklace", 1599, "necklace"),
        ("Glass Earrings", 699, "earrings"),
        ("Cork Cap", 450, "cap"),
        ("Bamboo Watch Strap", 399, "strap"),
        ("Vegan Keychain", 199, "keychain"),
        ("Canvas Hat", 550, "hat"),
        ("Hemp Wallet", 650, "wallet"),
        ("Plastic Sunglasses", 899, "sunglasses"),
        ("Wool Mittens", 699, "mittens"),
        ("Cotton Socks", 250, "socks")
    ],
    "Stationery": [
        ("Recycled Notebook", 299, "notebook"),
        ("Bamboo Pen", 149, "pen"),
        ("Seed Pencils", 199, "pencil"),
        ("Eco Sticky Notes", 99, "notes"),
        ("Wooden Ruler", 79, "ruler"),
        ("Cork Mousepad", 399, "mousepad"),
        ("Stone Journal", 499, "journal"),
        ("Wheat Pen", 129, "pen"),
        ("Paperclips", 89, "paperclips"),
        ("Recycled Eraser", 49, "eraser"),
        ("Pencil Case", 299, "case"),
        ("Bamboo Stapler", 499, "stapler"),
        ("Soy Markers", 350, "markers"),
        ("Plantable Cards", 199, "card"),
        ("Desk Organizer", 699, "organizer"),
        ("Eco Glue Stick", 99, "glue"),
        ("Leather Sketchbook", 899, "sketchbook"),
        ("Cork Desk Mat", 799, "deskmat"),
        ("Highlighter", 120, "highlighter"),
        ("Magazine Pencils", 150, "pencil")
    ],
    "Kitchen": [
        ("Coconut Bowl", 399, "bowl"),
        ("Bamboo Cutlery", 299, "cutlery"),
        ("Silicone Bags", 499, "silicone"),
        ("Steel Straws", 199, "straw"),
        ("Beeswax Wrap", 350, "wrap"),
        ("Glass Jars", 599, "jar"),
        ("Wooden Board", 899, "board"),
        ("Compost Bin", 1299, "bin"),
        ("Cast Iron Pan", 2499, "pan"),
        ("Coffee Pods", 499, "coffee"),
        ("Bamboo Brush", 199, "brush"),
        ("Cotton Towel", 250, "towel"),
        ("Ceramic Dish", 799, "dish"),
        ("Steel Water Bottle", 899, "bottle"),
        ("Copper Mug", 599, "mug"),
        ("Tea Infuser", 299, "tea"),
        ("Bamboo Steamer", 699, "steamer"),
        ("Silicone Mat", 450, "mat"),
        ("French Press", 1499, "frenchpress"),
        ("Glass Tumbler", 399, "tumbler")
    ]
}

import urllib.parse

def download_image(name, keyword, filepath):
    # Use Pollinations AI to generate a highly specific, realistic e-commerce product photo
    prompt = f"Professional e-commerce studio photography of {name}, white background, high resolution, product shot"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=600&nologo=true"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(filepath)
            return True
    except Exception as e:
        print(f"Failed to download image for {name}: {e}")
    
    # Fallback to a plain color with larger text if AI generation fails
    img = Image.new('RGB', (600, 600), color=(240, 245, 240))
    d = ImageDraw.Draw(img)
    # Since we can't easily load custom fonts, we'll draw a nice border and just put text
    d.rectangle([(20, 20), (580, 580)], outline=(100, 200, 100), width=5)
    d.text((100, 300), f"IMAGE FOR: {name}", fill=(50, 100, 50))
    img.save(filepath)
    return False

import concurrent.futures

def seed_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, 'static', 'images', 'catalog')
    os.makedirs(img_dir, exist_ok=True)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        users = [
            User(username='alice', name='Alice (Eco-Conscious)', green_points=120, persona='Eco-friendly', is_admin=False),
            User(username='bob', name='Bob (Tech Lover)', green_points=50, persona='Electronics lover', is_admin=False),
            User(username='carol', name='Carol (Fashionista)', green_points=300, persona='Sustainable fashion', is_admin=False),
            User(username='admin', name='Admin User', green_points=0, persona='System Administrator', is_admin=True)
        ]
        db.session.add_all(users)
        
        # Prepare list of tasks
        tasks = []
        product_count = 1
        for category, items in PRODUCTS.items():
            for name, price, keyword in items:
                img_filename = f"{category.lower().replace(' ', '_')}_{keyword}_{product_count}.jpg"
                img_path = os.path.join(img_dir, img_filename)
                
                tasks.append({
                    'id': f"PROD_{product_count:04d}",
                    'name': name,
                    'category': category,
                    'price': price,
                    'keyword': keyword,
                    'img_filename': img_filename,
                    'img_path': img_path
                })
                product_count += 1
                
        # Download images concurrently
        print("Starting threaded image downloads...")
        def fetch_img(t):
            # Always download new AI images to overwrite the old placeholders
            download_image(t['name'], t['keyword'], t['img_path'])
            return t
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(fetch_img, tasks)
            
        # Add to DB
        print("Inserting into DB...")
        for t in tasks:
            img_url = f"/static/images/catalog/{t['img_filename']}"
            p = Product(
                id=t['id'],
                name=t['name'],
                category=t['category'],
                material_type="Eco-Friendly Material",
                recycled_content_pct=random.uniform(50, 100),
                recyclability_pct=random.uniform(60, 100),
                manufacturing_process="Sustainable",
                packaging_type="Recycled Cardboard",
                packaging_recyclable_pct=100.0,
                carbon_footprint_kg=round(random.uniform(0.5, 5.0), 1),
                eco_label="Certified Green",
                price_inr=float(t['price']),
                eco_score=float(random.uniform(70, 99)),
                image_url=img_url,
                description=f"A premium sustainable {t['name'].lower()} designed to minimize environmental impact without compromising quality."
            )
            db.session.add(p)
                
        db.session.commit()
        print("Successfully seeded 120 DISTINCT products with local images!")

if __name__ == "__main__":
    seed_db()
