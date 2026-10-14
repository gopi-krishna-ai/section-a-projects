import os
os.environ["DISABLE_SQLALCHEMY_CEXT"] = "1"
from app import app
from backend.models import db, Product, Category

category_images = {
    "Laptops": "https://upload.wikimedia.org/wikipedia/commons/e/e9/MacBook_Pro_13%E2%80%9D_Mid_2012_Early_2015.jpg",
    "Mobiles": "https://upload.wikimedia.org/wikipedia/commons/f/fa/IPhone_5.png",
    "Men's Wear": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Blue_Tshirt.jpg/500px-Blue_Tshirt.jpg",
    "Women's Wear": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Dress_%286812833075%29.jpg/500px-Dress_%286812833075%29.jpg",
    "Sports": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Adidas_Telstar_18.jpg/500px-Adidas_Telstar_18.jpg",
    "Electronics": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Headphones_1.jpg/500px-Headphones_1.jpg",
    "Footwear": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Converse-All-Star-Shoe.jpg/500px-Converse-All-Star-Shoe.jpg",
    "Beauty": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cosmetics.jpg/500px-Cosmetics.jpg",
    "Personal Care": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Cosmetics.jpg/500px-Cosmetics.jpg",
    "Home & Kitchen": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kitchen_utensils_hanging.jpg/500px-Kitchen_utensils_hanging.jpg"
}

default_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/E-commerce_concept_with_shopping_cart.jpg/500px-E-commerce_concept_with_shopping_cart.jpg"

def update_product_images():
    with app.app_context():
        products = Product.query.all()
        categories = Category.query.all()
        cat_map = {c.id: c.name for c in categories}
        
        for p in products:
            cname = cat_map.get(p.category_id, "")
            
            # Find closest match
            matched = default_img
            for k, v in category_images.items():
                if k.lower() in cname.lower() or cname.lower() in k.lower():
                    matched = v
                    break
            
            p.image_url = matched
            
        db.session.commit()
        print("Updated images to Wikimedia Commons!")

if __name__ == '__main__':
    update_product_images()
