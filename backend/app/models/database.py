"""
SQLAlchemy database models
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import app.config as config

Base = declarative_base()

# Database engine
if config.DATABASE_URL.startswith('sqlite'):
    engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(config.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """Kullanıcı modeli"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Integer, default=config.YENI_KULLANICI_KREDI)  # Kredi bakiyesi
    is_admin = Column(Boolean, default=False)
    theme = Column(String, default='dark')  # 'dark' veya 'light'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    queries = relationship("Query", back_populates="user", cascade="all, delete-orphan")
    companies = relationship("Company", back_populates="user", cascade="all, delete-orphan")


class Transaction(Base):
    """Bakiye işlemleri modeli"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Pozitif: yükleme, Negatif: harcama
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    user = relationship("User", back_populates="transactions")


class Query(Base):
    """Sorgu geçmişi modeli"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sehir = Column(String)
    kategori = Column(String)
    ulke = Column(String)
    limit = Column(Integer)
    result_count = Column(Integer)  # Kaç sonuç bulundu
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    user = relationship("User", back_populates="queries")


class Company(Base):
    """Firma modeli"""
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    firma_adi = Column(String, nullable=False)
    sehir = Column(String)
    ilce = Column(String)
    ulke = Column(String)
    adres = Column(Text)
    telefon = Column(String)
    web = Column(String)
    asama = Column(String, default='Yeni')
    rating = Column(Float)
    user_ratings_total = Column(Integer)
    price_level = Column(Integer)
    business_status = Column(String)
    international_phone_number = Column(String)
    url = Column(String)
    plus_code = Column(String)
    type = Column(String)
    types = Column(Text)
    kategori = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    user = relationship("User", back_populates="companies")
    activities = relationship("Activity", back_populates="company", cascade="all, delete-orphan")


class Activity(Base):
    """Aktivite modeli"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    aktivite_tipi = Column(String, nullable=False)
    sonuc = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    company = relationship("Company", back_populates="activities")


# Veritabanı tablolarını oluştur
def init_db():
    """Veritabanı tablolarını oluştur"""
    Base.metadata.create_all(bind=engine)


# Dependency injection için
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

