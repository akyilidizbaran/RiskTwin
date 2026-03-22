"""
RiskTwin Açıklanabilirlik Katmanı
Kural tabanlı Türkçe doğal dil açıklamalar üretir.
"""
from typing import Dict, List

from src.config import (
    SCORE_WEIGHTS,
    SYSTEM_LABELS,
    SOIL_LABELS,
)


def _get_top_factors(sub_scores: Dict[str, float], top_n: int = 3) -> List[str]:
    """En yüksek skora sahip (en riskli) faktörleri döndür."""
    sorted_factors = sorted(sub_scores.items(), key=lambda x: x[1], reverse=True)
    return [f[0] for f in sorted_factors[:top_n]]


def _factor_label(factor: str) -> str:
    """Faktör anahtarını Türkçe etikete çevir."""
    labels = {
        "hazard": "deprem tehlike seviyesi",
        "soil": "zemin sınıfı",
        "age": "bina yaşı",
        "floors": "kat sayısı",
        "system": "taşıyıcı sistem türü",
    }
    return labels.get(factor, factor)


def _score_description(factor: str, score: float) -> str:
    """Faktör skoru için Türkçe açıklama üret."""
    if score >= 70:
        severity = "yüksek risk katkısı"
    elif score >= 40:
        severity = "orta düzey risk katkısı"
    else:
        severity = "düşük risk katkısı"

    descriptions = {
        "hazard": {
            "high": "Bina, yüksek deprem tehlikesi olan bir bölgede yer almaktadır. AFAD verilerine göre bölgenin tehlike skoru yüksektir.",
            "medium": "Bina, orta seviyede deprem tehlikesi olan bir bölgededir.",
            "low": "Bina, görece düşük deprem tehlikesi olan bir bölgededir.",
        },
        "soil": {
            "high": "Zemin sınıfı zayıf kategoridedir. Bu zemin tipi deprem dalgalarını güçlendirebilir ve yapısal hasarı artırabilir.",
            "medium": "Zemin sınıfı orta kategoridedir. Zemin etkisi mevcut ancak kritik düzeyde değildir.",
            "low": "Zemin sınıfı güçlü kategoridedir. Zemin koşulları yapı güvenliğine olumlu katkı sağlar.",
        },
        "age": {
            "high": "Bina eski yapım yılına sahiptir. Bu dönemde inşa edilen yapılar güncel deprem yönetmeliklerine uygun olmayabilir.",
            "medium": "Bina orta yaştadır. Kısmen güncel standartlara uygun olabilir ancak doğrulama gerekir.",
            "low": "Bina görece yenidir. Güncel deprem yönetmeliklerine uygun olma olasılığı yüksektir.",
        },
        "floors": {
            "high": "Yüksek katlı yapıda deprem kuvvetleri daha büyük olabilir. Kat sayısı arttıkça yapısal talep de artmaktadır.",
            "medium": "Orta yükseklikteki yapı. Kat sayısı makul seviyededir.",
            "low": "Düşük katlı yapı. Kat sayısının deprem riskine etkisi sınırlıdır.",
        },
        "system": {
            "high": "Taşıyıcı sistem türü deprem performansı açısından dezavantajlıdır. Modern standartlara uygun güçlendirme önerilir.",
            "medium": "Taşıyıcı sistem orta düzeyde deprem performansı sunmaktadır.",
            "low": "Taşıyıcı sistem modern deprem standartlarına uygun performans sağlamaktadır.",
        },
    }

    if score >= 70:
        level = "high"
    elif score >= 40:
        level = "medium"
    else:
        level = "low"

    return descriptions.get(factor, {}).get(level, f"{_factor_label(factor)}: {severity}")


def generate_risk_explanation(evaluation_result: Dict) -> str:
    """
    Değerlendirme sonucu için Türkçe açıklama metni üret.
    """
    sub_scores = evaluation_result["sub_scores"]
    risk_score = evaluation_result["risk_score"]
    band = evaluation_result["risk_band"]
    priority = evaluation_result["inspection_priority"]

    lines = []

    # Genel özet
    lines.append(
        f"**Genel Değerlendirme:** Bu yapının deprem risk skoru **{risk_score}/100** "
        f"olarak hesaplanmıştır ({band['label']} risk bandı)."
    )
    lines.append("")

    # En etkili faktörler
    top_factors = _get_top_factors(sub_scores, top_n=3)
    factor_names = [_factor_label(f) for f in top_factors]
    lines.append(
        f"**Risk Faktörleri:** Riski en fazla artıran faktörler: "
        f"**{', '.join(factor_names)}**."
    )
    lines.append("")

    # Her faktör için detay
    lines.append("**Detaylı Analiz:**")
    for factor in top_factors:
        desc = _score_description(factor, sub_scores[factor])
        weight_pct = int(SCORE_WEIGHTS.get(factor, 0) * 100)
        lines.append(
            f"- **{_factor_label(factor).capitalize()}** "
            f"(ağırlık: %{weight_pct}, skor: {sub_scores[factor]:.0f}/100): "
            f"{desc}"
        )
    lines.append("")

    # Öncelik ve öneri
    lines.append(
        f"**İnceleme Önceliği:** {priority} — "
        f"{evaluation_result['inspection_recommendation']}"
    )

    return "\n".join(lines)


def generate_scenario_explanation(scenario_result: Dict) -> str:
    """Senaryo karşılaştırması için Türkçe açıklama üret."""
    lines = []
    name = scenario_result["scenario_name"]
    delta = scenario_result["delta_risk"]
    base = scenario_result["base_risk_score"]
    new = scenario_result["new_risk_score"]

    if delta < 0:
        direction = "düşürmektedir"
        impact = f"**{abs(delta):.1f} puan** iyileşme"
    elif delta > 0:
        direction = "artırmaktadır"
        impact = f"**{delta:.1f} puan** kötüleşme"
    else:
        direction = "değiştirmemektedir"
        impact = "değişiklik yok"

    lines.append(
        f"**{name}** senaryosu risk skorunu {base:.1f}'den {new:.1f}'e {direction} ({impact})."
    )

    if scenario_result["base_band"] != scenario_result["new_band"]:
        lines.append(
            f"Risk bandı **{scenario_result['base_band']}**'den "
            f"**{scenario_result['new_band']}**'e geçmektedir."
        )

    lines.append(f"\n{scenario_result['recommendation']}")

    return "\n".join(lines)
