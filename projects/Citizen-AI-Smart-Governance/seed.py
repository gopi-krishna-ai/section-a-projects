from app import create_app, db
from app.models import User, Application
from datetime import datetime

app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing
        db.drop_all()
        db.create_all()
        
        # Create Admin
        admin = User(username='admin', email='admin@citizenai.demo', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create Citizen
        citizen = User(username='citizen', email='citizen@demo.com', role='citizen')
        citizen.set_password('1234')
        db.session.add(citizen)
        
        db.session.commit()
        print('Database seeded with demo users.')

if __name__ == '__main__':
    seed_data()

