import pandas as pd
import ast, os, requests, random, concurrent.futures
from PIL import Image
from io import BytesIO
from app import app
from models import db, Product

csv_path = r'C:\Users\krish\Downloads\archive\flipkart_com-ecommerce_sample.csv'
df = pd.read_csv(csv_path)

df['top_category'] = df['product_category_tree'].dropna().apply(lambda x: x.split('>>')[0][2:-1].strip())
clothing_df = df[df['top_category'] == 'Clothing'].head(15)

app.app_context().push()

Product.query.delete()
db.session.commit()
print('Old products wiped.')

base_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(base_dir, 'static', 'images', 'catalog')
os.makedirs(img_dir, exist_ok=True)

def download_and_insert(row_tuple):
    idx, row = row_tuple
    try:
        img_urls = ast.literal_eval(row['image'])
        if not img_urls: return None
        img_url = img_urls[0]
        
        headers = {'User-Agent': 'Mozilla/5.0'}
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
        desc = str(desc)[:500]
        
        return {
            'id': f'PROD_{idx:04d}',
            'name': pname[:100],
            'category': 'Clothing',
            'price': float(price),
            'desc': desc,
            'image_url': f'/static/images/catalog/{filename}?v=1'
        }
    except Exception as e:
        print(f"Error processing {row['product_name']}: {e}")
        return None

tasks = list(clothing_df.iterrows())
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(download_and_insert, tasks))

results = [r for r in results if r is not None]

for i, r in enumerate(results):
    p = Product(
        id=f'PROD_{i+1:04d}',
        name=r['name'],
        category=r['category'],
        material_type='Eco-Friendly Cotton',
        recycled_content_pct=random.uniform(20, 80),
        recyclability_pct=random.uniform(60, 100),
        manufacturing_process='Sustainable Weaving',
        packaging_type='Recycled Paper',
        packaging_recyclable_pct=100.0,
        carbon_footprint_kg=round(random.uniform(0.5, 3.0), 1),
        eco_label='Green Label',
        price_inr=r['price'],
        eco_score=float(random.uniform(70, 99)),
        image_url=r['image_url'],
        description=r['desc']
    )
    db.session.add(p)

db.session.commit()
print(f'Successfully imported {len(results)} products from Flipkart dataset.')
