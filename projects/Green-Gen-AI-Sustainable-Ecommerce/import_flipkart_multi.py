import pandas as pd
import ast, os, requests, random, concurrent.futures
from PIL import Image
from io import BytesIO
from app import app
from models import db, Product

csv_path = r'C:\Users\krish\Downloads\archive\flipkart_com-ecommerce_sample.csv'
df = pd.read_csv(csv_path)

df['top_category'] = df['product_category_tree'].dropna().apply(lambda x: x.split('>>')[0][2:-1].strip())

target_categories = [
    'Clothing',
    'Footwear',
    'Home Decor & Festive Needs',
    'Beauty and Personal Care',
    'Computers',
    'Kitchen & Dining',
    'Toys & School Supplies',
    'Watches'
]

app.app_context().push()

Product.query.delete()
db.session.commit()
print('Old products wiped.')

base_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(base_dir, 'static', 'images', 'catalog')
os.makedirs(img_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

def process_row(row):
    try:
        img_urls = ast.literal_eval(row['image'])
        if not img_urls: return None
        img_url = img_urls[0]
        
        resp = requests.get(img_url, headers=headers, timeout=10)
        if resp.status_code != 200: return None
        
        img = Image.open(BytesIO(resp.content))
        if img.mode != 'RGB': img = img.convert('RGB')
        
        width, height = img.size
        min_dim = min(width, height)
        img = img.crop(((width-min_dim)/2, (height-min_dim)/2, (width+min_dim)/2, (height+min_dim)/2))
        img = img.resize((600, 600))
        
        uid = row['uniq_id']
        filename = f'flipkart_{uid}.jpg'
        filepath = os.path.join(img_dir, filename)
        img.save(filepath, format='JPEG', quality=85)
        
        price = row['retail_price'] if not pd.isna(row['retail_price']) else random.uniform(499, 2999)
        pname = row['product_name']
        desc = row['description'] if not pd.isna(row['description']) else f'High quality {pname}.'
        
        return {
            'id': uid,
            'name': pname[:100],
            'category': row['top_category'],
            'price': float(price),
            'desc': str(desc)[:500],
            'image_url': f'/static/images/catalog/{filename}'
        }
    except Exception as e:
        return None

global_idx = 1
for cat in target_categories:
    print(f'Processing category: {cat}...')
    cat_df = df[df['top_category'] == cat].dropna(subset=['image'])
    
    # Shuffle to get random items, not just the first chunk
    cat_df = cat_df.sample(frac=1, random_state=42)
    
    # Deduplicate by first two words to avoid identical variations
    seen_prefixes = set()
    unique_rows = []
    for _, row in cat_df.iterrows():
        prefix = ' '.join(str(row['product_name']).split()[:2]).lower()
        if prefix not in seen_prefixes:
            seen_prefixes.add(prefix)
            unique_rows.append(row)
            if len(unique_rows) >= 60:
                break
                
    cat_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for res in executor.map(process_row, unique_rows):
            if res is not None:
                cat_results.append(res)
            if len(cat_results) >= 15: # 15 unique products per category
                break
                
    for r in cat_results[:15]:
        p = Product(
            id=f'PROD_{global_idx:04d}',
            name=r['name'],
            category=r['category'],
            material_type='Eco-Friendly Material',
            recycled_content_pct=random.uniform(20, 80),
            recyclability_pct=random.uniform(60, 100),
            manufacturing_process='Sustainable Production',
            packaging_type='Recycled Packaging',
            packaging_recyclable_pct=100.0,
            carbon_footprint_kg=round(random.uniform(0.5, 3.0), 1),
            eco_label='Green Certified',
            price_inr=r['price'],
            eco_score=float(random.uniform(70, 99)),
            image_url=r['image_url'],
            description=r['desc']
        )
        db.session.add(p)
        global_idx += 1

db.session.commit()
print(f'Successfully imported {global_idx - 1} diverse products.')
