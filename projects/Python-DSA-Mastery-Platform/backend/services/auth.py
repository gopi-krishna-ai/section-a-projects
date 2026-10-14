import hmac
import hashlib
import secrets
import time
from typing import Tuple, Optional, Dict, Any, List
from sqlalchemy.orm import Session
from backend.config import settings
from backend.models import User

TOKEN_EXPIRY_SECONDS = settings.TOKEN_EXPIRY_DAYS * 24 * 3600

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
    sig = hmac.new(settings.SECRET_KEY.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"

def verify_access_token(token: str) -> Optional[str]:
    try:
        parts = token.split(':')
        if len(parts) != 3:
            return None
        user_id, timestamp_str, sig = parts
        payload = f"{user_id}:{timestamp_str}"
        expected_sig = hmac.new(settings.SECRET_KEY.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()
        if not secrets.compare_digest(sig, expected_sig):
            return None
        
        timestamp = int(timestamp_str)
        if time.time() - timestamp > TOKEN_EXPIRY_SECONDS:
            return None
            
        return user_id
    except Exception:
        return None

DEMO_ACCOUNTS = [
    {
        "id": "user_pyninja",
        "username": "py_ninja",
        "full_name": "Kavya Patel",
        "email": "kavya@pyninja.dev",
        "password": "password123",
        "skill_level": "advanced",
        "target_goal": "Senior Backend & System Architecture",
        "avatar": "KP"
    },
    {
        "id": "user_algomaster",
        "username": "algo_master",
        "full_name": "Arjun Sharma",
        "email": "arjun@algomaster.dev",
        "password": "password123",
        "skill_level": "advanced",
        "target_goal": "FAANG / Competitive Coding",
        "avatar": "AS"
    },
    {
        "id": "user_beginner",
        "username": "beginner_coder",
        "full_name": "Liam Vance",
        "email": "liam@beginner.dev",
        "password": "password123",
        "skill_level": "intermediate",
        "target_goal": "Independent Algorithmic Thinking",
        "avatar": "LV"
    },
    {
        "id": "default_user",
        "username": "dev_rohan",
        "full_name": "Rohan Mistry",
        "email": "rohan@mastery.dev",
        "password": "password123",
        "skill_level": "intermediate",
        "target_goal": "Full-Stack Python & DSA Mastery",
        "avatar": "RM"
    }
]

def seed_demo_users(db: Session):
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
                skill_level=acc["skill_level"],
                target_goal=acc["target_goal"],
                avatar=acc["avatar"],
                preferences={"target_goal": acc["target_goal"], "dark_mode": True, "editor_font_size": 14}
            )
            db.add(u)
        else:
            if not u.password_hash:
                u.password_hash = p_hash
                u.salt = salt
    db.commit()
