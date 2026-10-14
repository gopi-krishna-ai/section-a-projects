import os
import sqlite3
import random
from app import app, db
from models import Product

def update_images():
    # Get all image paths
    base_dir = 'static/images/small'
    image_paths = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                # Create the relative URL path: /static/images/small/...
                # root is like 'static/images/small\00' on Windows
                rel_path = os.path.relpath(os.path.join(root, file), 'static').replace('\\', '/')
                image_paths.append(f"/static/{rel_path}")
                
    random.shuffle(image_paths)
    print(f"Found {len(image_paths)} images.")

    with app.app_context():
        products = Product.query.all()
        print(f"Updating {len(products)} products...")
        
        for i, product in enumerate(products):
            if i < len(image_paths):
                product.image_url = image_paths[i]
                
        db.session.commit()
        print("Done updating product images in the database!")

if __name__ == "__main__":
    update_images()
