# Yol Haritası

## Faz 1: MVP (Bugün)
- [x] Heuristic skorlama motoru
- [x] Streamlit dashboard (harita, skor kartları, grafikler)
- [x] Senaryo karşılaştırma
- [x] Türkçe açıklanabilir çıktı
- [x] Demo veri seti (5 İstanbul lokasyonu)
- [x] ML training-ready altyapı
- [x] Sentetik GeoJSON katmanlar
- [x] Testler ve dokümantasyon

## Faz 2: Gerçek Geospatial Entegrasyon
- [ ] AFAD tehlike haritası otomatik entegrasyonu
- [ ] Overpass API ile gerçek OSM bina verisi
- [ ] Geofabrik PBF extract işleme
- [ ] Çoklu şehir desteği (Ankara, İzmir)
- [ ] PostGIS / geospatial veritabanı
- [ ] Mahalle/ilçe bazlı toplu risk taraması

## Faz 3: Supervised Model Training
- [ ] Hasar etiketli veri toplama (geçmiş deprem kayıtları)
- [ ] SHAP tabanlı model açıklanabilirliği
- [ ] Hiperparametre optimizasyonu
- [ ] Cross-validation ve model karşılaştırma
- [ ] Model versiyonlama (MLflow)
- [ ] A/B test: heuristic vs ML performansı

## Faz 4: BIM / TUCBS / Genişleme
- [ ] TUCBS WFS/WMS servis entegrasyonu
- [ ] Belediye açık veri portalları
- [ ] BIM (IFC) dosya okuma
- [ ] Zemin etüdü verisi entegrasyonu
- [ ] MTA jeoloji haritaları
- [ ] Çok kullanıcılı erişim ve yetkilendirme
- [ ] API layer (FastAPI)
- [ ] CI/CD pipeline
