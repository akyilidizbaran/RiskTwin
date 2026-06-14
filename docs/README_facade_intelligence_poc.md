# Facade Intelligence POC Planı

Bu belge, RiskTwin'in yeni görsel yapay zeka hattını tanımlar. Amaç, dış cephe görüntülerinden yapı envanterinde eksik kalan bilgileri çıkarmak ve bunları RiskTwin'in risk önceliklendirme kararına kontrollü biçimde bağlamaktır.

## 1) Problem Tanımı

Türkiye'de yapı envanteri birçok yerde eksik veya güncel değildir. Bir binanın yapı yaşı, kat sayısı, taşıyıcı sistem sınıfı, zemin kat düzensizliği veya görsel bakım durumu çoğu zaman merkezi ve erişilebilir bir veri tabanında yer almaz.

Bu eksikliği klasik yöntemle kapatmak için:

- saha ekiplerinin bina bina dolaşması gerekir
- veri toplama maliyeti artar
- süre uzar
- güncellik sorunu devam eder
- kentsel dönüşüm önceliklendirmesi yavaşlar

RiskTwin'in yeni POC hattı, bu boşluğu görüntü işleme ve yapay zeka ile azaltmayı hedefler.

## 2) POC'nin Ana Cümlesi

RiskTwin, dış cephe görüntülerinden yapı envanterinde eksik kalan kritik bina özelliklerini tahmin eden, yalnızca yüksek güvenli sonuçları kabul eden ve bu sonuçları hazard bağlamı ile birleştirerek kentsel dönüşüm ve inceleme önceliği üreten bir Digital Twin karar destek katmanı geliştirmeyi hedefler.

## 3) Ne Yapıyoruz?

POC kapsamında şunları yapacağız:

- açık veya izinli street-level imagery kullanacağız
- binaları çoklu açıdan görsel olarak değerlendireceğiz
- bina görüntüsünü bina kimliğiyle eşleştirmeyi çözeceğiz
- dış cepheden tahmin edilebilir yapı sinyallerini çıkaracağız
- her tahmine güven skoru ekleyeceğiz
- düşük güvenli tahminleri kabul etmeyeceğiz
- tahminleri RiskTwin'in risk motoruna feature olarak bağlayacağız

## 4) Ne Yapmıyoruz?

POC kapsamında şunları iddia etmeyeceğiz:

- tek başına görüntüden kesin deprem dayanımı belirlemek
- otomatik yıkım veya güçlendirme kararı vermek
- her bina için zorla tahmin üretmek
- düşük güvenli çıktıları risk skoruna sessizce dahil etmek
- görüntüden bilinmesi mümkün olmayan mühendislik detaylarını uydurmak

## 5) İki Aşamalı Sistem

Tek aşamalı "görüntüden yıkım tahmini" yaklaşımı bilimsel ve ürünsel olarak zayıftır. Bu nedenle sistem iki aşamalı kurulacaktır.

### Aşama 1 - Görsel Envanter ve Kırılganlık Proxy Tahmini

Model dış cepheden görülebilir özellikleri tahmin eder:

- kat sayısı
- yapım dönemi veya yaş bandı
- yapı tipolojisi proxy'si
- taşıyıcı sistem proxy'si
- soft-story veya açık zemin kat riski
- görsel bozulma veya bakım durumu
- ticari zemin kat / karma kullanım proxy'si
- cephe düzeni ve morfolojik yapı sinyalleri

Bu aşamada çıktı bir nihai risk kararı değildir. Çıktı, RiskTwin'in daha sonra kullanacağı zenginleştirilmiş envanter bilgisidir.

### Aşama 2 - RiskTwin Karar Katmanı

Aşama 1'den gelen feature'lar şu bağlamlarla birleştirilir:

- hazard bağlamı
- fay yakınlığı
- jeolojik ve zemin proxy'leri
- mevcut belediye veya açık bina envanteri
- post-event observed outcome etiketleri
- bölge ve mahalle bağlamı

Bu birleşimden şu çıktılar üretilir:

- enriched risk score
- inspection priority
- warning level
- manual review requirement
- hayat koridoru ve kentsel dönüşüm önceliklendirme sinyali

## 6) Confidence-aware Davranış

Model her bina için tahmin vermek zorunda değildir. RiskTwin'in yeni AI katmanı şu ilkeye göre çalışır:

> Tahmin güvenilir değilse, sistem bunu açıkça söyler ve manuel incelemeye yönlendirir.

Bu nedenle her model çıktısı şu alanlarla taşınır:

- `prediction_value`
- `prediction_confidence`
- `accepted_prediction_flag`
- `manual_review_required`
- `uncertainty_reason`
- `source_type`

Düşük güvenli örneklerde varsayılan çıktı:

- `unknown`
- `manual_review`

Bu karar hem teknik hem ürün tarafından birlikte tanımlanacaktır. Teknik tarafta confidence eşiği metriklerle ölçülecek, ürün tarafında ise kullanıcıya hangi seviyede güven gösterileceği belirlenecektir.

## 7) İlk POC Kapsamı

İlk POC dar ve savunulabilir tutulacaktır.

| Başlık | Karar |
|---|---|
| Şehir | İstanbul |
| Bina sayısı | Yaklaşık 100 bina |
| Veri tipi | Açık street-level imagery veya kurumsal izinli görüntüler |
| Görüntüleme | Çoklu açı |
| Görsel-bina eşleme | Biz çözeceğiz |
| Tarih bilgisi | Yapı yaşı ve label uyumu için önemli |
| Nihai karar | Uzmanlarda kalacak |
| POC çıktısı | Skor, confidence, öncelik ve açıklama |

## 8) Hedef Değişkenler

İlk POC için aday hedefler:

- `storey_count`
- `construction_period_band`
- `typology_proxy`
- `structural_system_proxy`
- `soft_story_risk`
- `visual_degradation_score`
- `ground_floor_commercial_proxy`
- `visual_vulnerability_proxy`

İlk fazda en gerçekçi minimal hedef seti:

- kat sayısı
- yapım dönemi bandı
- soft-story veya görsel düzensizlik riski
- görsel kırılganlık proxy'si

Doğrudan `collapse` veya `demolition` kararı üretimi bu fazda kapsam dışıdır. Eğer yıkım verisi kullanılacaksa bu bilgi, modelin nihai kararı değil, post-event observed outcome olarak etiket stratejisinde yer alır.

## 9) Model Mimarisi İçin İlk Varsayım

İlk POC için önerilen teknik yaklaşım:

- görüntü encoder modeli
- çoklu görüntü birleştirme
- bina bazlı aggregation
- tabular hazard ve lokasyon feature'larıyla late fusion
- confidence estimation
- selective prediction

Aday model aileleri:

- CNN tabanlı baseline
- Vision Transformer tabanlı encoder
- CLIP benzeri pretrained visual encoder
- tabular fusion için gradient boosting veya shallow MLP

İlk POC'de aşırı karmaşık uçtan uca sistem kurmak yerine, önce görüntüden envanter çıkarımı doğrulanmalıdır.

## 10) Değerlendirme Metrikleri

Kullanıcı nihai başarı metriğini daha sonra netleştirecek. Şu an aday metrikler:

- F1
- macro F1
- accepted prediction precision
- coverage
- calibration
- manual review rate
- false reassurance risk

Kullanıcının ön hedefi, özellikle pozitif/riskli durumu yakalayabilen bir sistem kurmaktır. Bu nedenle sadece accuracy yeterli olmayacaktır. F1 ve high-confidence precision birlikte değerlendirilmelidir.

## 11) Ürün KPI'ları

POC teknik başarıdan ibaret olmayacaktır. Aşağıdaki ürün KPI'ları da izlenecektir:

- envanter doluluk oranındaki artış
- manuel inceleme ihtiyacındaki azalma
- yüksek öncelikli bina yakalama oranı
- önceliklendirme süresindeki azalma
- kullanıcıya açıklanabilir çıktı oranı
- unknown/manual review oranı

## 12) Hayat Koridorları ve Kentsel Dönüşüm

RiskTwin'in yeni hattı yalnız bina skoru üretmekle sınırlı değildir. Eğer bir mahalle veya bölge yoğun yapısal kırılganlık gösteriyorsa, sistem şu kararları destekleyebilir:

- hangi sokak veya aksların önce ele alınması gerektiği
- hangi bölgede hızlı kentsel dönüşüm ihtiyacı olduğu
- afet sonrası erişim ve tahliye açısından hangi aksların kritik olduğu
- yüksek riskli kümelerin nerede yoğunlaştığı

Bu kapsamda `hayat koridoru`, yüksek riskli bölgelerde afet sonrası erişim, tahliye ve müdahale kabiliyetini artırmak için önceliklendirilmiş dönüşüm aksı olarak ele alınacaktır.

## 13) POC Sonrası Ürünleşme

POC başarılı olursa yeni katman RiskTwin'e şu şekilde eklenecektir:

- bina kartında tahmin edilmiş envanter alanları
- her tahmin için confidence
- resmi / açık / predicted / unknown ayrımı
- visual model kaynaklı feature etiketi
- manual review flag
- kentsel dönüşüm öncelik haritası

## 14) Açık Sorular

Bu belge ilerledikçe şu sorular cevaplanmalıdır:

- İstanbul içinde ilk POC bölgesi neresi olacak?
- İlk 100 bina nasıl seçilecek?
- Açık imagery kaynağı yeterli mi?
- Kurumsal izinli görüntü erişimi mümkün mü?
- Bina-görüntü eşleme hangi geometriyle yapılacak?
- İlk hedef değişkenler kesin olarak hangileri olacak?
- F1 dışında hangi metrik zorunlu olacak?
- Hayat koridoru çıktısı MVP'de görsel olarak gösterilecek mi?
