"""
Search routes - Google Maps arama
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.models.database import User, Company, get_db
from app.utils.auth import get_current_user
from app.services.google_maps_service import GoogleMapsService
from app.services.credit_service import CreditService
import app.config as config

router = APIRouter(prefix="/api/search", tags=["search"])


class SearchRequest(BaseModel):
    sehir: Optional[str] = None
    ulke: str = "Türkiye"
    kategori: str
    limit: int = 20
    tum_sehirler: bool = False
    telefon_filtre: bool = False


class CompanyResponse(BaseModel):
    id: Optional[int] = None
    firma_adi: str
    sehir: Optional[str]
    ilce: Optional[str]
    ulke: Optional[str]
    adres: Optional[str]
    telefon: Optional[str]
    web: Optional[str]
    asama: Optional[str]
    rating: Optional[float]
    user_ratings_total: Optional[int]
    price_level: Optional[int]
    business_status: Optional[str]
    international_phone_number: Optional[str]
    url: Optional[str]
    plus_code: Optional[str]
    type: Optional[str]
    types: Optional[str]
    kategori: Optional[str]
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    companies: List[CompanyResponse]
    total_found: int
    credits_used: int
    remaining_balance: int


def save_companies_to_db(db: Session, user_id: int, companies: List[dict], kategori: str):
    """Firmaları veritabanına kaydet (background task)"""
    for company_data in companies:
        # Firma zaten var mı kontrol et
        existing = db.query(Company).filter(
            Company.user_id == user_id,
            Company.firma_adi == company_data['firma_adi'],
            Company.adres == company_data.get('adres', '')
        ).first()
        
        if existing:
            # Güncelle
            for key, value in company_data.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            if kategori:
                existing.kategori = kategori
        else:
            # Yeni ekle
            new_company = Company(
                user_id=user_id,
                kategori=kategori,
                **company_data
            )
            db.add(new_company)
    
    db.commit()


@router.post("/", response_model=SearchResponse)
async def search_companies(
    search_request: SearchRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """İşletme ara"""
    # Bakiye kontrolü
    credit_service = CreditService()
    balance = credit_service.check_balance(db, current_user.id)
    
    # Gerekli kredi hesapla
    required_credits = search_request.limit * config.SORGU_BASINA_KREDI
    
    if balance < required_credits:
        raise HTTPException(
            status_code=400,
            detail=f"Yetersiz bakiye. Gerekli: {required_credits}, Mevcut: {balance}"
        )
    
    # Google Maps arama
    google_maps = GoogleMapsService()
    
    try:
        if search_request.tum_sehirler:
            # Tüm şehirlerde ara
            companies_data = google_maps.tum_sehirlerde_ara(
                kategori=search_request.kategori,
                ulke=search_request.ulke,
                limit_per_sehir=search_request.limit,
                telefon_filtre=search_request.telefon_filtre
            )
        else:
            # Tek şehirde ara
            if not search_request.sehir:
                raise HTTPException(status_code=400, detail="Şehir belirtilmedi")
            
            companies_data = google_maps.isletme_ara(
                sehir=search_request.sehir,
                ulke=search_request.ulke,
                kategori=search_request.kategori,
                limit=search_request.limit,
                telefon_filtre=search_request.telefon_filtre
            )
        
        # Kredi düşür
        credits_used = len(companies_data) * config.SORGU_BASINA_KREDI
        success = credit_service.deduct_credit(
            db=db,
            user_id=current_user.id,
            amount=credits_used,
            description=f"Arama: {search_request.kategori} - {search_request.sehir or 'Tüm Şehirler'}"
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Kredi düşürme hatası")
        
        # Sorgu geçmişini kaydet
        credit_service.save_query(
            db=db,
            user_id=current_user.id,
            sehir=search_request.sehir or "Tüm Şehirler",
            kategori=search_request.kategori,
            ulke=search_request.ulke,
            limit=search_request.limit,
            result_count=len(companies_data)
        )
        
        # Firmaları veritabanına kaydet (background)
        background_tasks.add_task(
            save_companies_to_db,
            db=db,
            user_id=current_user.id,
            companies=companies_data,
            kategori=search_request.kategori
        )
        
        # Güncel bakiyeyi al
        db.refresh(current_user)
        
        # Response oluştur
        companies_response = [
            CompanyResponse(**company) for company in companies_data
        ]
        
        return SearchResponse(
            companies=companies_response,
            total_found=len(companies_data),
            credits_used=credits_used,
            remaining_balance=current_user.balance
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Arama hatası: {str(e)}")

