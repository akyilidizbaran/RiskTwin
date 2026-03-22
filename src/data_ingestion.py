"""
RiskTwin Veri Yükleme Modülü
CSV/GeoJSON okuma, eksik dosya yönetimi, fallback demo veri üretimi.
"""
import json
import os
import warnings
from typing import Dict, List, Optional

import pandas as pd

from src.config import (
    HAZARD_CSV,
    BUILDING_CSV,
    POPULATION_CSV,
    BUILDINGS_GEOJSON,
    ROADS_GEOJSON,
    POIS_GEOJSON,
    NEIGHBORHOODS_GEOJSON,
)


# ── Fallback Demo Verileri ──

FALLBACK_HAZARD_DATA = [
    {"location_id": "LOC001", "location_name": "Kadıköy Moda", "city": "İstanbul", "district": "Kadıköy", "lat": 40.9862, "lon": 29.0262, "hazard_level": "high", "hazard_score": 75, "source": "AFAD", "notes": "Demo veri"},
    {"location_id": "LOC002", "location_name": "Beyoğlu Tarlabaşı", "city": "İstanbul", "district": "Beyoğlu", "lat": 41.0351, "lon": 28.9777, "hazard_level": "high", "hazard_score": 70, "source": "AFAD", "notes": "Demo veri"},
    {"location_id": "LOC003", "location_name": "Avcılar Merkez", "city": "İstanbul", "district": "Avcılar", "lat": 40.9792, "lon": 28.7214, "hazard_level": "high", "hazard_score": 90, "source": "AFAD", "notes": "Demo veri"},
    {"location_id": "LOC004", "location_name": "Kartal Sahil", "city": "İstanbul", "district": "Kartal", "lat": 40.8890, "lon": 29.1890, "hazard_level": "high", "hazard_score": 68, "source": "AFAD", "notes": "Demo veri"},
    {"location_id": "LOC005", "location_name": "Fatih Sultanahmet", "city": "İstanbul", "district": "Fatih", "lat": 41.0054, "lon": 28.9768, "hazard_level": "high", "hazard_score": 72, "source": "AFAD", "notes": "Demo veri"},
]

FALLBACK_BUILDING_DATA = [
    {"building_id": "BIN001", "location_id": "LOC001", "building_age": 45, "floor_count": 5, "structural_system": "betonarme_cerceve", "soil_class": "ZC", "usage_type": "konut", "is_existing_building": True, "retrofit_status": "yok"},
    {"building_id": "BIN002", "location_id": "LOC001", "building_age": 10, "floor_count": 3, "structural_system": "betonarme_perde", "soil_class": "ZC", "usage_type": "konut", "is_existing_building": True, "retrofit_status": "yok"},
    {"building_id": "BIN003", "location_id": "LOC002", "building_age": 60, "floor_count": 4, "structural_system": "yigma", "soil_class": "ZD", "usage_type": "ticari", "is_existing_building": True, "retrofit_status": "yok"},
    {"building_id": "BIN004", "location_id": "LOC003", "building_age": 30, "floor_count": 6, "structural_system": "betonarme_cerceve", "soil_class": "ZE", "usage_type": "konut", "is_existing_building": True, "retrofit_status": "yok"},
    {"building_id": "BIN005", "location_id": "LOC005", "building_age": 70, "floor_count": 3, "structural_system": "yigma", "soil_class": "ZD", "usage_type": "konut", "is_existing_building": True, "retrofit_status": "yok"},
]


def load_csv(file_path: str, fallback_data: Optional[List[Dict]] = None) -> pd.DataFrame:
    """CSV dosyası yükle. Eksikse fallback veri kullan."""
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            warnings.warn(f"CSV okuma hatası ({file_path}): {e}")

    if fallback_data:
        warnings.warn(f"Dosya bulunamadı: {file_path}. Demo veri kullanılıyor.")
        return pd.DataFrame(fallback_data)

    warnings.warn(f"Dosya bulunamadı ve fallback veri yok: {file_path}")
    return pd.DataFrame()


def load_geojson(file_path: str) -> Optional[Dict]:
    """GeoJSON dosyası yükle."""
    if not os.path.exists(file_path):
        warnings.warn(f"GeoJSON bulunamadı: {file_path}")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        warnings.warn(f"GeoJSON okuma hatası ({file_path}): {e}")
        return None


def load_hazard_data() -> pd.DataFrame:
    """AFAD tehlike verisini yükle."""
    return load_csv(HAZARD_CSV, FALLBACK_HAZARD_DATA)


def load_building_data() -> pd.DataFrame:
    """Bina girdi verisini yükle."""
    return load_csv(BUILDING_CSV, FALLBACK_BUILDING_DATA)


def load_population_data() -> pd.DataFrame:
    """TÜİK nüfus bağlam verisini yükle."""
    return load_csv(POPULATION_CSV)


def load_buildings_geojson() -> Optional[Dict]:
    """Bina footprint GeoJSON yükle."""
    return load_geojson(BUILDINGS_GEOJSON)


def get_location_options(hazard_df: pd.DataFrame) -> Dict[str, Dict]:
    """Hazard verisinden lokasyon seçenekleri oluştur."""
    locations = {}
    for _, row in hazard_df.iterrows():
        loc_id = row["location_id"]
        locations[loc_id] = {
            "location_id": loc_id,
            "location_name": row.get("location_name", loc_id),
            "city": row.get("city", "İstanbul"),
            "district": row.get("district", ""),
            "lat": row.get("lat", 41.0082),
            "lon": row.get("lon", 28.9784),
            "hazard_level": row.get("hazard_level", "high"),
            "hazard_score": row.get("hazard_score", 70),
        }
    return locations
