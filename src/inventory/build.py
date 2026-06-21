"""
RiskTwin — Pilot envanteri üretimi (Adım 1 → Adım 2 köprüsü).

footprint (OSM) + site bağlamı (AFAD/İBB) + öznitelik çıkarımı → provenanslı
BuildingRecord → mevcut skor motoru (evaluate_building). Çıktı:
  - data/processed/pilot_inventory_<ilçe>.csv     (provenanslı düz tablo + skor)
  - data/processed/pilot_inventory_<ilçe>.geojson (harita için geometri + skor)

Çalıştırma:  python -m src.inventory.build
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Tuple

import pandas as pd

from src.config import PROCESSED_DIR
from src.inventory.attributes import extract_attributes
from src.inventory.footprints import (
    FOOTPRINT_LICENSE,
    PILOT_DISTRICT,
    ZEYTINBURNU_BBOX,
    fetch_osm_buildings,
)
from src.inventory.record import BuildingRecord
from src.inventory.site_context import get_site_context
from src.scoring_engine import evaluate_building


def build_records(bbox=ZEYTINBURNU_BBOX, district=PILOT_DISTRICT, limit=None) -> List[Dict]:
    """Footprint → site → öznitelik → BuildingRecord + skor. Returns satır+geometri listesi."""
    buildings = fetch_osm_buildings(bbox, district)
    if limit:
        buildings = buildings[:limit]

    out: List[Dict] = []
    for i, b in enumerate(buildings):
        lat, lon = b["centroid"]
        rec = BuildingRecord(building_id=f"{district[:2].upper()}{i + 1:05d}", location_id=district)

        site = get_site_context(lat, lon)
        rec.set("hazard", site["hazard_score"], source=site["hazard_source"], confidence=site["hazard_conf"])
        rec.set("soil_class", site["soil_class"], source=site["soil_source"], confidence=site["soil_conf"])

        for name, ar in extract_attributes(b["tags"], b["area_m2"]).items():
            rec.attributes[name] = ar

        res = evaluate_building(**rec.to_scoring_kwargs())

        row = rec.to_row()
        row.update({
            "lat": lat, "lon": lon, "area_m2": b["area_m2"], "osm_id": b["osm_id"],
            "risk_score": res["risk_score"], "risk_band": res["risk_band"]["label"],
            "data_status": res["data_status"], "needs_field_check": res["needs_field_check"],
            "triage_note": res["triage_note"],
        })
        out.append({"row": row, "ring": b["ring"], "lat": lat, "lon": lon, "result": res, "id": rec.building_id})
    return out


def _to_geojson(items: List[Dict]) -> Dict:
    features = []
    for it in items:
        r, res = it["row"], it["result"]
        features.append({
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [[[lon, lat] for lon, lat in it["ring"]]]},
            "properties": {
                "building_id": it["id"],
                "risk_score": res["risk_score"],
                "risk_band": res["risk_band"]["label"],
                "data_status": res["data_status"],
                "completeness": res["completeness"],
                "needs_field_check": res["needs_field_check"],
            },
        })
    return {"type": "FeatureCollection", "license": FOOTPRINT_LICENSE, "features": features}


def build_pilot_inventory(bbox=ZEYTINBURNU_BBOX, district=PILOT_DISTRICT, limit=None) -> Tuple[str, str, pd.DataFrame]:
    """Pilot envanterini üret, CSV + GeoJSON yaz, özet DataFrame döndür."""
    items = build_records(bbox, district, limit)
    df = pd.DataFrame([it["row"] for it in items])

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    slug = district.lower()
    csv_path = os.path.join(PROCESSED_DIR, f"pilot_inventory_{slug}.csv")
    geojson_path = os.path.join(PROCESSED_DIR, f"pilot_inventory_{slug}.geojson")
    df.to_csv(csv_path, index=False)
    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(_to_geojson(items), f)
    return csv_path, geojson_path, df


def _summary(df: pd.DataFrame) -> str:
    n = len(df)
    floors_known = (df["floor_count__status"] == "gozlemlendi").sum()
    age_known = (df["building_age__status"] == "gozlemlendi").sum()
    field = df["needs_field_check"].sum()
    bands = df["risk_band"].value_counts().to_dict()
    status = df["data_status"].value_counts().to_dict()
    return (
        f"Toplam bina: {n}\n"
        f"  Kat sayısı biliniyor : {floors_known} (%{100*floors_known/n:.0f})\n"
        f"  Bina yaşı biliniyor   : {age_known} (%{100*age_known/n:.0f})\n"
        f"  Saha kontrolü gerekli : {field} (%{100*field/n:.0f})\n"
        f"  Veri durumu           : {status}\n"
        f"  Risk bandı dağılımı   : {bands}\n"
    )


if __name__ == "__main__":
    csv_path, geojson_path, df = build_pilot_inventory()
    print("Yazıldı:", csv_path)
    print("Yazıldı:", geojson_path)
    print("-" * 50)
    print(_summary(df))
