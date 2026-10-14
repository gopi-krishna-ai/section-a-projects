import os
import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import urllib.parse
import concurrent.futures
from app import app
from models import db, Product

CATEGORY = "Fitness & Yoga"
PRODUCTS = [
    ("Cork Yoga Mat", 2499, "yogamat"),
    ("Bamboo Jump Rope", 899, "jumprope"),
    ("Recycled Dumbbells", 3499, "dumbbells"),
    ("Rubber Resistance Bands", 1299, "resistancebands"),
    ("Organic Cotton Yoga Block", 699, "yogablock"),
    ("Eco Foam Roller", 1599, "foamroller"),
    ("Hemp Gym Towel", 499, "gymtowel"),
    ("Recycled Water Jug", 799, "waterjug"),
    ("Bamboo Balance Board", 2999, "balanceboard"),
    ("Biodegradable Mat Bag", 1199, "matbag")
]

def download_image(name, keyword, filepath):
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
    
    # Fallback
    img = Image.new('RGB', (600, 600), color=(240, 245, 240))
    d = ImageDraw.Draw(img)
    d.rectangle([(20, 20), (580, 580)], outline=(100, 200, 100), width=5)
    d.text((100, 300), f"IMAGE FOR: {name}", fill=(50, 100, 50))
    img.save(filepath)
    return False

def add_products():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, 'static', 'images', 'catalog')
    os.makedirs(img_dir, exist_ok=True)
    
    with app.app_context():
        tasks = []
        
        existing_count = Product.query.count()
        product_count = existing_count + 1
        
        for name, price, keyword in PRODUCTS:
            img_filename = f"fitness_{keyword}_{product_count}.jpg"
            img_path = os.path.join(img_dir, img_filename)
            
            tasks.append({
                'id': f"PROD_{product_count:04d}",
                'name': name,
                'price': price,
                'keyword': keyword,
                'img_filename': img_filename,
                'img_path': img_path
            })
            product_count += 1
            
        print("Starting threaded image downloads...")
        def fetch_img(t):
            download_image(t['name'], t['keyword'], t['img_path'])
            return t
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(fetch_img, tasks)
            
        print("Inserting into DB...")
        for t in tasks:
            img_url = f"/static/images/catalog/{t['img_filename']}?v=4"
            p = Product(
                id=t['id'],
                name=t['name'],
                category=CATEGORY,
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
        print("Successfully added 10 Fitness products with local images!")

if __name__ == "__main__":
    add_products()
