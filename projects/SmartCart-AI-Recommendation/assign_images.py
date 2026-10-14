import os
import random
from app import app
from backend.models import db, Product

def update_product_images():
    with app.app_context():
        products = Product.query.all()
        
        # Collect all image paths
        base_dir = os.path.join(app.root_path, 'static', 'images', 'products', 'small')
        all_images = []
        if os.path.exists(base_dir):
            for subdir in os.listdir(base_dir):
                subdir_path = os.path.join(base_dir, subdir)
                if os.path.isdir(subdir_path):
                    for img in os.listdir(subdir_path):
                        if img.endswith('.jpg') or img.endswith('.png'):
                            # Store relative path for url_for('static', filename='...')
                            all_images.append(f"images/products/small/{subdir}/{img}")
                            
        if not all_images:
            print("No images found in the extracted archive.")
            return

        print(f"Found {len(all_images)} images. Assigning to {len(products)} products...")
        
        # Shuffle images to get random ones
        random.shuffle(all_images)
        
        for i, prod in enumerate(products):
            # Assign a random image
            prod.image_url = all_images[i % len(all_images)]
            
        db.session.commit()
        print("Product images updated successfully in the database!")

if __name__ == '__main__':
    update_product_images()
