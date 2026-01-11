"""
Dashboard routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import User, Transaction, Query, get_db
from app.utils.auth import get_current_user
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


class DashboardStats(BaseModel):
    balance: int
    total_queries: int
    total_companies: int
    queries_today: int
    companies_today: int
    recent_transactions: List[dict]
    recent_queries: List[dict]


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dashboard istatistiklerini getir"""
    # Bugünün başlangıcı
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Toplam sorgu sayısı
    total_queries = db.query(Query).filter(Query.user_id == current_user.id).count()
    
    # Bugünkü sorgu sayısı
    queries_today = db.query(Query).filter(
        Query.user_id == current_user.id,
        Query.created_at >= today_start
    ).count()
    
    # Toplam firma sayısı
    from app.models.database import Company
    total_companies = db.query(Company).filter(Company.user_id == current_user.id).count()
    
    # Bugünkü firma sayısı
    companies_today = db.query(Company).filter(
        Company.user_id == current_user.id,
        Company.created_at >= today_start
    ).count()
    
    # Son işlemler (10 adet)
    recent_transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).limit(10).all()
    
    transactions_data = [
        {
            "id": t.id,
            "amount": t.amount,
            "description": t.description,
            "created_at": t.created_at.isoformat()
        }
        for t in recent_transactions
    ]
    
    # Son sorgular (10 adet)
    recent_queries = db.query(Query).filter(
        Query.user_id == current_user.id
    ).order_by(Query.created_at.desc()).limit(10).all()
    
    queries_data = [
        {
            "id": q.id,
            "sehir": q.sehir,
            "kategori": q.kategori,
            "ulke": q.ulke,
            "result_count": q.result_count,
            "created_at": q.created_at.isoformat()
        }
        for q in recent_queries
    ]
    
    return DashboardStats(
        balance=current_user.balance,
        total_queries=total_queries,
        total_companies=total_companies,
        queries_today=queries_today,
        companies_today=companies_today,
        recent_transactions=transactions_data,
        recent_queries=queries_data
    )

