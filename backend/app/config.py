"""
Uygulama yapılandırma dosyası
"""
import os
from typing import Optional

# Google Maps API Anahtarı
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')

# Veritabanı
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./crm_data.db')

# JWT Secret Key
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 gün

# Kredi sistemi
YENI_KULLANICI_KREDI = 50
SORGU_BASINA_KREDI = 1
EXCEL_KREDI = 0  # Ücretsiz

# Türkiye şehirleri listesi
TURKIYE_SEHIRLERI = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya",
    "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur",
    "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne",
    "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
    "Hakkari", "Hatay", "Isparta", "Mersin", "İstanbul", "İzmir", "Kars", "Kastamonu",
    "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya",
    "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde",
    "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ",
    "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak",
    "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın",
    "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"
]

# Aşama seçenekleri
ASAMA_SECENEKLERI = ["Yeni", "İletişimde", "Teklif", "Kapalı", "İptal"]

# Aktivite tipleri
AKTIVITE_TIPLERI = ["Tel", "E-posta", "Ziyaret", "Toplantı", "Not", "Diğer"]

# Ülke listesi
ULKELER = [
    "Türkiye", "Almanya", "Fransa", "İngiltere", "İtalya", "İspanya", 
    "Yunanistan", "Bulgaristan", "Romanya", "Rusya", "Ukrayna", "Polonya",
    "ABD", "Kanada", "Meksika", "Brezilya", "Arjantin", "Japonya", "Çin",
    "Hindistan", "Avustralya", "Yeni Zelanda", "Güney Afrika", "Mısır"
]

# Kategori listesi
KATEGORILER = [
    "emlak", "restoran", "market", "eczane", "hastane", "okul", "üniversite",
    "otel", "kafe", "berber", "kuaför", "spor salonu", "fitness", "gym",
    "otomobil", "oto yedek parça", "oto galeri", "benzin istasyonu",
    "avukat", "muhasebeci", "doktor", "diş hekimi", "veteriner",
    "mobilya", "elektronik", "giyim", "ayakkabı", "kozmetik", "kuyumcu",
    "banka", "sigorta", "inşaat", "mimarlık", "mühendislik", "temizlik",
    "güvenlik", "nakliyat", "kargo", "kurye", "pizza", "hamburger",
    "fast food", "pastane", "fırın", "manav", "kasap", "balık",
    "kitap", "kırtasiye", "oyuncak", "bebek", "çocuk", "evlilik",
    "düğün salonu", "cafe", "bar", "disco", "sinema", "tiyatro",
    "müze", "park", "plaj", "havuz", "spor", "futbol", "basketbol"
]

