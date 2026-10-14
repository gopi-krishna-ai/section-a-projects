import os
import hmac
import hashlib
import secrets
import time
from typing import Tuple, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.models import User, TopicMastery, Topic

SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "aptitude_mastery_coach_secret_2026_jwt_token")
TOKEN_EXPIRY_SECONDS = 7 * 24 * 3600 # 7 days

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return hashed, salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    if not password_hash or not salt:
        return False
    computed, _ = hash_password(password, salt)
    return secrets.compare_digest(computed, password_hash)

def create_access_token(user_id: str) -> str:
    timestamp = str(int(time.time()))
    payload = f"{user_id}:{timestamp}"
    sig = hmac.new(SECRET_KEY.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"

def verify_access_token(token: str) -> Optional[str]:
    try:
        parts = token.split(':')
        if len(parts) != 3:
            return None
        user_id, timestamp_str, sig = parts
        payload = f"{user_id}:{timestamp_str}"
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
        if not secrets.compare_digest(sig, expected_sig):
            return None
        
        # Check expiry
        timestamp = int(timestamp_str)
        if time.time() - timestamp > TOKEN_EXPIRY_SECONDS:
            return None
            
        return user_id
    except Exception:
        return None

DEMO_ACCOUNTS = [
    {
        "id": "user_rohan",
        "username": "rohan",
        "full_name": "Rohan Mistry",
        "email": "rohan@example.com",
        "password": "password123",
        "target_company": "TCS / Infosys",
        "avatar": "RM"
    },
    {
        "id": "user_priya",
        "username": "priya",
        "full_name": "Priya Sharma",
        "email": "priya@example.com",
        "password": "password123",
        "target_company": "Accenture Cognitive",
        "avatar": "PS"
    },
    {
        "id": "user_alex",
        "username": "beginner_coder",
        "full_name": "Alex Chen",
        "email": "alex@example.com",
        "password": "password123",
        "target_company": "Cognizant GenC",
        "avatar": "AC"
    },
    {
        "id": "default_user",
        "username": "learner",
        "full_name": "Demo Learner",
        "email": "learner@example.com",
        "password": "password123",
        "target_company": "TCS / Infosys",
        "avatar": "DL"
    }
]

def seed_demo_accounts(db: Session):
    for acc in DEMO_ACCOUNTS:
        u = db.query(User).filter((User.id == acc["id"]) | (User.username == acc["username"])).first()
        p_hash, salt = hash_password(acc["password"])
        if not u:
            u = User(
                id=acc["id"],
                username=acc["username"],
                email=acc["email"],
                full_name=acc["full_name"],
                password_hash=p_hash,
                salt=salt,
                target_company=acc["target_company"],
                preferences={"target_company": acc["target_company"], "daily_goal": 15, "avatar": acc["avatar"]}
            )
            db.add(u)
        else:
            if not u.password_hash:
                u.password_hash = p_hash
                u.salt = salt
            if not u.full_name:
                u.full_name = acc["full_name"]
            if not u.target_company:
                u.target_company = acc["target_company"]
    db.commit()
