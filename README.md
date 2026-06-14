# RiskTwin

**Açıklanabilir deprem riski, kentsel dönüşüm önceliklendirmesi ve görsel yapı envanteri zenginleştirme için Digital Twin karar destek platformu**

RiskTwin, Türkiye'deki eksik ve parçalı yapı envanteri problemini deprem riski bağlamında ele alır. Projenin yeni araştırma hattı, dış cephe görüntülerinden ve street-level imagery kaynaklarından yapı envanterinde eksik kalan kritik bilgileri çıkarmayı; bu bilgileri belediye envanteri, hazard bağlamı ve afet sonrası gözlem verileriyle birleştirerek daha kapsamlı bir Digital Twin ortamı kurmayı hedefler.

Bu repo iki şeyi birlikte taşır:

- Bugünkü `Streamlit` tabanlı RiskTwin MVP'si
- Yeni `Facade Intelligence` araştırma ve POC planı

## Ana Problem

Türkiye'de birçok bina, belediye yapı envanterlerinde eksik, güncel olmayan veya hiç bulunmayan bilgilerle temsil ediliyor. Bu eksikliği tamamen saha çalışmasıyla kapatmak pahalı, yavaş ve operasyonel olarak zor.

RiskTwin'in yeni odağı:

- görüntü işleme ve yapay zeka ile envanterde eksik kalan binaları ve bina özelliklerini tespit etmek
- bu çıktıları mevcut yapı envanteriyle birleştirmek
- mahalle, ada, parsel ve bina düzeyinde daha kapsamlı bir Digital Twin tabanı oluşturmak
- kentsel dönüşüm önceliklendirmesi ve hayat koridoru planlamasına karar desteği sağlamak

## Yeni Araştırma Hattı

Yeni hat doğrudan "bu bina yıkılır" kararı vermez. Amaç, dış cephe görüntülerinden görülebilir yapı sinyallerini çıkarıp bunları risk önceliklendirmesinde kullanılabilir hale getirmektir.

Çekirdek yaklaşım:

- iki aşamalı sistem
- confidence-aware tahmin
- düşük güvenli örneklerde `unknown` ve `manual review`
- resmi, açık, tahmin edilmiş ve bilinmeyen veri ayrımının kullanıcıya görünür olması
- uzman kararının yerine geçmeyen, uzmanı önceleyen karar desteği

## POC Kararları

İlk POC için sabitlenen kararlar:

| Başlık | Karar |
|---|---|
| İlk şehir | İstanbul |
| Yaklaşık kapsam | 100 bina |
| Görsel veri | Açık street-level imagery veya kurumsal izinli görüntüler |
| Görüntüleme | Çoklu açı |
| Görsel-bina eşleme | Sistem tarafından çözülecek |
| Etiket tipi | Post-event observed outcome |
| Afet veri odağı | 6 Şubat depremi, uygun olursa 1999 ve Van depremi verileri |
| Model davranışı | Her bina için tahmin zorunlu değil |
| Düşük güvenli çıktı | `unknown` + `manual review` |
| Karar seviyesi | Skor ve önceliklendirme; nihai karar uzmanlarda |
| README tonu | Teknik araştırma + ürün stratejisi + jüri savunması hibriti |

## Dokümanlar

Bu repo artık POC kararlarını ayrı dokümanlarda takip eder:

- [Facade Intelligence POC Planı](docs/README_facade_intelligence_poc.md)
- [Veri, Etiket ve Lisans Stratejisi](docs/README_data_label_strategy.md)
- [Ürün Kapsamı ve Digital Twin Karar Çerçevesi](docs/README_product_scope_and_questions.md)

## Mevcut MVP

Mevcut uygulama hâlâ çalışır durumdadır ve şu akışı gösterir:

1. Lokasyon ve yapı parametreleri alınır
2. Deprem tehlikesi ve yapısal kırılganlık birlikte değerlendirilir
3. Risk, uygunluk ve inceleme önceliği hesaplanır
4. Türkçe doğal dil açıklama ile karar gerekçesi sunulur
5. Alternatif senaryolar kıyaslanır
6. Sonuç kurumsal karar arayüzünde gösterilir

Teknik bileşenler:

- `Streamlit` çok sayfalı ürün arayüzü
- `Folium` harita katmanı
- `Plotly` skor ve karşılaştırma görselleştirmeleri
- heuristic scoring engine
- scenario engine
- explainability layer
- ML-ready prediction layer

## Kurulum

```bash
git clone https://github.com/akyilidizbaran/RiskTwin.git
cd RiskTwin
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py
```

Canlı lokal adres:

```text
http://localhost:8505
```

## Takım

**Takım Adı:** Aerolith Systems

- **Baran Akyıldız** - Teknik Lider, AI/ML ve modelleme
- **Elif Sena Önsöz** - Geospatial ve veri mühendisliği
- **Elif Güngen** - AI uygulama, ürün deneyimi ve sunum
- **Burak Kılıç** - Mekanik sistemler ve teknik doğrulama

## Kritik Sınır

RiskTwin bir mühendislik kararının yerine geçmez. Ürün, eksik envanteri zenginleştiren, önceliklendirme yapan, belirsizliği görünür kılan ve uzman kararını hızlandıran bir karar destek katmanı olarak konumlanır.

## Lisans

**All rights reserved**

Bu repository ve içindeki tüm proje çıktıları Aerolith Systems ve ilgili ekip üyelerinin kontrolündedir. Açık kaynak lisansı tanımlanmamıştır.
