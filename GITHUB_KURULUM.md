# GitHub'a Yükleme Rehberi

## Yöntem 1: GitHub Desktop ile (Kolay)

1. **GitHub Desktop İndir**
   - https://desktop.github.com adresinden indirin
   - GitHub hesabınızla giriş yapın

2. **Repository Oluştur**
   - GitHub Desktop'ta "File" > "New Repository"
   - Name: `google-maps-crm` (veya istediğiniz isim)
   - Local Path: `C:\Users\atill\OneDrive\Masaüstü\projects\google_maps\deploy`
   - "Initialize this repository with a README" işaretlemeyin
   - "Create Repository" tıklayın

3. **Dosyaları Ekle ve Commit**
   - Tüm dosyalar otomatik görünecek
   - Sol altta "Summary" kısmına "Initial commit" yazın
   - "Commit to main" butonuna tıklayın

4. **GitHub'a Push Et**
   - "Publish repository" butonuna tıklayın
   - Repository adını onaylayın
   - "Publish" tıklayın

## Yöntem 2: Komut Satırı ile (Terminal)

### Adım 1: Git Kurulumu
Eğer Git yüklü değilse:
- https://git-scm.com/download/win adresinden indirin
- Kurulum sırasında "Git from the command line" seçeneğini işaretleyin

### Adım 2: Terminal'de Komutlar

```powershell
# deploy klasörüne git
cd "C:\Users\atill\OneDrive\Masaüstü\projects\google_maps\deploy"

# Git repository başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: Google Maps CRM web uygulaması"

# GitHub'da yeni repository oluştur (web tarayıcıdan)
# https://github.com/new adresine gidin
# Repository adı: google-maps-crm
# Public veya Private seçin
# "Create repository" tıklayın

# GitHub repository URL'ini ekle (kendi kullanıcı adınızla değiştirin)
git remote add origin https://github.com/KULLANICI_ADINIZ/google-maps-crm.git

# Dosyaları GitHub'a push et
git branch -M main
git push -u origin main
```

## Yöntem 3: GitHub Web Arayüzü ile

1. **GitHub'da Repository Oluştur**
   - https://github.com/new adresine gidin
   - Repository adı: `google-maps-crm`
   - Public veya Private seçin
   - "Create repository" tıklayın

2. **Dosyaları Yükle**
   - GitHub'da "uploading an existing file" linkine tıklayın
   - Veya "Add file" > "Upload files"
   - `deploy` klasöründeki tüm dosyaları sürükle-bırak yapın
   - "Commit changes" tıklayın

## Önemli Notlar

- `.env` dosyasını GitHub'a yüklemeyin (güvenlik)
- `.gitignore` dosyası zaten oluşturuldu, hassas dosyalar otomatik ignore edilir
- İlk push'tan sonra Railway'e bağlayabilirsiniz

## Railway'e Bağlama

1. Railway'de "New Project" > "Deploy from GitHub repo"
2. Oluşturduğunuz repository'yi seçin
3. Railway otomatik olarak deploy edecek

