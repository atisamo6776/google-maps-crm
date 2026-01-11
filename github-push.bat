@echo off
echo GitHub'a Push Etme Scripti
echo.

cd /d "%~dp0"

echo Git repository kontrol ediliyor...
if not exist ".git" (
    echo Git repository başlatılıyor...
    git init
)

echo Dosyalar ekleniyor...
git add .

echo Commit yapılıyor...
git commit -m "Update: Google Maps CRM web uygulaması"

echo.
echo ========================================
echo Şimdi GitHub'da repository oluşturun:
echo 1. https://github.com/new adresine gidin
echo 2. Repository adı: google-maps-crm
echo 3. Create repository tıklayın
echo.
echo Sonra şu komutu çalıştırın:
echo git remote add origin https://github.com/KULLANICI_ADINIZ/google-maps-crm.git
echo git branch -M main
echo git push -u origin main
echo ========================================
echo.

pause

