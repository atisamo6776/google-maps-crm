"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from app.models.database import User, get_db, init_db
from app.utils.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user
)
from app.models.database import User as UserModel
import app.config as config

router = APIRouter(prefix="/api/auth", tags=["auth"])


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    balance: int
    is_admin: bool
    theme: str
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


@router.post("/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Yeni kullanıcı kaydı"""
    # Email kontrolü
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Username kontrolü
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Yeni kullanıcı oluştur
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        balance=config.YENI_KULLANICI_KREDI  # 50 kredi
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Token oluştur
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            balance=new_user.balance,
            is_admin=new_user.is_admin,
            theme=new_user.theme
        )
    }


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Kullanıcı girişi"""
    # Username veya email ile giriş yapılabilir
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token oluştur
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            balance=user.balance,
            is_admin=user.is_admin,
            theme=user.theme
        )
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserModel = Depends(get_current_user)):
    """Mevcut kullanıcı bilgilerini getir"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        balance=current_user.balance,
        is_admin=current_user.is_admin,
        theme=current_user.theme
    )

