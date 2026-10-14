from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='citizen') # 'citizen' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    applications = db.relationship('Application', backref='applicant', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(64), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_type = db.Column(db.String(50)) # Aadhaar, PAN, etc.
    status = db.Column(db.String(50), default='Draft') # Draft, Pending Review, Needs Correction, Approved, Rejected, Completed
    current_step = db.Column(db.Integer, default=1)
    completion_percentage = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    submitted_at = db.Column(db.DateTime)
    
    # Form data (stored as JSON for flexibility in this prototype)
    form_data = db.Column(db.Text, default='{}') 
    
    documents = db.relationship('Document', backref='application', lazy='dynamic')
    validation_results = db.relationship('ValidationResult', backref='application', lazy='dynamic')

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    document_type = db.Column(db.String(50))
    file_path = db.Column(db.String(256))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ocr_results = db.relationship('OCRResult', backref='document', uselist=False)

class OCRResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    extracted_text = db.Column(db.Text)
    extracted_fields = db.Column(db.Text) # JSON mapping
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ValidationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('application.id'))
    field_name = db.Column(db.String(50))
    form_value = db.Column(db.String(256))
    ocr_value = db.Column(db.String(256))
    status = db.Column(db.String(20)) # Match, Mismatch
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

