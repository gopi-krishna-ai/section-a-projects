from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from backend.database import get_db
from backend.models import User, TopicMastery, Topic
from backend.services.auth import (
    hash_password, verify_password, create_access_token,
    verify_access_token, DEMO_ACCOUNTS
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    target_company: Optional[str] = "TCS / Infosys"

class LoginRequest(BaseModel):
    username: str
    password: str

class SwitchDemoRequest(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    target_company: str
    preferences: Dict[str, Any] = {}
    created_at: datetime

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip().lower()
    if len(clean_username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    existing = db.query(User).filter_by(username=clean_username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists. Please pick another or log in.")

    p_hash, salt = hash_password(payload.password)
    new_user = User(
        username=clean_username,
        email=payload.email,
        full_name=payload.full_name or clean_username.title(),
        password_hash=p_hash,
        salt=salt,
        target_company=payload.target_company or "TCS / Infosys",
        preferences={"target_company": payload.target_company or "TCS / Infosys", "daily_goal": 15}
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize topic masteries
    topics = db.query(Topic).all()
    for t in topics:
        db.add(TopicMastery(
            user_id=new_user.id,
            topic_id=t.id,
            mastery_score=0.0,
            status="not_started"
        ))
    db.commit()

    token = create_access_token(new_user.id)
    return AuthResponse(token=token, user=new_user)

@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip().lower()
    user = db.query(User).filter_by(username=clean_username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(payload.password, user.password_hash or "", user.salt or ""):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.id)
    return AuthResponse(token=token, user=user)

@router.get("/me", response_model=UserResponse)
def get_current_user(
    authorization: Optional[str] = Header(None),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    uid = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        uid = verify_access_token(token)

    if not uid:
        uid = user_id or "default_user"

    user = db.query(User).filter_by(id=uid).first()
    if not user:
        user = db.query(User).filter_by(id="default_user").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/demo_users")
def get_demo_users():
    return [
        {
            "id": a["id"],
            "username": a["username"],
            "full_name": a["full_name"],
            "target_company": a["target_company"],
            "email": a["email"],
            "avatar": a["avatar"]
        }
        for a in DEMO_ACCOUNTS
    ]

@router.post("/switch_demo", response_model=AuthResponse)
def switch_demo(payload: SwitchDemoRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip().lower()
    user = db.query(User).filter_by(username=clean_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not found")

    token = create_access_token(user.id)
    return AuthResponse(token=token, user=user)
