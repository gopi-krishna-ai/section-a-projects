import random
from app import create_app
from models import db, User, Item, Category, RentalRequest
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # India coordinates rough bounding box: Lat 10 to 28, Lng 70 to 88
        def get_rand_lat(): return random.uniform(12.9, 13.1) # Focused around Bangalore for realism
        def get_rand_lng(): return random.uniform(77.5, 77.7)

        # Create Admin
        admin = User(name='RentMate Admin', email='admin@rentmate.demo', password_hash=generate_password_hash('admin123'), role='ADMIN')
        db.session.add(admin)

        # Create Delivery Guy
        delivery = User(
            name='Speedy Delivery', 
            email='delivery@rentmate.demo', 
            password_hash=generate_password_hash('1234'), 
            role='DELIVERY', 
            location='Central Bangalore',
            lat=get_rand_lat(),
            lng=get_rand_lng()
        )
        db.session.add(delivery)

        # Create Renters
        renters = [
            User(name='Demo Renter 1', email='renter@rentmate.demo', password_hash=generate_password_hash('1234'), role='RENTER', location='Koramangala', lat=get_rand_lat(), lng=get_rand_lng()),
            User(name='Demo Renter 2', email='renter2@rentmate.demo', password_hash=generate_password_hash('1234'), role='RENTER', location='Indiranagar', lat=get_rand_lat(), lng=get_rand_lng()),
            User(name='Demo Renter 3', email='renter3@rentmate.demo', password_hash=generate_password_hash('1234'), role='RENTER', location='Whitefield', lat=get_rand_lat(), lng=get_rand_lng())
        ]
        db.session.add_all(renters)

        # Create Owners
        owners = [
            User(name='Arun Kumar', email='owner@rentmate.demo', password_hash=generate_password_hash('1234'), role='OWNER', location='HSR Layout', lat=get_rand_lat(), lng=get_rand_lng()),
            User(name='Priya Rentals', email='priya@rentmate.demo', password_hash=generate_password_hash('1234'), role='OWNER', location='Jayanagar', lat=get_rand_lat(), lng=get_rand_lng()),
            User(name='Rahul Home Tools', email='rahul@rentmate.demo', password_hash=generate_password_hash('1234'), role='OWNER', location='BTM Layout', lat=get_rand_lat(), lng=get_rand_lng()),
            User(name='Meena Events', email='meena@rentmate.demo', password_hash=generate_password_hash('1234'), role='OWNER', location='Electronic City', lat=get_rand_lat(), lng=get_rand_lng()),
            User(name='Kiran Sharing Hub', email='kiran@rentmate.demo', password_hash=generate_password_hash('1234'), role='OWNER', location='Indiranagar', lat=get_rand_lat(), lng=get_rand_lng())
        ]
        db.session.add_all(owners)
        db.session.commit()

        # Define seed items
        seed_items = [
            {"name": "Sony Alpha A7III Camera", "category": "Electronics", "price": 1500, "desc": "Professional full-frame mirrorless camera. Perfect for weddings and events. Comes with 24-70mm lens.", "owner_idx": 0, "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80"},
            {"name": "DJI Mavic Air 2 Drone", "category": "Electronics", "price": 2000, "desc": "4K drone with intelligent shooting modes. Includes 3 batteries and ND filters.", "owner_idx": 1, "image": "https://images.unsplash.com/photo-1579829366248-204fe8413f31?auto=format&fit=crop&w=800&q=80"},
            {"name": "JBL PartyBox 310", "category": "Party Supplies", "price": 800, "desc": "Massive 240W sound with dynamic light show. Portable with wheels.", "owner_idx": 2, "image": "https://images.unsplash.com/photo-1520151121098-963b65287515?auto=format&fit=crop&w=800&q=80"},
            {"name": "Bosch Power Drill Set", "category": "Tools", "price": 300, "desc": "Heavy duty hammer drill with 100-piece accessory kit. Great for DIY home projects.", "owner_idx": 3, "image": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=800&q=80"},
            {"name": "4-Person Camping Tent", "category": "Outdoors", "price": 400, "desc": "Weatherproof Quechua tent, sets up in 10 minutes. Includes sleeping mats.", "owner_idx": 4, "image": "https://images.unsplash.com/photo-1504280390227-3615456f93fc?auto=format&fit=crop&w=800&q=80"},
            {"name": "PlayStation 5 Console", "category": "Gaming", "price": 1000, "desc": "PS5 Disc Edition with 2 DualSense controllers and FIFA 24.", "owner_idx": 0, "image": "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?auto=format&fit=crop&w=800&q=80"},
            {"name": "Karcher Pressure Washer", "category": "Tools", "price": 600, "desc": "High pressure washer for cars, patios, and driveways. Comes with foam nozzle.", "owner_idx": 1, "image": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=800&q=80"},
            {"name": "Weber BBQ Grill", "category": "Party Supplies", "price": 900, "desc": "Premium charcoal grill for outdoor BBQ parties. Comes with grilling tools.", "owner_idx": 2, "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80"},
            {"name": "Trek Mountain Bike", "category": "Outdoors", "price": 500, "desc": "21-speed mountain bike. Perfect for weekend trails. Helmet included.", "owner_idx": 3, "image": "https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=800&q=80"},
            {"name": "Epson 4K Projector", "category": "Electronics", "price": 1200, "desc": "Home theater 4K projector. Perfect for movie nights or presentations.", "owner_idx": 4, "image": "https://images.unsplash.com/photo-1587925358603-c2eea5305bbc?auto=format&fit=crop&w=800&q=80"}
        ]
        
        items = []
        for d in seed_items:
            owner = owners[d["owner_idx"]]
            it = Item(
                owner_id=owner.id,
                category=d["category"],
                name=d["name"],
                description=d["desc"],
                price_per_day=d["price"],
                status='APPROVED',
                image_url=d["image"],
                location=owner.location,
                lat=owner.lat,
                lng=owner.lng
            )
            items.append(it)
        db.session.add_all(items)
        db.session.commit()

        # Create active rentals so the delivery guy has tasks
        rentals = [
            RentalRequest(
                renter_id=renters[0].id, owner_id=owners[0].id, item_id=items[0].id, delivery_guy_id=delivery.id,
                start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=2),
                rental_days=2, price_per_day=120, total_amount=240, status='ACTIVE', delivery_status='IN_TRANSIT'
            ),
            RentalRequest(
                renter_id=renters[1].id, owner_id=owners[1].id, item_id=items[1].id,
                start_date=datetime.utcnow(), end_date=datetime.utcnow() + timedelta(days=3),
                rental_days=3, price_per_day=150, total_amount=450, status='ACTIVE', delivery_status='PENDING_PICKUP'
            )
        ]
        db.session.add_all(rentals)
        db.session.commit()

        print("Database seeded successfully with Delivery Role and Tasks!")

if __name__ == '__main__':
    seed_database()
