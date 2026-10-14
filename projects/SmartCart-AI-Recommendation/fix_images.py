import os
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
from app import app
from backend.models import db, Product

def fix_images():
    with app.app_context():
        products = Product.query.all()
        for p in products:
            # Use picsum seed to guarantee a unique, working photo for every single product
            p.image_url = f"https://picsum.photos/seed/{p.id + 1000}/500/500"
            
        db.session.commit()
        print("Fixed all images using Picsum Photos!")

if __name__ == '__main__':
    fix_images()
