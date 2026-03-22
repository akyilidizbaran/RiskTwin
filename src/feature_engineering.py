"""
RiskTwin Feature Engineering
Risk modeline girecek feature setini üretir, categorical encode eder, training matrix hazırlar.
"""
import pandas as pd
import numpy as np
from typing import Tuple

from src.config import SYSTEM_SCORE_MAP, SOIL_SCORE_MAP


# ── Ordinal Encoding Maps ──
SOIL_ORDINAL = {"ZA": 0, "ZB": 1, "ZC": 2, "ZD": 3, "ZE": 4, "ZF": 5}

SYSTEM_ORDINAL = {
    "betonarme_perde": 0,
    "celik": 1,
    "betonarme_cerceve": 2,
    "prefabrik": 3,
    "yigma": 4,
    "bilinmiyor": 3,
}

RETROFIT_ORDINAL = {"tam": 0, "kismen": 1, "yok": 2}


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ham bina verisini ML-ready feature matrix'e dönüştür.
    Input: building_age, floor_count, structural_system, soil_class,
           is_existing_building, retrofit_status, hazard_score
    Output: Tüm sayısal feature'lar içeren DataFrame
    """
    features = pd.DataFrame()

    # Sayısal özellikler (doğrudan)
    features["building_age"] = pd.to_numeric(df["building_age"] if "building_age" in df.columns else pd.Series([25] * len(df)), errors="coerce").fillna(25)
    features["floor_count"] = pd.to_numeric(df["floor_count"] if "floor_count" in df.columns else pd.Series([5] * len(df)), errors="coerce").fillna(5)
    features["hazard_score"] = pd.to_numeric(df["hazard_score"] if "hazard_score" in df.columns else pd.Series([70] * len(df)), errors="coerce").fillna(70)

    # Normalize edilmiş sayısal özellikler
    features["age_normalized"] = features["building_age"].clip(0, 100) / 100
    features["floors_normalized"] = features["floor_count"].clip(1, 40) / 40
    features["hazard_normalized"] = features["hazard_score"].clip(0, 100) / 100

    # Ordinal encoding: zemin sınıfı
    if "soil_class" in df.columns:
        features["soil_ordinal"] = df["soil_class"].map(SOIL_ORDINAL).fillna(2)
    else:
        features["soil_ordinal"] = 2

    # Ordinal encoding: taşıyıcı sistem
    if "structural_system" in df.columns:
        features["system_ordinal"] = df["structural_system"].map(SYSTEM_ORDINAL).fillna(2)
    else:
        features["system_ordinal"] = 2

    # Ordinal encoding: güçlendirme durumu
    if "retrofit_status" in df.columns:
        features["retrofit_ordinal"] = df["retrofit_status"].map(RETROFIT_ORDINAL).fillna(2)
    else:
        features["retrofit_ordinal"] = 2

    # Binary: mevcut bina
    if "is_existing_building" in df.columns:
        features["is_existing"] = df["is_existing_building"].astype(int)
    else:
        features["is_existing"] = 1

    # Heuristic sub-scores (kullanılabilir feature olarak)
    if "soil_class" in df.columns:
        features["soil_risk_score"] = df["soil_class"].map(SOIL_SCORE_MAP).fillna(50)
    else:
        features["soil_risk_score"] = 50

    if "structural_system" in df.columns:
        features["system_risk_score"] = df["structural_system"].map(SYSTEM_SCORE_MAP).fillna(60)
    else:
        features["system_risk_score"] = 60

    # One-hot encoding: taşıyıcı sistem
    if "structural_system" in df.columns:
        system_dummies = pd.get_dummies(df["structural_system"], prefix="sys")
        features = pd.concat([features, system_dummies], axis=1)

    # One-hot encoding: zemin sınıfı
    if "soil_class" in df.columns:
        soil_dummies = pd.get_dummies(df["soil_class"], prefix="soil")
        features = pd.concat([features, soil_dummies], axis=1)

    return features


def prepare_training_data(
    df: pd.DataFrame,
    target_col: str = "risk_label",
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Training matrix ve target hazırla.
    Eğer target_col yoksa heuristic skordan oluştur.
    """
    features = encode_features(df)

    if target_col in df.columns:
        target = df[target_col]
    else:
        # Heuristic skordan label oluştur
        from src.scoring_engine import get_sub_scores, calculate_risk_score

        labels = []
        for _, row in df.iterrows():
            sub = get_sub_scores(
                hazard_score=row.get("hazard_score"),
                hazard_level=row.get("hazard_level", "high"),
                soil_class=row.get("soil_class", "ZC"),
                building_age=int(row.get("building_age", 25)),
                floor_count=int(row.get("floor_count", 5)),
                structural_system=row.get("structural_system", "betonarme_cerceve"),
            )
            score = calculate_risk_score(sub)
            # 3 sınıf: 0=düşük, 1=orta, 2=yüksek
            if score < 40:
                labels.append(0)
            elif score < 65:
                labels.append(1)
            else:
                labels.append(2)
        target = pd.Series(labels, name="risk_class")

    return features, target


def get_feature_names() -> list:
    """Temel feature isimlerini döndür."""
    return [
        "building_age", "floor_count", "hazard_score",
        "age_normalized", "floors_normalized", "hazard_normalized",
        "soil_ordinal", "system_ordinal", "retrofit_ordinal",
        "is_existing", "soil_risk_score", "system_risk_score",
    ]
