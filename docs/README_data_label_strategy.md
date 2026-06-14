# Veri, Etiket ve Lisans Stratejisi

Bu belge, RiskTwin'in görsel envanter zenginleştirme hattında kullanılacak veri kaynaklarını, etiket yaklaşımını, lisans sınırlarını ve doğrulanması gereken riskleri tanımlar.

## 1) Ana Veri Problemi

RiskTwin'in yeni araştırma hattı, eksik yapı envanterini dış cephe görüntülerinden zenginleştirmeyi amaçlar. Bunun için üç veri ailesi gerekir:

- bina görüntüsü
- bina kimliği ve konumu
- afet sonrası gözlenmiş sonuç veya yapı skoru

Bu üç veri aynı bina üzerinde güvenilir biçimde birleşmezse model yanlış ilişki öğrenebilir.

## 2) Görsel Veri Kaynakları

İlk tercih sırası:

1. açık street-level imagery
2. kurumsal izinli görüntüler
3. kendi toplanan saha görüntüleri
4. sınırlı ve hukuken güvenli test/referans amaçlı üçüncü taraf görüntüler

Google Street View veya benzeri kapalı lisanslı kaynaklar ana eğitim veri kaynağı olarak konumlandırılmayacaktır. Bu kaynaklar ancak lisans sınırları net biçimde doğrulanırsa ve yalnız uygun kullanım kapsamında değerlendirilecektir.

## 3) Görüntüleme Stratejisi

POC çoklu açı yaklaşımı kullanacaktır.

Beklenen veri yapısı:

| Alan | Açıklama |
|---|---|
| `building_id` | Bina veya aday bina anahtarı |
| `image_id` | Görüntü anahtarı |
| `view_angle` | Görselin açı bilgisi |
| `capture_date` | Görsel tarihi |
| `lat` / `lon` | Görüntü veya pano konumu |
| `source` | Açık, kurumsal veya kullanıcı toplama kaynağı |
| `license_status` | Kullanım lisansı |

Çoklu açı önemlidir çünkü tek cephe:

- kat sayısını saklayabilir
- zemin katı göstermeyebilir
- bina girişini veya cephe bütünlüğünü kaçırabilir
- ağaç, araç veya tabela ile kapanabilir

## 4) Bina-Görüntü Eşleme

Görseller bina bazında hazır eşlenmiş varsayılmayacaktır. Bu eşlemeyi sistem çözecektir.

Olası eşleme sinyalleri:

- bina footprint poligonu
- adres veya parsel bilgisi
- görüntü çekim koordinatı
- kamera yönü
- pano veya görüntü tarihi
- cephe görünürlüğü

Her eşleme için confidence tutulmalıdır:

- `image_building_match_confidence`
- `match_method`
- `match_review_required`

Yanlış görüntü-bina eşleşmesi, modelin tüm karar zincirini bozar. Bu yüzden eşleme confidence'ı model tahmin confidence'ından ayrı tutulmalıdır.

## 5) Etiket Stratejisi

Kullanılacak ana etiket tipi:

> `post-event observed outcome`

Bu, deprem sonrası gözlenen yıkım, ağır hasar veya yapı performansı bilgisidir. Etiket nihai mühendislik truth'u gibi değil, gözlenmiş sonuç katmanı olarak ele alınacaktır.

## 6) Aday Afet Veri Kaynakları

Şu an kullanıcı tarafından belirtilen adaylar:

- 6 Şubat depremleri sonrası yıkılan veya hasar gören bina/bölge verileri
- bulunabilirse 1999 Marmara depremi verileri
- bulunabilirse Van depremi verileri

Not: Van depremi kapsamı, yılı ve veri erişim durumu ayrıca doğrulanmalıdır.

## 7) Etiket Granülerliği

Mevcut varsayım:

- bazı veriler bina bazında olmayabilir
- bazı veriler bölge veya mahalle düzeyinde olabilir
- 6 Şubat verileri özellikle bölge bazlı olabilir

Bu nedenle etiketler üç sınıfa ayrılmalıdır:

| Sınıf | Anlam |
|---|---|
| `hard_label` | Bina bazlı ve güvenilir etiket |
| `weak_evidence` | Dolaylı, bölgesel veya düşük kesinlikli kanıt |
| `post_event_observed_outcome` | Afet sonrası gözlenen sonuç |

Modelleme sırasında bu etiketler aynı ağırlıkta kullanılmamalıdır.

## 8) Zaman Uyumu

Kullanıcı şu an pre-event görüntü ile post-event label tarih uyumunu bilmiyor. Bu önemli bir açık sorudur.

Takip edilmesi gereken tarih alanları:

- `image_capture_date`
- `inventory_date`
- `event_date`
- `damage_observation_date`
- `retrofit_or_change_date`

Eğer görüntü tarihi ile afet tarihi arasında yapı değişmişse, label gürültülü hale gelir.

Bu nedenle her örneğe zaman uyumu statüsü eklenmelidir:

- `aligned`
- `possibly_misaligned`
- `unknown`
- `invalid_for_training`

## 9) Veri Kalitesi Riskleri

Ana riskler:

- görüntüde bina tam görünmüyor
- görüntü yanlış binaya eşleniyor
- label bölge bazında ama model bina bazında öğreniyor
- görüntü afet öncesi ama bina afet öncesinde değişmiş
- farklı şehirlerden gelen veriler Türkiye içi domain gap yaratıyor
- model dış cephe stilini gerçek kırılganlık sanıyor

Bu riskler için her örnekte provenance tutulmalıdır.

## 10) Lisans Politikası

Lisans stratejisi net olmalıdır:

- ana eğitim verisi lisanslı ve tekrar üretilebilir olmalıdır
- kapalı platform görüntüleri ana training set olarak kullanılmamalıdır
- üçüncü taraf görüntüler için kullanım şartları ayrıca doğrulanmalıdır
- kurumsal görüntü varsa izin kapsamı yazılı olmalıdır
- model çıktısının ticari veya kamu kullanımına uygunluğu ayrıca kontrol edilmelidir

README ve ürün ekranlarında veri kaynağı şeffaflığı korunmalıdır.

## 11) Feature Olarak Kullanım

Görsel modelden gelen tahminler RiskTwin'de feature olarak kullanılacaktır. Ancak bu feature'ların görsel model kaynaklı olduğu açıkça belirtilecektir.

Örnek alanlar:

- `predicted_storey_count`
- `predicted_construction_period`
- `predicted_typology_proxy`
- `predicted_soft_story_risk`
- `visual_vulnerability_proxy`
- `visual_prediction_confidence`
- `visual_source_type`

Bu alanlar resmi envanter alanlarıyla karıştırılmayacaktır.

## 12) Kullanıcıya Gösterim

Digital Twin ekranında her alanın kaynağı görünür olmalıdır:

- `official`
- `open`
- `predicted`
- `unknown`

Örnek:

| Alan | Değer | Kaynak | Güven |
|---|---|---|---|
| Kat sayısı | 6 | predicted | 0.82 |
| Yapım dönemi | 1990-2000 | predicted | 0.64 |
| Hazard skoru | 78 | official/open | 0.90 |
| Taşıyıcı sistem | unknown | unknown | - |

Bu şeffaflık, ürün güvenilirliği için zorunludur.

## 13) Backup Planları

| Risk | Plan A | Plan B | Plan C |
|---|---|---|---|
| Açık imagery yetersiz | Kurumsal izinli görüntüler | Kendi saha görüntüsü | Sınırlı manual test set |
| Bina bazlı label yok | Bölge bazlı weak evidence | Uzman etiketli küçük set | Sadece envanter tahmini |
| Zaman uyumu belirsiz | Tarihli imagery | Yakın dönem imagery | Time-alignment flag ile filtreleme |
| Domain gap yüksek | İstanbul odaklı POC | Şehir bazlı fine-tuning | Confidence threshold yükseltme |
| Eşleme hatası | Footprint + kamera yönü | Manuel audit subset | Low-confidence abstention |

## 14) İlk Cevaplanacak Sorular

- İstanbul POC için hangi alt bölge seçilecek?
- Açık imagery kaynağı pratikte yeterli mi?
- İlk 100 bina için görüntü-bina eşleme nasıl kurulacak?
- 6 Şubat verisi bina bazında mı, bölge bazında mı kullanılacak?
- 1999 ve Van verileri gerçekten erişilebilir mi?
- Hangi etiketler training, hangileri yalnız validation veya evidence olarak kullanılacak?
