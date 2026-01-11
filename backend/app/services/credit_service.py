"""
Kredi/Bakiye yönetim servisi
"""
from sqlalchemy.orm import Session
from app.models.database import User, Transaction, Query
from datetime import datetime
import app.config as config


class CreditService:
    @staticmethod
    def check_balance(db: Session, user_id: int) -> int:
        """Kullanıcı bakiyesini kontrol et"""
        user = db.query(User).filter(User.id == user_id).first()
        return user.balance if user else 0
    
    @staticmethod
    def deduct_credit(db: Session, user_id: int, amount: int, description: str) -> bool:
        """
        Kredi düşür
        
        Args:
            db: Database session
            user_id: Kullanıcı ID
            amount: Düşürülecek miktar (pozitif sayı)
            description: İşlem açıklaması
        
        Returns:
            Başarılı ise True
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if user.balance < amount:
            return False  # Yetersiz bakiye
        
        # Bakiyeyi düşür
        user.balance -= amount
        
        # İşlem kaydı oluştur
        transaction = Transaction(
            user_id=user_id,
            amount=-amount,  # Negatif (harcama)
            description=description
        )
        db.add(transaction)
        db.commit()
        
        return True
    
    @staticmethod
    def add_credit(db: Session, user_id: int, amount: int, description: str) -> bool:
        """
        Kredi ekle (admin tarafından)
        
        Args:
            db: Database session
            user_id: Kullanıcı ID
            amount: Eklenecek miktar (pozitif sayı)
            description: İşlem açıklaması
        
        Returns:
            Başarılı ise True
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Bakiyeyi artır
        user.balance += amount
        
        # İşlem kaydı oluştur
        transaction = Transaction(
            user_id=user_id,
            amount=amount,  # Pozitif (yükleme)
            description=description
        )
        db.add(transaction)
        db.commit()
        
        return True
    
    @staticmethod
    def get_transactions(db: Session, user_id: int, limit: int = 50):
        """Kullanıcının işlem geçmişini getir"""
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).limit(limit).all()
        return transactions
    
    @staticmethod
    def save_query(db: Session, user_id: int, sehir: str, kategori: str, 
                   ulke: str, limit: int, result_count: int):
        """Sorgu geçmişini kaydet"""
        query = Query(
            user_id=user_id,
            sehir=sehir,
            kategori=kategori,
            ulke=ulke,
            limit=limit,
            result_count=result_count
        )
        db.add(query)
        db.commit()
        return query

