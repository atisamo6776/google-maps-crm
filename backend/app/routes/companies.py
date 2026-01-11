"""
Companies routes - Firma yönetimi
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.models.database import User, Company, Activity, get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/companies", tags=["companies"])


class CompanyResponse(BaseModel):
    id: int
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
    created_at: Optional[str]
    
    class Config:
        from_attributes = True


class CompanyUpdate(BaseModel):
    asama: Optional[str] = None


class ActivityCreate(BaseModel):
    aktivite_tipi: str
    sonuc: Optional[str] = None


class ActivityResponse(BaseModel):
    id: int
    aktivite_tipi: str
    sonuc: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[CompanyResponse])
async def get_companies(
    sehir_filtre: Optional[str] = None,
    ilce_filtre: Optional[str] = None,
    asama_filtre: Optional[str] = None,
    telefon_filtre: Optional[str] = None,  # "hepsi", "var", "yok"
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Firmaları listele (filtrelerle)"""
    query = db.query(Company).filter(Company.user_id == current_user.id)
    
    if sehir_filtre and sehir_filtre != "Hepsi":
        query = query.filter(Company.sehir == sehir_filtre)
    
    if ilce_filtre and ilce_filtre != "Hepsi":
        query = query.filter(Company.ilce == ilce_filtre)
    
    if asama_filtre and asama_filtre != "Hepsi":
        query = query.filter(Company.asama == asama_filtre)
    
    if telefon_filtre == "var":
        query = query.filter(Company.telefon.isnot(None), Company.telefon != "")
    elif telefon_filtre == "yok":
        query = query.filter(
            (Company.telefon.is_(None)) | (Company.telefon == "")
        )
    
    companies = query.order_by(Company.created_at.desc()).all()
    
    return [
        CompanyResponse(
            id=c.id,
            firma_adi=c.firma_adi,
            sehir=c.sehir,
            ilce=c.ilce,
            ulke=c.ulke,
            adres=c.adres,
            telefon=c.telefon,
            web=c.web,
            asama=c.asama,
            rating=c.rating,
            user_ratings_total=c.user_ratings_total,
            price_level=c.price_level,
            business_status=c.business_status,
            international_phone_number=c.international_phone_number,
            url=c.url,
            plus_code=c.plus_code,
            type=c.type,
            types=c.types,
            kategori=c.kategori,
            created_at=c.created_at.isoformat() if c.created_at else None
        )
        for c in companies
    ]


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Firma detayını getir"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Firma bulunamadı")
    
    return CompanyResponse(
        id=company.id,
        firma_adi=company.firma_adi,
        sehir=company.sehir,
        ilce=company.ilce,
        ulke=company.ulke,
        adres=company.adres,
        telefon=company.telefon,
        web=company.web,
        asama=company.asama,
        rating=company.rating,
        user_ratings_total=company.user_ratings_total,
        price_level=company.price_level,
        business_status=company.business_status,
        international_phone_number=company.international_phone_number,
        url=company.url,
        plus_code=company.plus_code,
        type=company.type,
        types=company.types,
        kategori=company.kategori,
        created_at=company.created_at.isoformat() if company.created_at else None
    )


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    update_data: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Firma bilgilerini güncelle (sadece aşama)"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Firma bulunamadı")
    
    if update_data.asama:
        company.asama = update_data.asama
    
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        id=company.id,
        firma_adi=company.firma_adi,
        sehir=company.sehir,
        ilce=company.ilce,
        ulke=company.ulke,
        adres=company.adres,
        telefon=company.telefon,
        web=company.web,
        asama=company.asama,
        rating=company.rating,
        user_ratings_total=company.user_ratings_total,
        price_level=company.price_level,
        business_status=company.business_status,
        international_phone_number=company.international_phone_number,
        url=company.url,
        plus_code=company.plus_code,
        type=company.type,
        types=company.types,
        kategori=company.kategori,
        created_at=company.created_at.isoformat() if company.created_at else None
    )


@router.delete("/{company_id}")
async def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Firmayı sil"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Firma bulunamadı")
    
    db.delete(company)
    db.commit()
    
    return {"message": "Firma silindi"}


@router.get("/{company_id}/activities", response_model=List[ActivityResponse])
async def get_company_activities(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Firmanın aktivitelerini getir"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Firma bulunamadı")
    
    activities = db.query(Activity).filter(
        Activity.company_id == company_id
    ).order_by(Activity.created_at.desc()).all()
    
    return [
        ActivityResponse(
            id=a.id,
            aktivite_tipi=a.aktivite_tipi,
            sonuc=a.sonuc,
            created_at=a.created_at.isoformat() if a.created_at else ""
        )
        for a in activities
    ]


@router.post("/{company_id}/activities", response_model=ActivityResponse)
async def create_activity(
    company_id: int,
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Yeni aktivite ekle"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Firma bulunamadı")
    
    activity = Activity(
        company_id=company_id,
        aktivite_tipi=activity_data.aktivite_tipi,
        sonuc=activity_data.sonuc
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return ActivityResponse(
        id=activity.id,
        aktivite_tipi=activity.aktivite_tipi,
        sonuc=activity.sonuc,
        created_at=activity.created_at.isoformat() if activity.created_at else ""
    )


@router.delete("/{company_id}/activities/{activity_id}")
async def delete_activity(
    company_id: int,
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Aktiviteyi sil"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Firma bulunamadı")
    
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.company_id == company_id
    ).first()
    
    if not activity:
        raise HTTPException(status_code=404, detail="Aktivite bulunamadı")
    
    db.delete(activity)
    db.commit()
    
    return {"message": "Aktivite silindi"}


@router.get("/filters/cities")
async def get_cities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının firmalarındaki şehirleri getir"""
    cities = db.query(Company.sehir).filter(
        Company.user_id == current_user.id,
        Company.sehir.isnot(None),
        Company.sehir != ""
    ).distinct().all()
    
    return [city[0] for city in cities]


@router.get("/filters/districts")
async def get_districts(
    sehir: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının firmalarındaki ilçeleri getir"""
    query = db.query(Company.ilce).filter(
        Company.user_id == current_user.id,
        Company.ilce.isnot(None),
        Company.ilce != ""
    )
    
    if sehir and sehir != "Hepsi":
        query = query.filter(Company.sehir == sehir)
    
    districts = query.distinct().all()
    
    return [district[0] for district in districts]

