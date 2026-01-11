"""
Admin routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.models.database import User, Transaction, get_db
from app.utils.auth import get_current_admin_user
from app.services.credit_service import CreditService

router = APIRouter(prefix="/api/admin", tags=["admin"])


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    balance: int
    is_admin: bool
    created_at: str
    
    class Config:
        from_attributes = True


class CreditUpdate(BaseModel):
    amount: int
    description: str


class UserSearch(BaseModel):
    query: str  # Email veya username ile arama


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    search: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Tüm kullanıcıları listele (arama ile)"""
    query = db.query(User)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.email.like(search_term)) | (User.username.like(search_term))
        )
    
    users = query.order_by(User.created_at.desc()).all()
    
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            username=u.username,
            balance=u.balance,
            is_admin=u.is_admin,
            created_at=u.created_at.isoformat() if u.created_at else ""
        )
        for u in users
    ]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Kullanıcı detayını getir"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        balance=user.balance,
        is_admin=user.is_admin,
        created_at=user.created_at.isoformat() if user.created_at else ""
    )


@router.post("/users/{user_id}/credit", response_model=dict)
async def add_credit_to_user(
    user_id: int,
    credit_data: CreditUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Kullanıcıya kredi ekle"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    if credit_data.amount <= 0:
        raise HTTPException(status_code=400, detail="Kredi miktarı pozitif olmalı")
    
    credit_service = CreditService()
    success = credit_service.add_credit(
        db=db,
        user_id=user_id,
        amount=credit_data.amount,
        description=credit_data.description
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Kredi ekleme hatası")
    
    # Güncel bakiyeyi al
    db.refresh(user)
    
    return {
        "message": "Kredi eklendi",
        "new_balance": user.balance
    }


@router.get("/users/{user_id}/transactions")
async def get_user_transactions(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının işlem geçmişini getir"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.created_at.desc()).limit(100).all()
    
    return [
        {
            "id": t.id,
            "amount": t.amount,
            "description": t.description,
            "created_at": t.created_at.isoformat() if t.created_at else ""
        }
        for t in transactions
    ]

