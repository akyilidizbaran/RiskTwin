# RiskTwin

**Açıklanabilir deprem riski ve proje uygunluk karar desteği için geliştirilen dijital twin MVP'si**

> RiskTwin, deprem riski ve proje uygunluk kararlarını açıklanabilir skorlar, senaryo kıyası ve ML-ready mimariyle destekleyen bir karar destek platformudur. Hackathon kapsamında geliştirilen bu MVP; belediyeler, geliştiriciler ve teknik ekipler için kurumsal, izlenebilir, Türkiye odaklı ve ölçeklenebilir ön değerlendirme akışı sunar. MVP düzeyindedir

## Durum Notu

> **Paylaşım Notu**
>
> RiskTwin bir hackathon projesi olarak geliştirilmiştir. Bu repository, ürünün web uygulamasını ve demo akışını göstermek için hazırlanmış paylaşılabilir paketi içerir. Tüm dahili çalışma notları, tasarım iterasyonları, yardımcı araçlar ve bazı geliştirme varlıkları bu repoda yer almaz.

## RiskTwin Nedir?

RiskTwin; bina, parsel, deprem tehlikesi ve temel yapı parametrelerini tek karar yüzeyinde birleştiren bir ön değerlendirme platformudur. Amaç; mühendislik kararının yerine geçmek değil, doğru binayı, doğru projeyi ve doğru inceleme sırasını daha erken ve daha okunabilir biçimde belirlemektir.

Bu ürün özellikle şu soruya cevap vermek için tasarlanmıştır:

**"Bu yapı veya proje, mevcut koşullarda ne kadar riskli, ne kadar uygun ve ne kadar öncelikli?"**

## Neden Önemli?

Türkiye, yüksek sismik risk altında bulunan çok katmanlı bir yapı stoku ile karşı karşıya. Deprem tehlikesi, zemin koşulları, bina yaşı, taşıyıcı sistem ve müdahale seçenekleri çoğu zaman parçalı değerlendiriliyor. Sonuç olarak:

- karar süreçleri yavaşlıyor
- uzman bağımlılığı artıyor
- saha önceliklendirmesi zorlaşıyor
- proje ve güçlendirme alternatifleri sistematik kıyaslanamıyor

RiskTwin bu boşluğu kurumsal karar desteği odağıyla kapatır.

## Öne Çıkan 3 Değer

### 1. Açıklanabilirlik

RiskTwin yalnızca skor üretmez; riskin neden yükseldiğini, hangi faktörlerin öne çıktığını ve hangi kararın neden önerildiğini görünür kılar.

### 2. Kurumsal Karar Desteği

Platform belediyeler, geliştiriciler ve teknik değerlendirme ekipleri için ortak bir karar dili üretir. Amaç estetik bir dashboard değil, operasyonel olarak kullanılabilir bir değerlendirme katmanıdır.

### 3. ML-Ready Mimari

Heuristic-first yaklaşım ile hemen çalışabilir durumdadır; veri derinliği arttıkça supervised model olgunlaşmasına açık bir mimari üzerine kuruludur.

## Kim İçin Geliştirildi?

RiskTwin'in ana kullanıcı kitlesi:

- Belediye risk değerlendirme ve kentsel dönüşüm ekipleri
- Büyük geliştiriciler ve proje ekipleri
- Yapı denetim ve teknik inceleme ekipleri
- Afet yönetimi ve saha önceliklendirme karar vericileri
- Jüri / hackathon değerlendirme kurulları

## Web Uygulaması Neyi Gösteriyor?

RiskTwin şu anda beş ana ekran üzerinden ürün akışını gösterir:

### Proje Tanıtımı

Ürünün neden var olduğunu, problemi nasıl çerçevelediğini, neyi çözdüğünü ve neden şimdi önemli olduğunu anlatan giriş ekranıdır.

### Risk Analizi

Bir yapı için parametre girişi, harita bağlamı, risk skoru, proje uygunluk skoru ve inceleme önceliği aynı akışta gösterilir.

### Senaryo Karşılaştırma

Güçlendirme, kat azaltma veya alternatif yapı kararlarının risk ve uygunluk üzerindeki etkisi karşılaştırmalı olarak sunulur.

### Veri ve Metodoloji

Skorlama mantığı, veri kaynağı görünürlüğü, ağırlık dağılımı ve ML hazırlık seviyesi teknik denetlenebilirlik odağıyla açıklanır.

### Hakkında

Ürünün stratejik amacı, hedef kullanıcıları, mimari yaklaşımı, teknik sınırları ve gelişim yönü özetlenir.

## Ürün Akışı

RiskTwin'in karar mantığı basit ama güçlü bir akış üzerine kuruludur:

1. Lokasyon ve yapı parametreleri alınır
2. Deprem tehlikesi ve yapısal kırılganlık birlikte değerlendirilir
3. Risk, uygunluk ve inceleme önceliği hesaplanır
4. Doğal dil açıklama ile karar gerekçesi sunulur
5. Alternatif senaryolar kıyaslanır
6. Sonuç karar vericinin hızlı okuyacağı bir kurumsal arayüzde gösterilir

## Teknik Olarak Nasıl Çalışır?

RiskTwin mimarisi dört ana katmandan oluşur:

```text
Kullanıcı Katmanı
Streamlit dashboard + Folium harita + Plotly görselleştirme

İş Mantığı Katmanı
Scoring engine + scenario engine + explainability katmanı

ML Katmanı
Feature engineering + eğitim pipeline + predict/fallback akışı

Veri Katmanı
Deprem tehlikesi + geospatial katmanlar + kullanıcı girdisi + demo veri
```

### Temel Teknik Bileşenler

- `Streamlit`: çok sayfalı ürün arayüzü
- `Folium`: lokasyon ve risk bağlamı harita katmanı
- `Plotly`: skor ve karşılaştırma görselleştirmeleri
- `Heuristic scoring engine`: açıklanabilir ön risk değerlendirmesi
- `Scenario engine`: alternatif müdahale ve proje senaryoları
- `Explainability layer`: Türkçe doğal dil açıklama üretimi
- `ML pipeline`: feature engineering, eğitim ve prediction katmanı

## Skorlama Yaklaşımı

RiskTwin MVP sürümünde riski aşağıdaki temel faktörler üzerinden değerlendirir:

| Faktör | Ağırlık | Rol |
|--------|---------|-----|
| Deprem Tehlikesi | %30 | Lokasyonun sismik tehlike düzeyi |
| Zemin Sınıfı | %25 | Zemin koşullarının risk etkisi |
| Bina Yaşı | %15 | Yönetmelik dönemi ve yaş kaynaklı kırılganlık |
| Kat Sayısı | %15 | Yapısal talep ve taşıma zorlanması |
| Taşıyıcı Sistem | %15 | Sistem dayanımı ve davranış kapasitesi |

**Risk bantları:** `0-39 Düşük`, `40-64 Orta`, `65-100 Yüksek`

## Veri Durumu

RiskTwin MVP mantığında kullanılan veri aileleri:

- deprem tehlike verisi
- geospatial katmanlar
- kullanıcı tarafından girilen yapı parametreleri
- bağlam / nüfus / referans katmanları
- model eğitimi için hazırlanan demo ve sentetik veri akışları

> Bu repository içinde yalnızca web uygulamasını çalıştırmak için gerekli demo ve örnek veri varlıkları paylaşılmıştır. Daha geniş veri hazırlık süreci ve dahili çalışma materyalleri bu repoya dahil edilmemiştir.

## Tasarım ve Deneyim Yaklaşımı

RiskTwin yalnızca teknik olarak değil, deneyim açısından da kurumsal karar vericilere göre tasarlanmıştır.

Arayüz yaklaşımı:

- premium dark enterprise dashboard dili
- yüksek bilgi yoğunluğunu sakin hiyerarşiyle sunan düzen
- JetBrains Mono + IBM Plex Sans temelli teknik tipografi
- harita, skor ve açıklama bloklarını tek karar ailede birleştiren kompozisyon
- gösterişli AI görselleri yerine güven veren ürün dili

Tasarım tarafında Stitch destekli bir **design workflow exists** yaklaşımı bulunmaktadır. Bu workflow, ürün ekranlarının görsel yönünü rafine etmek için kullanılmıştır; ancak erişim ve entegrasyon detayları bu README içinde paylaşılmamaktadır.

## Klasör Yapısı

```text
risktwin/
├── app/
│   ├── app.py
│   ├── pages/
│   │   ├── home.py
│   │   ├── risk_analysis.py
│   │   ├── scenario.py
│   │   ├── methodology.py
│   │   └── about.py
│   └── components/
├── src/
├── data/
├── models/
├── README.md
└── requirements.txt
```

## Kurulum ve Lokal Çalıştırma

> Bu repo, paylaşılan web uygulama paketini lokal olarak ayağa kaldırmak için yeterli dosyaları içerir.

```bash
git clone <REPO_URL>
cd risktwin
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py
```

## Takım

**Takım Adı:** Aerolith Systems

- **Baran Akyıldız** — Teknik Lider
- **Elif Sena Önsöz** — Geospatial & Data Engineer
- **Elif Güngen** — AI Application Engineer
- **Burak Kılıç** — Mechanical Systems & Technical Validation Lead

## Gelecek Vizyonu

RiskTwin'in yarışma sonrası büyüme yönleri:

- çoklu şehir desteği
- gerçek veri entegrasyonları
- supervised model olgunlaşması
- explainable AI derinleşmesi
- toplu tarama ve operasyonel kullanım senaryoları
- API / backend katmanı
- daha geniş kurumsal entegrasyon kabiliyeti

## Linkler

- **Website:** [PLACEHOLDER_WEBSITE_LINK](https://example.com/risktwin-website)
- **Canlı Demo:** [PLACEHOLDER_DEMO_LINK](https://example.com/risktwin-demo)
- **Video / Demo Sunumu:** [PLACEHOLDER_VIDEO_LINK](https://example.com/risktwin-video)
- **Sunum / Pitch Deck:** [PLACEHOLDER_PITCH_LINK](https://example.com/risktwin-pitch)
- **İletişime Geç:** [PLACEHOLDER_CONTACT_LINK](https://example.com/risktwin-contact)

## Yayın Kontrol Listesi

GitHub'a pushlamadan önce şu maddeler kontrol edilmelidir:

- README içindeki placeholder linkler gerçek bağlantılarla güncellendi mi?
- Paylaşılmaması gereken dahili dosyalar repo dışında tutuldu mu?
- Gizli erişim bilgileri veya servis akışları README ve commit geçmişinde yer almıyor mu?
- Repo içeriği ile README'deki paylaşım kapsamı tutarlı mı?
- Public-facing açıklama metni ve repo açıklaması aynı mesaj ailesinde mi?

## Lisans

**All rights reserved**

Bu repository ve içindeki tüm proje çıktıları Aerolith Systems ve ilgili ekip üyelerinin kontrolündedir. Açık kaynak lisansı tanımlanmamıştır.
