# Ürün Kapsamı ve Digital Twin Karar Çerçevesi

Bu belge, RiskTwin'in yeni görsel AI katmanının ürün tarafında neye dönüşeceğini, hangi kullanıcı değerini üreteceğini ve hangi açık soruların cevaplanması gerektiğini tanımlar.

## 1) Ürün Konumu

RiskTwin bu fazda bir araştırma hattı olarak konumlanacaktır. Amaç doğrudan üretim sistemi kurmak değil, POC ile yapılabilirliği göstermek ve ürünleşebilir karar yüzeyini kanıtlamaktır.

Ürün konumu:

- araştırma hattı
- POC adayı
- ileride ürünleşme potansiyeli olan modül

## 2) Ana Değer Önerisi

RiskTwin'in yeni katmanı iki ana değer üretir:

- eksik yapı envanterini tamamlamak
- daha güvenilir risk önceliklendirmesi yapmak

Bu iki değer, kentsel dönüşüm ve afet hazırlığı için birleşik karar desteği sağlar.

## 3) Kentsel Dönüşüm Önceliklendirmesi

RiskTwin, bina bazlı tahminleri mahalle, sokak veya bölge ölçeğinde gruplayarak kentsel dönüşüm önceliği üretebilir.

Bu çıktı şu sorulara cevap verebilir:

- hangi binalar önce incelenmeli?
- hangi sokaklarda kırılganlık yoğunlaşıyor?
- hangi mahallelerde dönüşüm aciliyeti artıyor?
- hangi bölgelerde saha ekipleri önce çalışmalı?
- hangi alanlar afet sonrası erişim açısından riskli?

## 4) Hayat Koridorları

Hayat koridoru, yüksek riskli veya yoğun kırılganlık gösteren bölgelerde afet öncesi ve sonrası erişim, tahliye ve müdahale kabiliyetini artırmak için önceliklendirilmiş dönüşüm veya açılım aksı olarak tanımlanır.

RiskTwin bu kapsamda şunları destekleyebilir:

- yüksek risk kümelerini tespit etmek
- yıkılma veya erişim kapanma riski taşıyan yoğun dokuları işaretlemek
- dönüşüm önceliği yüksek aksları belirlemek
- müdahale, tahliye ve ulaşım sürekliliği için kritik sokakları öne çıkarmak

Bu modül nihai şehircilik kararını vermez. Karar vericiye veri destekli öncelik haritası sağlar.

## 5) Digital Twin'de Ne Görünecek?

Digital Twin ekranında bina kartı şu alanları taşımalıdır:

- bina kimliği
- konum ve geometri
- resmi envanter alanları
- açık veriden gelen alanlar
- görsel modelden tahmin edilen alanlar
- unknown/pending alanlar
- hazard bağlamı
- visual vulnerability proxy
- risk skoru
- inspection priority
- confidence ve provenance bilgisi
- manual review flag

Bu ekranın ana ilkesi:

> Kullanıcı yalnız sonucu değil, sonucun hangi veriyle ve ne kadar güvenle üretildiğini görmelidir.

## 6) Veri Kaynağı Şeffaflığı

Her alan şu statülerden biriyle gösterilecektir:

- `official`
- `open`
- `predicted`
- `unknown`

Bu ayrım özellikle görsel AI katmanında zorunludur. Çünkü predicted alanlar resmi veri gibi sunulmamalıdır.

## 7) Ürün Çıktıları

Yeni katman RiskTwin'e şu ürün çıktıları sağlar:

- `enriched_inventory_record`
- `visual_vulnerability_proxy`
- `inventory_completion_score`
- `inspection_priority`
- `manual_review_required`
- `urban_transformation_priority`
- `life_corridor_signal`
- `data_confidence_summary`

## 8) Karar Sınırı

RiskTwin şu kararları destekler:

- önceliklendirme
- tarama
- saha yönlendirme
- risk görünürlüğü
- veri eksikliği tespiti
- dönüşüm aday alanı belirleme

RiskTwin şu kararları tek başına vermez:

- yıkım kararı
- kesin güçlendirme kararı
- bina güvenlidir/güvensizdir hükmü
- nihai mühendislik onayı

## 9) Kullanıcı Rolleri

Ana kullanıcılar:

- belediye kentsel dönüşüm birimleri
- afet risk yönetimi ekipleri
- yapı envanteri ekipleri
- saha inceleme ekipleri
- teknik danışmanlar

İkincil kullanıcılar:

- büyük geliştiriciler
- site yönetimleri
- yatırım ve portföy ekipleri
- kamu karar vericileri

## 10) MVP Gösterimi

Kullanıcı İstanbul için ayrıca bir MVP gösterimi hazırlamak istiyor. Bu gösterim büyük olasılıkla şu parçaları içermelidir:

- 100 bina POC evreni
- her bina için görüntü veya görüntü placeholder'ı
- tahmin edilen birkaç envanter alanı
- confidence değeri
- official/open/predicted/unknown ayrımı
- RiskTwin risk ve öncelik çıktısı
- seçili bölge için kentsel dönüşüm veya hayat koridoru sinyali

Bu gösterim gerçek üretim doğruluğu iddia etmemelidir. Ama sistem mantığını ve ürün potansiyelini göstermelidir.

## 11) Sunumda Kullanılabilecek Ana Cümle

RiskTwin, eksik yapı envanterini dış cephe görüntülerinden zenginleştiren, bu bilgiyi hazard bağlamı ile birleştiren ve kentsel dönüşüm ile hayat koridoru planlaması için açıklanabilir önceliklendirme sağlayan bir Digital Twin karar destek sistemidir.

## 12) Açık Ürün Soruları

- MVP gösterimi İstanbul içinde hangi bölge üzerinden yapılacak?
- Hayat koridoru çıktısı harita üzerinde nasıl gösterilecek?
- Kentsel dönüşüm önceliği bina bazında mı, sokak bazında mı, mahalle bazında mı verilecek?
- Kullanıcı için hangi confidence seviyesi kabul edilebilir?
- Düşük confidence durumunda ekran dili nasıl olacak?
- Görsel modelden gelen feature'lar risk skoruna hangi ağırlıkla girecek?
- Risk skorunu görüntü modeli mi artıracak, yoksa yalnız inspection priority mi etkileyecek?
- Ürünün ilk kullanıcı ekranı bina kartı mı, harita mı, bölgesel öncelik paneli mi olacak?

## 13) Çalışma Sırası

Ürün kararı şu sırayla ilerlemelidir:

1. İstanbul POC bölgesini seç
2. İlk 100 bina evrenini tanımla
3. Görsel veri kaynağını doğrula
4. Hedef değişkenleri dondur
5. Confidence ve manual review kuralını tanımla
6. Digital Twin bina kartı alanlarını belirle
7. Hayat koridoru veya kentsel dönüşüm önceliği gösterimini tasarla
8. POC başarı kriterini netleştir
