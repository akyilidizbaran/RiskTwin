"""
RiskTwin Skorlama Motoru
Heuristic tabanlı risk skoru, proje uygunluk skoru ve inceleme önceliği hesaplama.
"""
from typing import Dict, Tuple

from src.config import (
    SCORE_WEIGHTS,
    RISK_BANDS,
    HAZARD_SCORE_MAP,
    SOIL_SCORE_MAP,
    AGE_THRESHOLDS,
    FLOOR_THRESHOLDS,
    SYSTEM_SCORE_MAP,
    CRITICAL_ATTRIBUTES,
)


def _score_hazard(hazard_level: str = None, hazard_score: float = None) -> float:
    """Tehlike seviyesini 0-100 skora çevir."""
    if hazard_score is not None:
        return max(0, min(100, hazard_score))
    if hazard_level:
        return HAZARD_SCORE_MAP.get(hazard_level.lower(), 50)
    return 50  # varsayılan


def _score_soil(soil_class: str) -> float:
    """Zemin sınıfını 0-100 skora çevir."""
    return SOIL_SCORE_MAP.get(soil_class.upper(), 50)


def _score_age(building_age: int) -> float:
    """Bina yaşını 0-100 skora çevir."""
    for t in AGE_THRESHOLDS:
        if building_age <= t["max_age"]:
            return t["score"]
    return 80


def _score_floors(floor_count: int) -> float:
    """Kat sayısını 0-100 skora çevir."""
    for t in FLOOR_THRESHOLDS:
        if floor_count <= t["max_floors"]:
            return t["score"]
    return 80


def _score_system(structural_system: str) -> float:
    """Taşıyıcı sistemi 0-100 skora çevir."""
    return SYSTEM_SCORE_MAP.get(structural_system.lower(), 60)


def get_sub_scores(
    hazard_level: str = None,
    hazard_score: float = None,
    soil_class: str = "ZC",
    building_age: int = 20,
    floor_count: int = 5,
    structural_system: str = "betonarme_cerceve",
) -> Dict[str, float]:
    """
    Tüm alt skorları hesapla ve sözlük olarak döndür.
    Konum-türevli faktörler (hazard, soil) her zaman üretilir. Yapı-düzeyi
    parametreler (age/floors/system) None ise EKSİK kabul edilir ve sözlüğe
    eklenmez; böylece risk skoru yalnız mevcut faktörler üzerinden hesaplanır
    (tasarım ilkesi 10.3 — eksik veriyi 0/güvenli gibi gösterme).
    """
    sub_scores: Dict[str, float] = {
        "hazard": _score_hazard(hazard_level, hazard_score),
        "soil": _score_soil(soil_class),
    }
    if building_age is not None:
        sub_scores["age"] = _score_age(building_age)
    if floor_count is not None:
        sub_scores["floors"] = _score_floors(floor_count)
    if structural_system is not None:
        sub_scores["system"] = _score_system(structural_system)
    return sub_scores


def calculate_risk_score(sub_scores: Dict[str, float]) -> float:
    """
    Ağırlıklı risk skoru hesapla (0-100).
    Yalnız mevcut faktörler üzerinden ağırlıklar yeniden normalize edilir; böylece
    eksik bir faktör skoru yapay olarak düşürmez. Tüm faktörler mevcutsa (toplam
    ağırlık = 1.0) sonuç klasik ağırlıklı ortalamayla aynıdır.
    """
    total_w = sum(SCORE_WEIGHTS[k] for k in sub_scores if k in SCORE_WEIGHTS)
    if total_w == 0:
        return 0.0
    score = sum(sub_scores[k] * SCORE_WEIGHTS[k] for k in sub_scores if k in SCORE_WEIGHTS) / total_w
    return round(max(0, min(100, score)), 1)


def get_risk_band(score: float) -> Dict:
    """Risk bandını döndür."""
    for band in RISK_BANDS:
        if band["min"] <= score <= band["max"]:
            return band
    return RISK_BANDS[-1]


def calculate_project_fit_score(
    risk_score: float,
    is_existing_building: bool = True,
    retrofit_status: str = "yok",
) -> float:
    """
    Proje uygunluk skoru hesapla (0-100).
    Düşük risk skoru → yüksek proje uygunluğu.
    Güçlendirme yapılmışsa uygunluk artar.
    """
    base_fit = 100 - risk_score

    # Güçlendirme bonusu
    retrofit_bonus = {"yok": 0, "kismen": 10, "tam": 20}
    bonus = retrofit_bonus.get(retrofit_status, 0)

    # Mevcut bina ise, güçlendirme durumuna göre bonus
    if is_existing_building:
        base_fit += bonus
    else:
        # Yeni proje: risk düşükse uygunluk daha yüksek
        base_fit += 5

    return round(max(0, min(100, base_fit)), 1)


def get_inspection_priority(
    risk_score: float,
    is_existing_building: bool = True,
) -> Tuple[str, str]:
    """
    İnceleme önceliği döndür.
    Returns: (priority_level, recommendation_text)
    """
    band = get_risk_band(risk_score)

    if band["label"] == "Yüksek":
        if is_existing_building:
            return (
                "Yüksek",
                "Detaylı mühendislik incelemesi öncelikli. "
                "Yapının taşıyıcı sistem performansı ve deprem güvenliği acil değerlendirilmelidir.",
            )
        else:
            return (
                "Yüksek",
                "Proje parametreleri revize edilmeli. "
                "Mevcut tasarım yüksek riskli bölge koşullarına uygun olmayabilir.",
            )
    elif band["label"] == "Orta":
        return (
            "Orta",
            "Senaryo analizi ve saha doğrulaması önerilir. "
            "Alternatif tasarım senaryoları ile risk azaltma potansiyeli incelenmelidir.",
        )
    else:
        return (
            "Düşük",
            "Ön değerlendirme olumlu. "
            "Detaylı doğrulama yine gereklidir; bu sonuç nihai mühendislik kararı yerine geçmez.",
        )


def evaluate_building(
    hazard_level: str = None,
    hazard_score: float = None,
    soil_class: str = "ZC",
    building_age: int = 20,
    floor_count: int = 5,
    structural_system: str = "betonarme_cerceve",
    is_existing_building: bool = True,
    retrofit_status: str = "yok",
) -> Dict:
    """
    Tek bir bina için tam değerlendirme yap.
    Returns: Tüm skorlar, band, uygunluk, öncelik ve açıklama içeren sözlük.
    """
    sub_scores = get_sub_scores(
        hazard_level=hazard_level,
        hazard_score=hazard_score,
        soil_class=soil_class,
        building_age=building_age,
        floor_count=floor_count,
        structural_system=structural_system,
    )

    risk_score = calculate_risk_score(sub_scores)
    risk_band = get_risk_band(risk_score)
    fit_score = calculate_project_fit_score(risk_score, is_existing_building, retrofit_status)
    priority_level, priority_text = get_inspection_priority(risk_score, is_existing_building)

    # ── Veri tamlığı / eksik-veri görünürlüğü (tasarım ilkesi 10.3) ──
    missing_structural = [k for k in CRITICAL_ATTRIBUTES if k not in sub_scores]
    present_structural = [k for k in CRITICAL_ATTRIBUTES if k in sub_scores]
    completeness = round(len(present_structural) / len(CRITICAL_ATTRIBUTES), 2)
    needs_field_check = bool(missing_structural)
    if not missing_structural:
        data_status = "tam"
    elif present_structural:
        data_status = "kismi"
    else:
        data_status = "site_only"  # yalnız konum (hazard+soil) bilgisi var
    triage_note = (
        "Kritik yapı verisi eksik — risk skoru konuma dayalı geçicidir; saha kontrolü gerekli."
        if needs_field_check else
        "Envanter verisi tam; risk skoru tüm faktörleri içerir."
    )
    # Güven, şimdilik tamlıktan türetilir; sonraki adım: öznitelik-başı kalibre güven (conformal).
    confidence = completeness

    return {
        "sub_scores": sub_scores,
        "risk_score": risk_score,
        "risk_band": risk_band,
        "project_fit_score": fit_score,
        "inspection_priority": priority_level,
        "inspection_recommendation": priority_text,
        "is_existing_building": is_existing_building,
        "retrofit_status": retrofit_status,
        # ── eksik-veri / provenans katmanı ──
        "completeness": completeness,
        "confidence": confidence,
        "data_status": data_status,
        "missing_structural": missing_structural,
        "needs_field_check": needs_field_check,
        "triage_note": triage_note,
    }
