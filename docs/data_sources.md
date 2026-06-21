# Veri Kaynakları

## Bugün Gerçekten Kullanılan Veriler

### 1. AFAD Deprem Tehlike Verisi
- **Kullanım:** Hazard input (tehlike girdisi)
- **Durum:** 5 İstanbul lokasyonu için manuel hazırlanmış örnek veri
- **Dosya:** `data/external/hazard_samples.csv`
- **Not:** AFAD'dan otomatik çekme yerine, 1. derece deprem bölgesi İstanbul ilçeleri için gerçekçi tehlike skorları atanmıştır
- **İleri adım:** AFAD interaktif harita veya API entegrasyonu

### 2. OSM / Geofabrik Geospatial Veri
- **Kullanım:** Bina footprint, yol ağı, POI, mahalle sınırları
- **Durum:** 5 lokasyon etrafında sentetik ama gerçekçi GeoJSON üretilmiştir
- **Dosyalar:**
  - `data/processed/buildings.geojson`
  - `data/processed/roads.geojson`
  - `data/processed/pois.geojson`
  - `data/processed/neighborhood_boundary.geojson`
- **Not:** Sentetik veri olarak işaretlenmiştir
- **İleri adım:** Overpass API ile gerçek OSM verisi çekme veya Geofabrik extract indirme

### 3. Kullanıcı Bina Girdileri
- **Kullanım:** Bina parametreleri (yaş, kat, sistem, zemin vb.)
- **Durum:** 12 örnek kayıt üretilmiştir
- **Dosya:** `data/processed/demo_building_inputs.csv`

## Referans Olarak Eklenen Veriler

### 4. TÜİK ADNKS (Opsiyonel)
- **Kullanım:** Nüfus yoğunluğu bağlam verisi, etki potansiyeli
- **Durum:** Örnek şema hazırlanmıştır, gerçek TÜİK verisiyle doldurulabilir
- **Dosya:** `data/external/population_context.csv`
- **Neden opsiyonel:** TÜİK verisi doğrudan API ile zor erişilmektedir; MVP için risk skoruna doğrudan girdi değildir ancak bağlam ve önceliklendirme için kullanılabilir

### 5. TUCBS (Referans)
- **Kullanım:** Coğrafi veri altyapısı referansı
- **Durum:** Doğrudan canlı entegrasyon yapılmamıştır
- **Not:** TUCBS, Türkiye Ulusal Coğrafi Bilgi Sistemi olarak ileriki genişleme için önemli bir referans kaynaktır. Kadastro, zemin, altyapı katmanları gibi veriler TUCBS uyumlu mimaride entegre edilebilir
- **İleri adım:** WFS/WMS servisleri üzerinden katman entegrasyonu

## Zemin Verisi Stratejisi
Zemin sınıfı verisi (TBDY 2018 ZA-ZF) otomatik erişimi bugün için zordur. MVP'de kullanıcı girdisi olarak alınmaktadır. İleriki fazlarda:
- MTA zemin haritaları
- Belediye zemin etüdü verileri
- TUCBS zemin katmanları
entegre edilebilir.
