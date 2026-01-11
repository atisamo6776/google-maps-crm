"""
Google Maps API service
"""
import googlemaps
from typing import List, Dict
import time
import app.config as config


class GoogleMapsService:
    def __init__(self, api_key: str = config.GOOGLE_MAPS_API_KEY):
        """Google Maps API client'ını başlat"""
        self.client = googlemaps.Client(key=api_key)
    
    def isletme_ara(self, sehir: str, ulke: str, kategori: str, 
                    limit: int = 20, telefon_filtre: bool = False) -> List[Dict]:
        """
        Google Maps'te işletme ara
        
        Args:
            sehir: Arama yapılacak şehir
            ulke: Ülke adı
            kategori: İşletme kategorisi/anahtar kelime
            limit: Maksimum sonuç sayısı
            telefon_filtre: Sadece telefonu olanları getir
        
        Returns:
            İşletme bilgileri listesi
        """
        sonuclar = []
        query = f"{kategori} {sehir} {ulke}"
        
        try:
            # Text Search kullanarak arama yap (pagination ile)
            all_results = []
            next_page_token = None
            
            while len(all_results) < limit:
                if next_page_token:
                    # Sonraki sayfa için bekle (Google API gereksinimi)
                    time.sleep(2)
                    places_result = self.client.places(
                        query=query, 
                        language='tr',
                        page_token=next_page_token
                    )
                else:
                    places_result = self.client.places(query=query, language='tr')
                
                results = places_result.get('results', [])
                all_results.extend(results)
                
                # Sonraki sayfa var mı kontrol et
                next_page_token = places_result.get('next_page_token')
                if not next_page_token or len(results) == 0:
                    break
                
                # Limit'e ulaştık mı kontrol et
                if len(all_results) >= limit:
                    break
            
            # Limit kadar sonuç al
            for place in all_results[:limit]:
                place_id = place.get('place_id')
                
                if not place_id:
                    continue
                
                # Detaylı bilgileri al
                place_details = self.client.place(
                    place_id=place_id,
                    language='tr',
                    fields=['name', 'formatted_address', 'formatted_phone_number', 
                           'website', 'geometry', 'address_component', 'rating',
                           'user_ratings_total', 'price_level', 'business_status',
                           'international_phone_number', 'url', 'plus_code', 'type']
                )
                
                details = place_details.get('result', {})
                
                if not details:
                    continue
                
                # Şehir ve ilçe bilgisini address_component'ten çıkar
                sehir_bilgisi = self._sehir_cikar(details.get('address_components', []), sehir)
                ilce_bilgisi = self._ilce_cikar(details.get('address_components', []))
                
                # Type ve Types bilgilerini al
                type_str = details.get('type', '') or ''
                types_list = details.get('types', [])
                types_str = ', '.join(types_list[:10]) if types_list else ''
                
                firma_bilgisi = {
                    'firma_adi': details.get('name', ''),
                    'adres': details.get('formatted_address', ''),
                    'telefon': details.get('formatted_phone_number', '') or '',
                    'web': details.get('website', '') or '',
                    'sehir': sehir_bilgisi,
                    'ilce': ilce_bilgisi,
                    'ulke': ulke,
                    'rating': details.get('rating'),
                    'user_ratings_total': details.get('user_ratings_total'),
                    'price_level': details.get('price_level'),
                    'business_status': details.get('business_status', ''),
                    'international_phone_number': details.get('international_phone_number', '') or '',
                    'url': details.get('url', '') or '',
                    'plus_code': details.get('plus_code', {}).get('global_code', '') if details.get('plus_code') else '',
                    'type': type_str,
                    'types': types_str
                }
                
                # Telefon filtresi varsa kontrol et
                if telefon_filtre and not firma_bilgisi['telefon']:
                    continue
                
                sonuclar.append(firma_bilgisi)
                
                # Rate limit için kısa bekleme
                time.sleep(0.1)
        
        except Exception as e:
            print(f"Google Maps API hatası: {e}")
            raise
        
        return sonuclar
    
    def _sehir_cikar(self, address_components: List[Dict], varsayilan_sehir: str) -> str:
        """Address components'ten şehir bilgisini çıkar"""
        for component in address_components:
            types = component.get('types', [])
            if 'locality' in types or 'administrative_area_level_1' in types:
                return component.get('long_name', varsayilan_sehir)
        return varsayilan_sehir
    
    def _ilce_cikar(self, address_components: List[Dict]) -> str:
        """Address components'ten ilçe bilgisini çıkar"""
        for component in address_components:
            types = component.get('types', [])
            if 'sublocality' in types or 'sublocality_level_1' in types:
                return component.get('long_name', '')
            elif 'administrative_area_level_2' in types:
                return component.get('long_name', '')
        return ''
    
    def tum_sehirlerde_ara(self, kategori: str, ulke: str, limit_per_sehir: int = 20,
                           telefon_filtre: bool = False) -> List[Dict]:
        """
        Türkiye'nin tüm şehirlerinde arama yap
        
        Args:
            kategori: İşletme kategorisi
            ulke: Ülke adı
            limit_per_sehir: Her şehir için maksimum sonuç
            telefon_filtre: Sadece telefonu olanları getir
        
        Returns:
            Tüm şehirlerden toplanan işletme bilgileri
        """
        tum_sonuclar = []
        
        for sehir in config.TURKIYE_SEHIRLERI:
            print(f"{sehir} aranıyor...")
            sonuclar = self.isletme_ara(
                sehir=sehir,
                ulke=ulke,
                kategori=kategori,
                limit=limit_per_sehir,
                telefon_filtre=telefon_filtre
            )
            tum_sonuclar.extend(sonuclar)
            
            # Rate limit için bekleme
            time.sleep(0.5)
        
        return tum_sonuclar

