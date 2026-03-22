"""
RiskTwin Senaryo Motoru
Aynı lokasyon için alternatif senaryolar üretir ve karşılaştırır.
"""
from typing import Dict, List
from src.scoring_engine import evaluate_building


def create_scenario(
    base_params: Dict,
    scenario_name: str,
    overrides: Dict,
) -> Dict:
    """
    Bir senaryo oluştur: base parametrelerin üzerine override'lar uygula.
    """
    scenario_params = {**base_params, **overrides}
    base_result = evaluate_building(**base_params)
    new_result = evaluate_building(**scenario_params)

    return {
        "scenario_name": scenario_name,
        "base_risk_score": base_result["risk_score"],
        "new_risk_score": new_result["risk_score"],
        "delta_risk": round(new_result["risk_score"] - base_result["risk_score"], 1),
        "base_project_fit_score": base_result["project_fit_score"],
        "new_project_fit_score": new_result["project_fit_score"],
        "delta_fit": round(
            new_result["project_fit_score"] - base_result["project_fit_score"], 1
        ),
        "base_band": base_result["risk_band"]["label"],
        "new_band": new_result["risk_band"]["label"],
        "recommendation": _generate_scenario_recommendation(
            base_result, new_result, scenario_name
        ),
        "overrides": overrides,
        "new_result": new_result,
    }


def _generate_scenario_recommendation(
    base_result: Dict, new_result: Dict, scenario_name: str
) -> str:
    """Senaryo sonucuna göre öneri üret."""
    delta = new_result["risk_score"] - base_result["risk_score"]
    base_band = base_result["risk_band"]["label"]
    new_band = new_result["risk_band"]["label"]

    if delta < -15:
        return (
            f"'{scenario_name}' senaryosu risk skorunu önemli ölçüde düşürmektedir "
            f"({base_band} → {new_band}). Bu senaryo güçlü bir iyileştirme sağlar."
        )
    elif delta < -5:
        return (
            f"'{scenario_name}' senaryosu risk skorunu kısmen düşürmektedir "
            f"({base_band} → {new_band}). Ek önlemlerle birlikte değerlendirilmelidir."
        )
    elif delta > 5:
        return (
            f"'{scenario_name}' senaryosu riski artırmaktadır "
            f"({base_band} → {new_band}). Bu parametreler dikkatle gözden geçirilmelidir."
        )
    else:
        return (
            f"'{scenario_name}' senaryosu risk skorunda belirgin bir değişiklik yaratmamaktadır "
            f"({base_band} → {new_band})."
        )


def get_predefined_scenarios(base_params: Dict) -> List[Dict]:
    """
    Önceden tanımlı senaryoları çalıştır:
    1. Güçlendirme
    2. Kat azaltma
    3. Zemin iyileştirme
    4. Mevcut bina → güçlendirilmiş bina kıyası
    """
    scenarios = []

    # Senaryo 1: Güçlendirme (taşıyıcı sistemi betonarme_perde yap)
    if base_params.get("structural_system") != "betonarme_perde":
        scenarios.append(
            create_scenario(
                base_params,
                "Güçlendirme (Betonarme Perde)",
                {
                    "structural_system": "betonarme_perde",
                    "retrofit_status": "tam",
                },
            )
        )

    # Senaryo 2: Kat sayısı azaltma
    current_floors = base_params.get("floor_count", 5)
    if current_floors > 3:
        reduced = max(3, current_floors - 3)
        scenarios.append(
            create_scenario(
                base_params,
                f"Kat Azaltma ({current_floors} → {reduced})",
                {"floor_count": reduced},
            )
        )

    # Senaryo 3: Zemin iyileştirme (bir sınıf yukarı)
    soil_upgrade = {
        "ZF": "ZE",
        "ZE": "ZD",
        "ZD": "ZC",
        "ZC": "ZB",
        "ZB": "ZA",
    }
    current_soil = base_params.get("soil_class", "ZC")
    if current_soil in soil_upgrade:
        new_soil = soil_upgrade[current_soil]
        scenarios.append(
            create_scenario(
                base_params,
                f"Zemin İyileştirme ({current_soil} → {new_soil})",
                {"soil_class": new_soil},
            )
        )

    # Senaryo 4: Tam güçlendirme (sistem + retrofit)
    if base_params.get("is_existing_building", True) and base_params.get("retrofit_status") != "tam":
        scenarios.append(
            create_scenario(
                base_params,
                "Tam Güçlendirme Paketi",
                {
                    "structural_system": "betonarme_perde",
                    "retrofit_status": "tam",
                },
            )
        )

    return scenarios


def create_custom_scenario(
    base_params: Dict,
    scenario_name: str,
    **overrides,
) -> Dict:
    """Kullanıcı tanımlı özel senaryo oluştur."""
    return create_scenario(base_params, scenario_name, overrides)
