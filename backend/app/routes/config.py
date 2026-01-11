"""
Config routes - Uygulama yapılandırma verileri
"""
from fastapi import APIRouter
from typing import List
import app.config as config

router = APIRouter(prefix="/api/config", tags=["config"])


class ConfigResponse:
    sehirler: List[str]
    ulkeler: List[str]
    kategoriler: List[str]
    asama_secenekleri: List[str]
    aktivite_tipleri: List[str]


@router.get("/")
async def get_config():
    """Uygulama yapılandırma verilerini getir"""
    return {
        "sehirler": config.TURKIYE_SEHIRLERI,
        "ulkeler": config.ULKELER,
        "kategoriler": config.KATEGORILER,
        "asama_secenekleri": config.ASAMA_SECENEKLERI,
        "aktivite_tipleri": config.AKTIVITE_TIPLERI
    }

