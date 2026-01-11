"""
Theme routes - Tema yönetimi
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.database import User, get_db
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/theme", tags=["theme"])


class ThemeUpdate(BaseModel):
    theme: str  # "dark" veya "light"


@router.patch("/", response_model=dict)
async def update_theme(
    theme_data: ThemeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcı temasını güncelle"""
    if theme_data.theme not in ["dark", "light"]:
        return {"error": "Geçersiz tema. 'dark' veya 'light' olmalı"}
    
    current_user.theme = theme_data.theme
    db.commit()
    
    return {"message": "Tema güncellendi", "theme": theme_data.theme}

