# Google Maps CRM Web Uygulaması

Bu proje, Google Maps API kullanarak işletme arama ve CRM yönetimi yapan bir web uygulamasıdır.

## Özellikler

- ✅ Kullanıcı kayıt/giriş sistemi
- ✅ Bakiye/kredi sistemi (yeni kullanıcılara 50 kredi)
- ✅ Google Maps API ile işletme arama
- ✅ Firma listesi ve detay görüntüleme
- ✅ CRM özellikleri (aşama yönetimi, aktivite takibi)
- ✅ Excel export (ücretsiz)
- ✅ Admin paneli (kullanıcı yönetimi, bakiye yükleme)
- ✅ Aydınlık/karanlık tema desteği

## Railway'e Deploy

1. Railway hesabı oluşturun: https://railway.app
2. Yeni proje oluşturun
3. GitHub repository'nizi bağlayın veya manuel deploy yapın
4. Environment variables ekleyin:
   - `GOOGLE_MAPS_API_KEY`: Google Maps API anahtarınız
   - `SECRET_KEY`: Güçlü bir secret key (JWT için)
   - `DATABASE_URL`: Railway PostgreSQL otomatik oluşturur
5. Deploy butonuna tıklayın

## Lokal Geliştirme

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Environment Variables

`.env` dosyası oluşturun:

```
GOOGLE_MAPS_API_KEY=your-key
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./crm_data.db
```

## API Endpoints

- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Kullanıcı girişi
- `GET /api/auth/me` - Mevcut kullanıcı bilgileri
- `GET /api/dashboard/stats` - Dashboard istatistikleri
- `POST /api/search/` - İşletme arama
- `GET /api/companies/` - Firma listesi
- `GET /api/excel/export` - Excel export
- `GET /api/admin/users` - Admin: Kullanıcı listesi
- `POST /api/admin/users/{user_id}/credit` - Admin: Kredi yükleme

## Kredi Sistemi

- Yeni kullanıcı: 50 kredi
- 1 işletme sorgusu: 1 kredi
- Excel export: Ücretsiz (0 kredi)

## İlk Admin Kullanıcı

Veritabanında manuel olarak admin kullanıcı oluşturmanız gerekir:

```python
from app.models.database import User, SessionLocal
from app.utils.auth import get_password_hash

db = SessionLocal()
admin_user = User(
    email="admin@example.com",
    username="admin",
    hashed_password=get_password_hash("admin123"),
    is_admin=True,
    balance=1000
)
db.add(admin_user)
db.commit()
```

