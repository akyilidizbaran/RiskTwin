"""
RiskTwin — Ağırlık Duyarlılık Analizi (tornado).

Risk skorundaki her parametrenin etkisini ölçer: her ağırlığı ±delta (oransal)
oynatıp kalan ağırlıkları yeniden normalize ederek skor değişimini hesaplar.
Başkan/uzman savunması: "hangi parametre skoru ne kadar etkiliyor?" sorusuna
sayısal, şeffaf cevap; en yüksek etkili parametreler en güçlü gerekçeyi gerektirir.
"""
from typing import Dict, List

from src.config import SCORE_WEIGHTS
from src.scoring_engine import calculate_risk_score


def _weighted(sub_scores: Dict[str, float], weights: Dict[str, float]) -> float:
    total = sum(weights[k] for k in sub_scores if k in weights)
    if total == 0:
        return 0.0
    score = sum(sub_scores[k] * weights[k] for k in sub_scores if k in weights) / total
    return round(max(0, min(100, score)), 1)


def weight_sensitivity(sub_scores: Dict[str, float], delta: float = 0.10) -> List[Dict]:
    """
    Her ağırlığı ±delta (oransal) değiştirip skor etkisini döndür.

    Returns: parametre başına {factor, base, low, high, swing} listesi,
    swing (|high-low|) azalan sırada — tornado grafiği için hazır.
    """
    base = calculate_risk_score(sub_scores)
    rows: List[Dict] = []
    for factor in SCORE_WEIGHTS:
        if factor not in sub_scores:
            continue  # mevcut olmayan faktör skoru etkilemez
        bounds = {}
        for sign, name in ((-1, "low"), (1, "high")):
            w = dict(SCORE_WEIGHTS)
            w[factor] = max(0.0, w[factor] * (1 + sign * delta))
            bounds[name] = _weighted(sub_scores, w)
        swing = round(abs(bounds["high"] - bounds["low"]), 1)
        rows.append({
            "factor": factor,
            "base": base,
            "low": bounds["low"],
            "high": bounds["high"],
            "swing": swing,
        })
    rows.sort(key=lambda r: r["swing"], reverse=True)
    return rows
