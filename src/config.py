"""
RiskTwin Konfigürasyon Dosyası
Dosya yolları, skor ağırlıkları, sınıflandırma eşikleri ve senaryo parametre limitleri.
"""
import os

# ── Proje Kök Dizini ──
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Dosya Yolları ──
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
INTERIM_DIR = os.path.join(DATA_DIR, "interim")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
EXTERNAL_DIR = os.path.join(DATA_DIR, "external")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")

HAZARD_CSV = os.path.join(EXTERNAL_DIR, "hazard_samples.csv")
BUILDING_CSV = os.path.join(PROCESSED_DIR, "demo_building_inputs.csv")
POPULATION_CSV = os.path.join(EXTERNAL_DIR, "population_context.csv")
BUILDINGS_GEOJSON = os.path.join(PROCESSED_DIR, "buildings.geojson")
ROADS_GEOJSON = os.path.join(PROCESSED_DIR, "roads.geojson")
POIS_GEOJSON = os.path.join(PROCESSED_DIR, "pois.geojson")
NEIGHBORHOODS_GEOJSON = os.path.join(PROCESSED_DIR, "neighborhood_boundary.geojson")

# ── Varsayılan Şehir ──
DEFAULT_CITY = "İstanbul"
DEFAULT_MAP_CENTER = [41.0082, 28.9784]
DEFAULT_MAP_ZOOM = 11

# ── Skor Ağırlıkları ──
SCORE_WEIGHTS = {
    "hazard": 0.30,
    "soil": 0.25,
    "age": 0.15,
    "floors": 0.15,
    "system": 0.15,
}

# ── Kritik (yapı-düzeyi) öznitelikler ──
# Bunlar bina-düzeyi veri/saha gerektirir. Eksik olduklarında skor, konum-türevli
# faktörler (hazard + soil) üzerinden yeniden normalize edilip "site-only" geçici
# skor üretir ve kayıt "saha kontrolü gerekli" işaretlenir (tasarım ilkesi 10.3 + 10.5).
CRITICAL_ATTRIBUTES = ["age", "floors", "system"]
SITE_FACTORS = ["hazard", "soil"]

# ── Katsayı Gerekçe Tablosu ──
# Başkan/uzman savunması: ağırlıklar keyfi değil; literatürdeki hızlı tarama
# yöntemlerine dayandırılmış uzman ön-değerleridir. Sonraki adım: AHP/uzman
# kalibrasyonu + 2023 Kahramanmaraş hasar verisiyle doğrulama.
COEFFICIENT_JUSTIFICATION = [
    {
        "factor": "hazard", "weight": 0.30,
        "basis": "Sismik talep en temel belirleyici; taban skoru tasarım yer hareketi (MCER/PGA) üzerinden belirlenir.",
        "source": "FEMA P-154 / P-155; TBDY-2018",
    },
    {
        "factor": "soil", "weight": 0.25,
        "basis": "Zemin amplifikasyonu talebi büyüten çarpan; yumuşak zeminler (ZD-ZF) tasarım spektrumunu artırır.",
        "source": "FEMA P-154 (S_D/S_E); TBDY-2018 zemin sınıfı",
    },
    {
        "factor": "age", "weight": 0.15,
        "basis": "Yapım yılı yönetmelik neslini (kod düzeyi) belirler; pre-code yapı yüksek kırılganlık.",
        "source": "FEMA P-154 (kod düzeyi); Sucuoğlu-Yakut 2008",
    },
    {
        "factor": "floors", "weight": 0.15,
        "basis": "Kat sayısı/yükseklik kütle ve periyodu artırır; rapid screening'de temel kırılganlık parametresi.",
        "source": "FEMA P-154; Sucuoğlu-Yakut 2008; P25",
    },
    {
        "factor": "system", "weight": 0.15,
        "basis": "Taşıyıcı sistem türü yanal yük kapasitesini belirler (perde > çerçeve > yığma).",
        "source": "FEMA P-154 (bina tipi); RISK-UE LM1",
    },
]

# ── Risk Bandları ──
RISK_BANDS = [
    {"min": 0, "max": 39, "label": "Düşük", "color": "#27ae60", "emoji": "🟢"},
    {"min": 40, "max": 64, "label": "Orta", "color": "#f39c12", "emoji": "🟡"},
    {"min": 65, "max": 100, "label": "Yüksek", "color": "#e74c3c", "emoji": "🔴"},
]

# ── Heuristic Mapping: Tehlike Seviyesi → Skor (0-100) ──
HAZARD_SCORE_MAP = {
    "low": 20,
    "medium": 50,
    "high": 80,
}

# ── Heuristic Mapping: Zemin Sınıfı → Skor ──
SOIL_SCORE_MAP = {
    "ZA": 10,
    "ZB": 20,
    "ZC": 50,
    "ZD": 70,
    "ZE": 85,
    "ZF": 95,
}

# ── Bina Yaşı → Skor (yıl cinsinden) ──
AGE_THRESHOLDS = [
    {"max_age": 10, "score": 20},
    {"max_age": 25, "score": 50},
    {"max_age": 999, "score": 80},
]

# ── Kat Sayısı → Skor ──
FLOOR_THRESHOLDS = [
    {"max_floors": 3, "score": 20},
    {"max_floors": 7, "score": 50},
    {"max_floors": 999, "score": 80},
]

# ── Taşıyıcı Sistem → Skor ──
SYSTEM_SCORE_MAP = {
    "betonarme_perde": 25,
    "celik": 30,
    "betonarme_cerceve": 55,
    "prefabrik": 65,
    "yigma": 85,
    "bilinmiyor": 60,
}

# ── Taşıyıcı Sistem Türkçe Etiketler ──
SYSTEM_LABELS = {
    "betonarme_perde": "Betonarme Perde",
    "celik": "Çelik",
    "betonarme_cerceve": "Betonarme Çerçeve",
    "prefabrik": "Prefabrik",
    "yigma": "Yığma",
    "bilinmiyor": "Bilinmiyor",
}

# ── Zemin Sınıfı Türkçe Etiketler ──
SOIL_LABELS = {
    "ZA": "ZA - Sağlam Kaya",
    "ZB": "ZB - Kaya",
    "ZC": "ZC - Sıkı Zemin",
    "ZD": "ZD - Yumuşak Zemin",
    "ZE": "ZE - Zayıf Zemin",
    "ZF": "ZF - Özel Araştırma Gerektiren",
}

# ── Kullanım Tipi Seçenekleri ──
USAGE_TYPES = ["konut", "ticari", "ofis", "karma", "sanayi", "egitim", "saglik"]

# ── Güçlendirme Durumu Seçenekleri ──
RETROFIT_OPTIONS = ["yok", "kismen", "tam"]

# ── Senaryo Parametre Limitleri ──
SCENARIO_LIMITS = {
    "floor_count_min": 1,
    "floor_count_max": 40,
    "building_age_min": 0,
    "building_age_max": 100,
}
