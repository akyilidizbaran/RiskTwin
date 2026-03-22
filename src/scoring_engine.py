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
    """Tüm alt skorları hesapla ve sözlük olarak döndür."""
    return {
        "hazard": _score_hazard(hazard_level, hazard_score),
        "soil": _score_soil(soil_class),
        "age": _score_age(building_age),
        "floors": _score_floors(floor_count),
        "system": _score_system(structural_system),
    }


def calculate_risk_score(sub_scores: Dict[str, float]) -> float:
    """Ağırlıklı risk skoru hesapla (0-100)."""
    score = sum(
        sub_scores.get(k, 0) * w for k, w in SCORE_WEIGHTS.items()
    )
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

    return {
        "sub_scores": sub_scores,
        "risk_score": risk_score,
        "risk_band": risk_band,
        "project_fit_score": fit_score,
        "inspection_priority": priority_level,
        "inspection_recommendation": priority_text,
        "is_existing_building": is_existing_building,
        "retrofit_status": retrofit_status,
    }
