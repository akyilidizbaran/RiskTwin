"""
RiskTwin Veri İşleme Modülü
Veri doğrulama, eksik kolon kontrolü, geospatial katman yükleme.
"""
import warnings
from typing import Dict, List, Optional, Set

import pandas as pd

from src.config import SYSTEM_SCORE_MAP, SOIL_SCORE_MAP


# ── Gerekli Kolonlar ──

REQUIRED_HAZARD_COLUMNS = {
    "location_id", "location_name", "lat", "lon", "hazard_level", "hazard_score"
}

REQUIRED_BUILDING_COLUMNS = {
    "building_id", "location_id", "building_age", "floor_count",
    "structural_system", "soil_class", "is_existing_building"
}


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Set[str],
    name: str = "veri",
) -> List[str]:
    """
    DataFrame'de gerekli kolonları kontrol et.
    Returns: Eksik kolon isimleri listesi (boşsa tüm kolonlar mevcut).
    """
    missing = required_columns - set(df.columns)
    if missing:
        warnings.warn(
            f"'{name}' verisinde eksik kolonlar: {', '.join(sorted(missing))}. "
            f"Bu kolonlar olmadan bazı özellikler çalışmayabilir."
        )
    return sorted(missing)


def validate_hazard_data(df: pd.DataFrame) -> List[str]:
    """Tehlike verisini doğrula."""
    return validate_dataframe(df, REQUIRED_HAZARD_COLUMNS, "tehlike")


def validate_building_data(df: pd.DataFrame) -> List[str]:
    """Bina verisini doğrula."""
    return validate_dataframe(df, REQUIRED_BUILDING_COLUMNS, "bina")


def clean_building_data(df: pd.DataFrame) -> pd.DataFrame:
    """Bina verisini temizle ve eksik değerleri doldur."""
    df = df.copy()

    # Varsayılan değerler
    defaults = {
        "building_age": 25,
        "floor_count": 5,
        "structural_system": "betonarme_cerceve",
        "soil_class": "ZC",
        "usage_type": "konut",
        "is_existing_building": True,
        "retrofit_status": "yok",
    }

    for col, default in defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default)
        else:
            df[col] = default

    # Tip düzeltmeleri
    if "building_age" in df.columns:
        df["building_age"] = pd.to_numeric(df["building_age"], errors="coerce").fillna(25).astype(int)
    if "floor_count" in df.columns:
        df["floor_count"] = pd.to_numeric(df["floor_count"], errors="coerce").fillna(5).astype(int)
    if "is_existing_building" in df.columns:
        df["is_existing_building"] = df["is_existing_building"].astype(bool)

    # Geçersiz değer kontrolü
    valid_systems = set(SYSTEM_SCORE_MAP.keys())
    if "structural_system" in df.columns:
        df.loc[~df["structural_system"].isin(valid_systems), "structural_system"] = "betonarme_cerceve"

    valid_soils = set(SOIL_SCORE_MAP.keys())
    if "soil_class" in df.columns:
        df.loc[~df["soil_class"].isin(valid_soils), "soil_class"] = "ZC"

    return df


def merge_hazard_building(
    hazard_df: pd.DataFrame,
    building_df: pd.DataFrame,
) -> pd.DataFrame:
    """Tehlike ve bina verilerini birleştir."""
    if hazard_df.empty or building_df.empty:
        return building_df

    merged = building_df.merge(
        hazard_df[["location_id", "hazard_level", "hazard_score", "lat", "lon"]],
        on="location_id",
        how="left",
    )
    return merged


def prepare_evaluation_input(row: pd.Series) -> Dict:
    """DataFrame satırından skorlama motoru girdisi hazırla."""
    return {
        "hazard_score": row.get("hazard_score"),
        "hazard_level": row.get("hazard_level", "high"),
        "soil_class": row.get("soil_class", "ZC"),
        "building_age": int(row.get("building_age", 25)),
        "floor_count": int(row.get("floor_count", 5)),
        "structural_system": row.get("structural_system", "betonarme_cerceve"),
        "is_existing_building": bool(row.get("is_existing_building", True)),
        "retrofit_status": row.get("retrofit_status", "yok"),
    }
