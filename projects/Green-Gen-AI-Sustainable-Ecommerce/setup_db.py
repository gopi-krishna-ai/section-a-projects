import pandas as pd
import random
from datetime import datetime, timedelta
from app import app, db
from models import User, Product, Interaction, Order, OrderItem, RecyclingRequest

def create_demo_data():
    with app.app_context():
        # Create tables
        db.create_all()

        print("Tables created.")

        # Check if users already exist
        if User.query.first():
            print("Database already populated.")
            return

        print("Populating database with demo data...")
        
        # 1. Load Products from CSV
        df = pd.read_csv('data/original/green_gen_ai_product_eco_dataset.csv')
        df = df.fillna('')
        
        categories = list(df['category'].unique())

        products = []
        for index, row in df.iterrows():
            product = Product(
                id=row['product_id'],
                name=f"{row['material_type']} {row['category']} - {row['product_id']}",
                category=row['category'],
                material_type=row['material_type'],
                recycled_content_pct=float(row['recycled_content_pct']) if row['recycled_content_pct'] else 0.0,
                recyclability_pct=float(row['recyclability_pct']) if row['recyclability_pct'] else 0.0,
                manufacturing_process=row['manufacturing_process'],
                energy_efficiency_score=float(row['energy_efficiency_score']) if row['energy_efficiency_score'] else 0.0,
                packaging_type=row['packaging_type'],
                packaging_recyclable_pct=float(row['packaging_recyclable_pct']) if row['packaging_recyclable_pct'] else 0.0,
                carbon_footprint_kg=float(row['carbon_footprint_kg']) if row['carbon_footprint_kg'] else 0.0,
                water_usage_liters=float(row['water_usage_liters']) if row['water_usage_liters'] else 0.0,
                durability_years=float(row['durability_years']) if row['durability_years'] else 0.0,
                price_inr=float(row['price_inr']) if row['price_inr'] else 0.0,
                eco_score=float(row['eco_score']) if row['eco_score'] else 0.0,
                eco_label=row['eco_label'],
                image_url=f"https://via.placeholder.com/300x300?text={row['category']}",
                description=f"A sustainable {row['category']} product made with {row['material_type']}."
            )
            products.append(product)
        db.session.bulk_save_objects(products)
        db.session.commit()
        print(f"Loaded {len(products)} products.")

        from werkzeug.security import generate_password_hash
        # 2. Create Demo Users and Admin
        users = [
            User(username="alice", name="Alice (Eco-Conscious)", persona="Eco-friendly", green_points=1200, password_hash=generate_password_hash("password123")),
            User(username="bob", name="Bob (Tech Lover)", persona="Electronics lover", green_points=300, password_hash=generate_password_hash("password123")),
            User(username="carol", name="Carol (Fashionista)", persona="Fashion lover", green_points=50, password_hash=generate_password_hash("password123")),
            User(username="admin", name="Admin User", persona="System Administrator", is_admin=True, password_hash=generate_password_hash("admin123"))
        ]
        db.session.add_all(users)
        db.session.commit()

        # 3. Create Interactions (For ML Training)
        # We'll make Alice interact mostly with high eco-score items
        # Bob mostly interacts with Electronics
        # Carol mostly interacts with Fashion/Bags
        
        interactions = []
        now = datetime.utcnow()

        all_products = Product.query.all()
        electronics = [p for p in all_products if p.category == 'Electronics']
        fashion_bags = [p for p in all_products if p.category in ['Bags', 'Accessories', 'Fashion', 'Personal Care']]
        eco_friendly = [p for p in all_products if p.eco_score > 75]

        def add_interaction(user, prod_list, count):
            if not prod_list: return
            for _ in range(count):
                p = random.choice(prod_list)
                t = now - timedelta(days=random.randint(1, 30))
                interactions.append(Interaction(user_id=user.id, product_id=p.id, event_type='VIEW', timestamp=t))
                if random.random() > 0.7:
                    interactions.append(Interaction(user_id=user.id, product_id=p.id, event_type='CART', timestamp=t + timedelta(minutes=5)))
                if random.random() > 0.9:
                    interactions.append(Interaction(user_id=user.id, product_id=p.id, event_type='PURCHASE', timestamp=t + timedelta(minutes=15)))
        
        add_interaction(users[0], eco_friendly, 50)
        add_interaction(users[1], electronics, 50)
        add_interaction(users[2], fashion_bags, 50)

        db.session.add_all(interactions)
        db.session.commit()
        print("Demo users and interactions created.")

if __name__ == "__main__":
    create_demo_data()
