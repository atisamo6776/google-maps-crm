# Railway Deployment Rehberi

## Adımlar

1. **Railway Hesabı Oluştur**
   - https://railway.app adresine gidin
   - GitHub ile giriş yapın

2. **Yeni Proje Oluştur**
   - "New Project" butonuna tıklayın
   - "Deploy from GitHub repo" seçin
   - Repository'nizi seçin veya deploy klasörünü GitHub'a push edin

3. **PostgreSQL Database Ekle**
   - Railway dashboard'da "New" butonuna tıklayın
   - "Database" > "Add PostgreSQL" seçin
   - Database otomatik oluşturulur ve `DATABASE_URL` environment variable olarak eklenir

4. **Environment Variables Ekle**
   - Proje ayarlarına gidin
   - "Variables" sekmesine tıklayın
   - Şu değişkenleri ekleyin:
     ```
     GOOGLE_MAPS_API_KEY=your-google-maps-api-key
     SECRET_KEY=your-strong-secret-key-here
     ```
   - `DATABASE_URL` otomatik olarak PostgreSQL için ayarlanır

5. **Deploy**
   - Railway otomatik olarak deploy edecek
   - "Settings" > "Generate Domain" ile bir domain oluşturun

6. **İlk Admin Kullanıcı Oluştur**
   - Railway'de "PostgreSQL" database'inize tıklayın
   - "Query" sekmesine gidin
   - Şu SQL'i çalıştırın (şifreyi değiştirin):
   ```sql
   INSERT INTO users (email, username, hashed_password, is_admin, balance)
   VALUES (
       'admin@example.com',
       'admin',
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5',  -- 'admin123' şifresinin hash'i
       true,
       1000
   );
   ```
   
   Veya Python ile:
   ```python
   from app.models.database import User, SessionLocal
   from app.utils.auth import get_password_hash
   
   db = SessionLocal()
   admin = User(
       email="admin@example.com",
       username="admin",
       hashed_password=get_password_hash("admin123"),
       is_admin=True,
       balance=1000
   )
   db.add(admin)
   db.commit()
   ```

## Notlar

- Railway otomatik olarak `PORT` environment variable'ını ayarlar
- `Procfile` veya `railway.json` dosyası deployment komutunu belirler
- İlk deploy biraz zaman alabilir (5-10 dakika)
- Logs'u Railway dashboard'dan takip edebilirsiniz

## Sorun Giderme

- **Build hatası**: `requirements.txt` dosyasını kontrol edin
- **Database bağlantı hatası**: `DATABASE_URL` environment variable'ını kontrol edin
- **API hatası**: Google Maps API key'inizi kontrol edin
- **Static files yüklenmiyor**: Frontend klasör yapısını kontrol edin

