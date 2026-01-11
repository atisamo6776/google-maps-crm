"""
Authentication utilities
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.database import User, get_db
import app.config as config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrulama"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Şifre hashleme"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT token oluştur"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Mevcut kullanıcıyı token'dan al"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Debug log
    import logging
    logger = logging.getLogger(__name__)
    
    if not token:
        logger.error("❌ Token None veya boş!")
        raise credentials_exception
    
    logger.info(f"✅ Token alındı, uzunluk: {len(token)}")
    logger.info(f"Token başlangıcı: {token[:50]}...")
    logger.info(f"SECRET_KEY var mı: {bool(config.SECRET_KEY)}")
    logger.info(f"SECRET_KEY uzunluk: {len(config.SECRET_KEY) if config.SECRET_KEY else 0}")
    logger.info(f"SECRET_KEY başlangıcı: {config.SECRET_KEY[:10] if config.SECRET_KEY else 'YOK'}...")
    
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        logger.info(f"✅ Token decode başarılı, payload: {payload}")
        user_id: int = payload.get("sub")
        if user_id is None:
            logger.error("❌ Token payload'da 'sub' bulunamadı")
            raise credentials_exception
        logger.info(f"✅ User ID: {user_id}")
    except JWTError as e:
        logger.error(f"❌ JWT decode hatası: {str(e)}")
        logger.error(f"Token: {token[:50]}...")
        logger.error(f"SECRET_KEY kullanılan: {config.SECRET_KEY[:10] if config.SECRET_KEY else 'YOK'}...")
        raise credentials_exception
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"❌ User bulunamadı, ID: {user_id}")
        raise credentials_exception
    
    logger.info(f"✅ User bulundu: {user.username}")
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Admin kullanıcı kontrolü"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

