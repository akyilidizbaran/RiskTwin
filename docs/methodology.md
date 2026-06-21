# Metodoloji

## Genel Yaklaşım

RiskTwin, heuristic + ML hibrit bir tasarım kullanır:
- **Bugün:** Kural tabanlı heuristic skorlama (çalışır MVP)
- **Yarın:** Supervised ML modeli (veri toplandığında)

## 1. Veri Akışı (Data Ingestion)

```
AFAD CSV → load_hazard_data()
Bina CSV → load_building_data()
GeoJSON  → load_buildings_geojson()
                    ↓
            Veri Doğrulama
            (kolon kontrolü, tip düzeltme)
                    ↓
            Birleştirme (merge)
                    ↓
         Skorlama / Feature Engineering
```

- Eksik dosyalarda fallback demo veri üretilir
- Uygulama hiçbir durumda crash olmaz
- Veri kaynağı (gerçek/demo) metadata'da belirtilir

## 2. Feature Engineering

### Sayısal Özellikler
- `building_age`: Doğrudan + normalize (0-1)
- `floor_count`: Doğrudan + normalize (0-1)
- `hazard_score`: Doğrudan + normalize (0-1)

### Kategorik Encoding
- **Ordinal:** Zemin sınıfı (ZA=0, ..., ZF=5), taşıyıcı sistem (perde=0, ..., yığma=4)
- **One-hot:** Taşıyıcı sistem ve zemin sınıfı (ML modeli için)
- **Binary:** Mevcut bina (0/1)

### Heuristic Alt Skorlar (feature olarak)
- `soil_risk_score`: Zemin sınıfından türetilmiş 0-100 skor
- `system_risk_score`: Taşıyıcı sistemden türetilmiş 0-100 skor

## 3. Heuristic Skorlama

Ağırlıklı toplam formülü:
```
risk = Σ(weight_i × sub_score_i)
```

Her alt skor bağımsız olarak 0-100'e normalize edilir. Ağırlıklar uzman görüşüne dayalı olarak belirlenmiştir ve konfigürasyondan değiştirilebilir.

## 4. ML Pipeline (Training-Ready)

```
Ham Veri → Feature Engineering → encode_features()
                                      ↓
                              prepare_training_data()
                                      ↓
                              train_test_split (75/25)
                                      ↓
                    ┌─── Logistic Regression
                    ├─── Random Forest
                    └─── XGBoost (opsiyonel)
                                      ↓
                              Metrikler (acc, f1)
                                      ↓
                    En iyi model → models/risk_model.pkl
```

- Heuristic skorlar bootstrap label olarak kullanılır
- Gerçek etiketli veri geldiğinde aynı pipeline ile supervised eğitim yapılır
- `predict.py` model varsa kullanır, yoksa heuristic'e fallback eder

## 5. Açıklanabilirlik (Explainability)

### Kural Tabanlı Yaklaşım
- Her alt skor eşik tabanlı Türkçe açıklamaya sahip
- En yüksek 3 risk faktörü vurgulanır
- Senaryo karşılaştırmalarında delta açıklaması üretilir

### İleriki Adım
- SHAP (SHapley Additive exPlanations) entegrasyonu
- Feature importance görselleştirmesi
- Counterfactual açıklamalar ("bu bina güçlendirilseydi...")

## 6. Senaryo Motoru

```
Base Parametreler → evaluate_building()
                          ↓
                    base_risk_score
                          ↓
Override Parametreler → evaluate_building()
                          ↓
                    new_risk_score
                          ↓
              delta = new - base → recommendation
```

Öntanımlı senaryolar:
1. Güçlendirme (taşıyıcı sistem değişimi)
2. Kat azaltma
3. Zemin iyileştirme
4. Tam güçlendirme paketi

Kullanıcı tanımlı özel senaryolar da desteklenir.
