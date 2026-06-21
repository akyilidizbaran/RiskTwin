# RiskTwin — Karar Günlüğü ve Gerekçeler

> Bu dosya, projenin yön değişiminden 6 günlük pilot kapsamına kadar verdiğimiz
> **tüm kararları**, her birinin **araştırma gerekçesini** ve **kaynağını** tek
> yerde toplar. Amaç: ekip ve paydaşlar (bakan/yatırımcı/başkan) karşısında her
> kararın "neden böyle?" sorusuna tutarlı cevap verebilmek.
>
> Tarih: 18 Haziran 2026 · Sürüm: 1.0 · Proje: RiskTwin / Aerolith Systems

---

## 0. Tek cümlede sistem

RiskTwin artık "risk tahmin eden bir yapay zekâ" değil; **görüntü/veriden ulusal
yapı envanterini (exposure) otomatik çıkaran, belirsizliği ve kaynağı izlenen,
insan-döngülü bir altyapı** — ve bu envanterin üstünde çalışan **açıklanabilir
ön-inceleme önceliklendirme dijital ikizi**.

İki adım:
- **Adım 1 (yeni):** Görüntü işleme + açık veri ile **yapı envanteri tahmini**.
- **Adım 2 (ilk fikrimiz, korunuyor):** Bu envanterden **RiskTwin dijital ikiz** —
  açıklanabilir önceliklendirme, hazard (AFAD/AYDES) entegrasyonu, senaryo analizi.

---

## 1. Stratejik pivot ve konumlandırma

| Konu | Karar | Gerekçe |
|---|---|---|
| Ana iddia | "Risk önceliklendirme"den → **"ulusal yapı envanteri altyapısı"**na | Kentsel dönüşüm müdürü: risk modeli zaten yapılmış; çözülmemiş gerçek problem = eksik/tamamlanamayan yapı envanteri |
| Eski fikrin yeri | Silinmedi; **Adım 2 (dijital ikiz)** olarak korundu | İlk girişimi yok saymamak; "temelini tamamladık" çerçevesi |
| İzleyici | Bakanlar, büyük yatırımcılar, büyük şirketler | Sunum bağlamı değişti |
| Emlak Konut | **Çapa ortak** (merkez değil) | Şablon Emlak Konut pilotunu zorunlu kılıyor; ulusal vizyon korunarak |
| Marka | RiskTwin · Aerolith Systems korunuyor | Süreklilik |

**Tek cümlelik tez:** "Milyonlarca binayı tek tek mühendisle taramak yerine; uydu,
hava, sokak ve drone verisini yapay zekâyla birleştirip riskli azınlığı
önceliklendiren bir ön-tarama (triyaj) altyapısı." **AI nihai karar vermez, eler.**

---

## 2. Problem ve ölçek (sunumun rakamsal omurgası)

- ~**19 milyon konut**; ~**14 milyonu** afet riski açısından incelenmeli.
- ~**6,5–7,5 milyon birim** risk altında; ~**2 milyon bina** acil.
- İstanbul: ~**1,5 milyon riskli**, ~600 bini acil.
- **2023 (6 Şubat):** ~**2,6 milyon bina** için hasar tespiti, ~**10.000 teknik
  personel** → "elle taranamaz" kanıtı.

---

## 3. Dünya kanıtı ve teknik dersler (kararları besleyen)

| Bulgu | Kaynak | Karara etkisi |
|---|---|---|
| BRAILS: kat sayısı %94,7; çatı %90,3; **yaş %26** | NHERI SimCenter | Yaşı görselden sınıflandırma; **ortofoto "ilk görünüm" tarihleme** kullan |
| Bina yaşı hava görüntüsünden %88–93 (3 sınıf) | Hollanda/Çin çalışmaları | Çok-yıllı ortofoto + Temporal Cluster Matching |
| Soft-story tespiti için ~17–42k etiketli görsel | Yu vd. 2020 | Öznitelik başına ciddi etiket gerekir → zayıf-denetim stratejisi |
| Gölge uzunluğuyla yükseklik ~%96 (2 m) | arXiv 2411.09411 | Yüksekliği uydudan çöz, sokak görüntüsüne bağımlı kalma |
| Hazır model ≠ doğrudan transfer (domain gap) | BRAILS yaş %26 | **Sıfırdan değil, transfer learning + Türk verisiyle ince ayar** |
| GEM Building Taxonomy (13 öznitelik) | GEM Foundation | Çıktı şeması standardı → vulnerability modeline bağlanır |

---

## 4. Tasarım ilkeleri (veri modeli) — kabul edildi

1. **Her öznitelik = {değer, kaynak, güven, durum}** (provenans). Güven kalibre olmalı (conformal — sonraki adım).
2. **Ana çıktı kesin risk skoru değil**; iki eksen: **ön inceleme önceliği × envanter güveni**. "Düşük öncelik ≠ güvenli."
3. **Eksik veri ayrı çıktıdır**: üç-durumlu öznitelik (biliniyor / çıkarılamadı / işlenmedi); kritik küme eksikse "saha kontrolü gerekli".
4. **Görüntü işleme = zenginleştirici**, karar verici değil (aday/şüphe/güven).
5. **Tehlike katmanları ikinci katman** (exposure ≠ risk); envantere gömülmez.
6. **Human-in-the-loop** → saha doğrulaması kaydı düzeltir + model etiketini besler (çark) → yaşayan sicil.

Kesişen gereklilikler: **kalibrasyon** (conformal), **kimlik omurgası (UAVT + MEGSIS footprint)**,
**zamansal geçerlilik (bayatlık)**, **metrikler pilottan önce tanımlanmalı** (precision@k, ECE, kapsama).
Standartlar: **GEM Taxonomy + ISO 19157**.

---

## 5. Veri kaynağı ve yasallık kararları

### KULLANMA (yasak / riskli)
| Kaynak | Neden |
|---|---|
| Google Maps / Street View karoları | Toplu indirme, türev veri, ML eğitimi TOS ile **yasak** |
| Esri World Imagery | Yalnız elle çizim; **ML eğitimi yasak** |
| Google Open Buildings | **Türkiye'yi kapsamıyor** |

### KULLAN (açık/serbest, 6 günde edinilebilir)
| Kaynak | İçerik | Lisans |
|---|---|---|
| **Microsoft GlobalMLBuildingFootprints** | TR ~5,8M bina footprint (birincil) | ODbL (ML serbest, atıf) |
| Overture / OSM (Geofabrik TR) | Yedek/doğrulama footprint | ODbL |
| Sentinel-2 (Copernicus) | Bağlam (10 m, bina detayı için kaba) | Ücretsiz/açık |
| AFAD Tehlike Haritası + TADAS | PGA/Ss/S1 koordinattan | Açık |
| MTA jeoloji + İBB mikrobölgeleme | Zemin sınıfı/amplifikasyon | Kamuya açık |
| Mapillary | Sokak görüntüsü (yalnız QA/doğrulama) | CC-BY-SA |

**MEGSIS / HGM ortofoto:** kamuya açık ama toplu API yok + lisans belirsiz →
6 günde yalnız **örneklem manuel kontrol**; toplu erişim kurumsal anlaşma ister.

---

## 6. İki entegrasyon modu

- **Mod A — 6 günlük MVP:** Mevcut/açık yapı stoğunu zenginleştirme (Microsoft
  footprints + AFAD/MTA zemin + İmar Barışı/MEGSIS örneklem).
- **Mod B — yol haritası (devlet ölçeği):** Her sokakta drone → yumuşak kat / kat /
  çatlak. **Gerçeklik kontrolü:** kolon kalınlığı dış görüntüden **çıkarılamaz**;
  çatlak **yakın-çekim drone** ister → MVP değil, yol haritası.

---

## 7. Risk skoru ve katsayı gerekçesi (başkanın sorusu)

**Karar:** Ağırlıklı-toplam skor; ağırlıklar **literatüre dayandırılmış uzman
ön-değerleri** + **katsayı-gerekçe tablosu** + **duyarlılık analizi**. Uzman/AHP
kalibrasyonu ve 2023 Kahramanmaraş doğrulaması = **sonraki adım**.

Mevcut ağırlıklar (`src/config.py::SCORE_WEIGHTS`) ve dayanağı:

| Faktör | Ağırlık | Temel | Kaynak |
|---|---|---|---|
| Tehlike (hazard) | 0.30 | Sismik talep en temel belirleyici (MCER/PGA) | FEMA P-154/P-155; TBDY-2018 |
| Zemin (soil) | 0.25 | Amplifikasyon talebi büyütür (ZD–ZF) | FEMA P-154 (S_D/S_E); TBDY-2018 |
| Yaş (age) | 0.15 | Yönetmelik nesli / kod düzeyi | FEMA P-154; Sucuoğlu-Yakut 2008 |
| Kat (floors) | 0.15 | Yükseklik kütle/periyodu artırır | FEMA P-154; P25 |
| Sistem (system) | 0.15 | Yanal yük kapasitesi (perde>çerçeve>yığma) | FEMA P-154; RISK-UE LM1 |

Literatürde katsayı türetme yolları: olasılıksal/fragility (FEMA P-154), deprem-sonrası
ampirik kalibrasyon (P25 — 323 bina; Sucuoğlu-Yakut — İstanbul), uzman/Delphi/AHP (RISK-UE).
Savunma stratejisi: gerekçe tablosu + duyarlılık (tornado) + (sonraki adım) Kahramanmaraş doğrulaması.

---

## 8. Eksik parametre → zemin bağlamı (kullanıcının isteği, uygulandı)

**Karar:** Skorun **%55'i (hazard 0.30 + soil 0.25) koordinattan** türetilebilir
(AFAD + MTA/mikrobölgeleme). Bir binanın yapı parametreleri envanterde yoksa
parametre uydurmak yerine, ağırlıklar mevcut faktörlere **yeniden normalize**
edilip **konuma dayalı geçici skor** üretilir ve kayıt **"kritik veri eksik —
saha gerekli"** işaretlenir (tasarım ilkesi 10.3 + 10.5). Kodda doğrulandı:
yüksek-tehlike/zayıf-zemin bina, yapı verisi yokken skor **düşmüyor** (yapay
güvenli görünmüyor), "saha gerekli" damgası alıyor.

---

## 9. 6 günlük pilot — kapsam kararları (onaylandı)

| Soru | Karar |
|---|---|
| 6 gün odağı | **Veri-entegrasyon MVP'si** (görüntü modeli eğitimi değil) |
| Katsayı temeli | **Literatür + gerekçe tablosu + duyarlılık**; uzman/AHP sonraki adım |
| Pilot bölge | **Mikrobölgelemesi olan İstanbul ilçesi** (öneri: Zeytinburnu/Bağcılar) |

Pilot çıktısı = **3 liste:** (1) ön inceleme önceliği yüksek binalar, (2) kritik
verisi eksik — saha gerekli binalar, (3) kaynak+güvenli envanter kaydı. Başarı,
mühendis saha doğrulamasıyla uyum (precision@k) üzerinden ölçülür.

---

## 10. Kod mimarisi, entegrasyon ve uygulama durumu

**Kanonik kod konumu:** parent `risktwin/` (src/, app/, tests/, docs/, notebooks/;
`.venv`). `RiskTwin-main/` eski kopyadır, kullanılmaz.

**Entegrasyon noktası:** Adım 1 envanteri, mevcut `data/processed/demo_building_inputs.csv`
şemasının üst kümesini üretir → mevcut `src/scoring_engine.py::evaluate_building()`
tüketir. Mimari değişiklik yok; provenans + eksik-veri katmanı eklendi.

**Uygulanan (çekirdek, 55/55 test yeşil):**
- `src/config.py`: `CRITICAL_ATTRIBUTES`, `COEFFICIENT_JUSTIFICATION`.
- `src/scoring_engine.py`: eksik-veri yeniden-normalizasyon + site-only fallback +
  `completeness/confidence/data_status/needs_field_check/triage_note` (tam-girdide skor değişmez).
- `src/inventory/record.py`: `AttributeRecord` / `BuildingRecord` (provenans).
- `src/sensitivity.py`: ağırlık tornado duyarlılık analizi.
- `tests/test_inventory.py`: 16 yeni test.

**Kalan:** #5 veri edinim (footprints/site/attrs, indirme), #6 web (Adım 1
envanter sayfası + provenans rozetleri + metodoloji tablo/grafik = deck SS'leri),
#7 uçtan uca doğrulama.

---

## 11. Sunum destesi planı (Anahtar Fikirler Zirvesi şablonu)

Şablon **kesin 10 sayfa** (yalnız "Çözüm Nasıl Çalışıyor?" +1 sayfa = azami 11).
Eşleştirme:

| Şablon bölümü | İçerik |
|---|---|
| 1 Etkinlik kapağı | sabit |
| 2 Takım & Proje | Aerolith · RiskTwin · slogan + logo |
| 3 Problem | Envanter yok → öncelik yok + rakamlar |
| 4 Çözüm | **2 adımlı sistem** + değer önerileri |
| 5 Çözüm Nasıl Çalışıyor (5a) | Adım 1 huni + **web SS #1** |
| 5b (+1 izinli) | Adım 2 dijital ikiz (XAI/AFAD-AYDES/senaryo) + **web SS #2** |
| 6 Benzersiz Değer | şehir ölçeği + provenans + İmar Barışı 13M |
| 7 Hedef Kitle + Metrikler | kullanıcılar + %50–60 / %30–40 / precision@k |
| 8 Emlak Konut Pilot | 1 ilçe · ~10k bina · 3 çıktı |
| 9 Takım | 4 üye |
| 10 Teşekkürler | slogan + talep |

Web sitesinin 2 sayfası 2 adıma birebir oturur (SS#1→5a, SS#2→5b).

---

## 12. Üretilen dosyalar / teslimatlar

- `docs/karar-gunlugu.md` — bu dosya.
- `Yapi_Envanteri_Pilotu_Teknik_Yol_Haritasi_v1_1.docx` — teknik yol haritası raporu.
- `~/.claude/plans/...greedy-giraffe.md` — onaylı 6 günlük uygulama planı.
- `Aerolith_Systems_Sunum_orijinal.pptx` — eski deste (referans); `Sablon_AnahtarFikirler.pptx` — resmi şablon.
- Kod: `src/inventory/`, `src/sensitivity.py`, `src/config.py`, `src/scoring_engine.py`, `tests/test_inventory.py`.

---

## 13. Açık kalemler ve sonraki adımlar

1. **#5 Veri edinim:** Microsoft footprints (ilçe bbox) + AFAD/MTA/İBB zemin → gerçek pilot envanteri.
2. **#6 Web:** Adım 1 envanter sayfası + provenans/eksik-veri rozetleri + metodoloji katsayı tablosu & duyarlılık grafiği → deck SS'leri.
3. **#7 Uçtan uca doğrulama** (app + pytest).
4. **Sonraki tur (MVP dışı):** uzman/AHP katsayı kalibrasyonu; 2023 Kahramanmaraş doğrulaması; conformal kalibre güven; UAVT+MEGSIS kimlik omurgası; veri edinim hukuku/kurumsal ortaklık (HGM/TKGM/İBB/İmar Barışı); İSMEP/Dünya Bankası eklemlenme.

---

## Temel kaynaklar

- NHERI SimCenter BRAILS · GEM Building Taxonomy v2.0 / Global Vulnerability Model
- FEMA P-154 / P-155 · Sucuoğlu & Yakut (2008) · P25 (Tezcan/Bal) · RISK-UE LM1 · TBDY-2018
- Temporal Cluster Matching (arXiv:2103.09787) · gölge-yükseklik (arXiv:2411.09411)
- Microsoft GlobalMLBuildingFootprints (ODbL) · Sentinel-2/Copernicus · AFAD TDTH/TADAS · MTA · Mapillary (CC-BY-SA)
- Google Maps Platform TOS (toplu indirme/ML yasağı) · ISO 19157 (veri kalitesi)
