# Skorlama Mantığı

## Risk Skoru Formülü

```
risk_score = hazard_score × 0.30
           + soil_score   × 0.25
           + age_score    × 0.15
           + floor_score  × 0.15
           + system_score × 0.15
```

Tüm alt skorlar 0-100 aralığında normalize edilmiştir. Nihai risk skoru da 0-100 aralığındadır.

## Ağırlık Gerekçeleri

| Faktör | Ağırlık | Gerekçe |
|--------|---------|---------|
| Deprem Tehlikesi | %30 | Lokasyonun sismik aktivitesi en temel belirleyicidir |
| Zemin Sınıfı | %25 | Zemin etkisi yapısal hasarı doğrudan güçlendirir/zayıflatır |
| Bina Yaşı | %15 | Yapım yılı yönetmelik uyumluluğunu belirler |
| Kat Sayısı | %15 | Yükseklik arttıkça deprem kuvvetleri artar |
| Taşıyıcı Sistem | %15 | Sistem türü performans kapasitesini belirler |

## Heuristic Mapping

### Tehlike Skoru
- Düşük (low): 20
- Orta (medium): 50
- Yüksek (high): 80
- Veya doğrudan 0-100 AFAD skoru kullanılır

### Zemin Sınıfı (TBDY 2018)
| Sınıf | Skor | Açıklama |
|-------|------|----------|
| ZA | 10 | Sağlam kaya |
| ZB | 20 | Kaya |
| ZC | 50 | Sıkı zemin |
| ZD | 70 | Yumuşak zemin |
| ZE | 85 | Zayıf zemin |
| ZF | 95 | Özel araştırma gerektiren |

### Bina Yaşı
| Aralık | Skor | Gerekçe |
|--------|------|---------|
| 0-10 yıl | 20 | TBDY 2018 sonrası |
| 10-25 yıl | 50 | 1998-2018 arası yönetmelikler |
| 25+ yıl | 80 | 1998 öncesi veya daha eski |

### Kat Sayısı
| Aralık | Skor |
|--------|------|
| 1-3 | 20 |
| 4-7 | 50 |
| 8+ | 80 |

### Taşıyıcı Sistem
| Sistem | Skor |
|--------|------|
| Betonarme Perde | 25 |
| Çelik | 30 |
| Betonarme Çerçeve | 55 |
| Prefabrik | 65 |
| Yığma | 85 |

## Risk Bandları

| Skor Aralığı | Band | Renk |
|---------------|------|------|
| 0-39 | Düşük | Yeşil |
| 40-64 | Orta | Turuncu |
| 65-100 | Yüksek | Kırmızı |

## Neden Heuristic Yaklaşım?

1. **Veri kısıtı:** Etiketli eğitim verisi henüz mevcut değil
2. **Açıklanabilirlik:** Heuristic kurallar doğrudan açıklanabilir
3. **Hız:** MVP için model eğitimi gerektirmeden çalışır
4. **Doğrulanabilirlik:** Uzmanlar ağırlıkları ve eşikleri doğrudan gözden geçirebilir

## ML ile Nasıl Geliştirilir?

1. Gerçek hasar/risk etiketli veri toplanır (geçmiş deprem verileri, hasar tespit raporları)
2. Heuristic skorlar baseline olarak kullanılır
3. Supervised model eğitilir (Random Forest, XGBoost)
4. Model performansı heuristic ile karşılaştırılır
5. Model daha iyi performans gösterirse heuristic'in yerini alır
6. Her durumda açıklanabilirlik katmanı (SHAP, feature importance) korunur
