"""
RiskTwin — Bina özniteliği çıkarımı (Adım 1, yapı katmanı).

OSM tag'lerinden yapı-düzeyi öznitelikleri provenanslı çıkarır. Bilinmeyenler
GİZLENMEZ; "belirlenemedi" olarak işaretlenir (tasarım ilkesi 10.3). Pratikte
yaş ve taşıyıcı sistem çoğunlukla belirlenemez — bu bir kusur değil, sistemin
"eksik-veri görünürlüğü" değer önerisidir (saha kontrol listesini üretir).
"""
from __future__ import annotations

from datetime import date
from typing import Dict

from src.inventory.record import AttributeRecord, AttrStatus

_CURRENT_YEAR = date.today().year

# OSM building tag → kullanım tipi
_USAGE_MAP = {
    "residential": "konut", "apartments": "konut", "house": "konut",
    "detached": "konut", "dormitory": "konut", "terrace": "konut",
    "commercial": "ticari", "retail": "ticari", "shop": "ticari",
    "office": "ofis", "industrial": "sanayi", "warehouse": "sanayi",
    "school": "egitim", "university": "egitim", "hospital": "saglik",
}


def _parse_int(value) -> int | None:
    try:
        return int(float(str(value).split(";")[0].strip()))
    except (ValueError, TypeError):
        return None


def extract_attributes(tags: Dict, area_m2: float) -> Dict[str, AttributeRecord]:
    """OSM tag'lerinden provenanslı öznitelik kayıtları üret."""
    attrs: Dict[str, AttributeRecord] = {}

    # ── Kat sayısı ──
    levels = _parse_int(tags.get("building:levels"))
    height = _parse_int(tags.get("height"))
    if levels is not None and levels > 0:
        attrs["floor_count"] = AttributeRecord(
            value=levels, source="OSM building:levels", confidence=0.85, status=AttrStatus.OBSERVED)
    elif height is not None and height > 0:
        attrs["floor_count"] = AttributeRecord(
            value=max(1, round(height / 3.0)), source="OSM height (≈3 m/kat)",
            confidence=0.5, status=AttrStatus.NEEDS_FIELD)
    else:
        attrs["floor_count"] = AttributeRecord(
            value=None, source="OSM (kat tag'i yok)", status=AttrStatus.UNDETERMINED)

    # ── Bina yaşı ──
    start = tags.get("start_date") or tags.get("year_of_construction")
    yr = _parse_int(str(start)[:4]) if start else None
    if yr is not None and 1900 <= yr <= _CURRENT_YEAR:
        attrs["building_age"] = AttributeRecord(
            value=_CURRENT_YEAR - yr, source="OSM start_date", confidence=0.7, status=AttrStatus.OBSERVED)
    else:
        # Yaş, MVP'de büyük oranda belirlenemez → ortofoto tarihleme (sonraki tur).
        attrs["building_age"] = AttributeRecord(
            value=None, source="ortofoto tarihleme gerekli", status=AttrStatus.UNDETERMINED)

    # ── Taşıyıcı sistem ── (OSM'de kodlanmaz → belirlenemez; saha/proje gerekli)
    attrs["structural_system"] = AttributeRecord(
        value=None, source="dış görüntüden çıkarılamaz", status=AttrStatus.UNDETERMINED)

    # ── Kullanım tipi ──
    btag = str(tags.get("building", "")).lower()
    usage = _USAGE_MAP.get(btag)
    if usage:
        attrs["usage_type"] = AttributeRecord(
            value=usage, source="OSM building tag", confidence=0.7, status=AttrStatus.OBSERVED)
    elif btag in ("yes", ""):
        attrs["usage_type"] = AttributeRecord(
            value="konut", source="varsayılan (tag yok)", confidence=0.3, status=AttrStatus.NEEDS_FIELD)
    else:
        attrs["usage_type"] = AttributeRecord(
            value=None, source="OSM (bilinmiyor)", status=AttrStatus.UNDETERMINED)

    # ── Mevcut bina / güçlendirme (envanterde mevcut yapı kabul; güçlendirme bilinmiyor) ──
    attrs["is_existing_building"] = AttributeRecord(
        value=True, source="envanter varsayımı", confidence=0.9, status=AttrStatus.OBSERVED)
    attrs["retrofit_status"] = AttributeRecord(
        value="yok", source="varsayılan (kayıt yok)", confidence=0.3, status=AttrStatus.NEEDS_FIELD)

    return attrs
