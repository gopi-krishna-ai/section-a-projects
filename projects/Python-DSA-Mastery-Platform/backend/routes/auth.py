from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from backend.database import get_db
from backend.models import User
from backend.schemas import (
    UserRegisterRequest, UserLoginRequest, SwitchDemoRequest,
    UserProfileResponse, AuthResponse
)
from backend.services.auth import (
    hash_password, verify_password, create_access_token,
    verify_access_token, DEMO_ACCOUNTS
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def get_current_user(
    authorization: Optional[str] = Header(None),
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
) -> User:
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

@router.post("/register", response_model=AuthResponse)
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip().lower()
    existing = db.query(User).filter_by(username=clean_username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    p_hash, salt = hash_password(payload.password)
    user = User(
        username=clean_username,
        email=payload.email,
        full_name=payload.full_name or payload.username,
        password_hash=p_hash,
        salt=salt,
        target_goal=payload.target_goal or "FAANG & Competitive DSA",
        skill_level=payload.skill_level or "intermediate",
        avatar=(clean_username[:2]).upper()
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    return AuthResponse(token=token, user=UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        skill_level=user.skill_level,
        target_goal=user.target_goal,
        avatar=user.avatar
    ))

@router.post("/login", response_model=AuthResponse)
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip().lower()
    user = db.query(User).filter_by(username=clean_username).first()
    if not user or not verify_password(payload.password, user.password_hash, user.salt):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.id)
    return AuthResponse(token=token, user=UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        skill_level=user.skill_level,
        target_goal=user.target_goal,
        avatar=user.avatar
    ))

@router.get("/demo_users", response_model=List[UserProfileResponse])
def get_demo_users():
    return [
        UserProfileResponse(
            id=d["id"],
            username=d["username"],
            email=d["email"],
            full_name=d["full_name"],
            skill_level=d["skill_level"],
            target_goal=d["target_goal"],
            avatar=d["avatar"]
        )
        for d in DEMO_ACCOUNTS
    ]

@router.post("/switch_demo", response_model=AuthResponse)
def switch_demo(payload: SwitchDemoRequest, db: Session = Depends(get_db)):
    clean_username = payload.username.strip().lower()
    user = db.query(User).filter_by(username=clean_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Demo account not found")

    token = create_access_token(user.id)
    return AuthResponse(token=token, user=UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        skill_level=user.skill_level,
        target_goal=user.target_goal,
        avatar=user.avatar
    ))

@router.get("/me", response_model=UserProfileResponse)
def get_me(user: User = Depends(get_current_user)):
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        skill_level=user.skill_level,
        target_goal=user.target_goal,
        avatar=user.avatar
    )
