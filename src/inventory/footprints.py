"""
RiskTwin — Yapı Envanteri / Footprint edinimi (Adım 1).

Pilot için bina footprint'leri OpenStreetMap'ten (Overpass API) çekilir:
gerçek poligonlar, ODbL lisansı (atıf şart), bbox ile sorgulanabilir ve
`building:levels` / `height` / `start_date` gibi öznitelik tag'leri taşır.

Ölçeklenme notu: Ulusal ölçekte Microsoft GlobalMLBuildingFootprints (ODbL,
TR ~5,8M bina) birincil kaynaktır; bu modülün `load_microsoft_*` yolu o veri
için ayrılmıştır. 6 günlük pilotta OSM Overpass kullanılır (güvenilir, anlık).
"""
from __future__ import annotations

import json
import math
import os
from typing import Dict, List, Tuple

import requests

from src.config import RAW_DIR

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]
_HEADERS = {
    "User-Agent": "RiskTwin/1.0 (deprem yapi envanteri pilotu)",
    "Accept": "application/json",
}

# ── Pilot bölge: Zeytinburnu, İstanbul (yüksek deprem riski, mikrobölgelemeli) ──
# bbox = (güney_lat, batı_lon, kuzey_lat, doğu_lon); ~3000 bina
ZEYTINBURNU_BBOX: Tuple[float, float, float, float] = (41.000, 28.898, 41.010, 28.912)
PILOT_DISTRICT = "Zeytinburnu"
FOOTPRINT_LICENSE = "© OpenStreetMap katkıda bulunanlar (ODbL)"


def _ring_area_m2(ring: List[Tuple[float, float]]) -> float:
    """(lon, lat) halkasının alanını m² olarak yaklaşık hesapla (shoelace + enlem ölçeği)."""
    if len(ring) < 3:
        return 0.0
    lat0 = sum(p[1] for p in ring) / len(ring)
    mlon = 111320.0 * math.cos(math.radians(lat0))
    mlat = 110540.0
    xs = [lon * mlon for lon, lat in ring]
    ys = [lat * mlat for lon, lat in ring]
    a = 0.0
    for i in range(len(ring)):
        j = (i + 1) % len(ring)
        a += xs[i] * ys[j] - xs[j] * ys[i]
    return round(abs(a) / 2.0, 1)


def _cache_path(district: str) -> str:
    os.makedirs(RAW_DIR, exist_ok=True)
    return os.path.join(RAW_DIR, f"osm_buildings_{district.lower()}.json")


def _overpass_request(query: str, timeout: int) -> List[Dict]:
    """Overpass'a başlıklı istek; aynalar arasında yedekli."""
    last_err = None
    for url in OVERPASS_MIRRORS:
        try:
            resp = requests.post(
                url, data={"data": query}, headers=_HEADERS, timeout=timeout + 30
            )
            resp.raise_for_status()
            return resp.json().get("elements", [])
        except Exception as exc:  # noqa: BLE001 - sonraki aynayı dene
            last_err = exc
            continue
    raise RuntimeError(f"Tüm Overpass aynaları başarısız: {last_err}")


def fetch_osm_buildings(
    bbox: Tuple[float, float, float, float] = ZEYTINBURNU_BBOX,
    district: str = PILOT_DISTRICT,
    timeout: int = 120,
    use_cache: bool = True,
) -> List[Dict]:
    """
    Overpass'tan bbox içindeki bina footprint'lerini çek.
    Returns: her bina için {osm_id, ring[(lon,lat)], centroid(lat,lon), area_m2, tags}.
    İndirilen ham yanıt data/raw/ altına önbelleğe alınır.
    """
    cache = _cache_path(district)
    if use_cache and os.path.exists(cache):
        with open(cache, "r", encoding="utf-8") as f:
            elements = json.load(f)
    else:
        s, w, n, e = bbox
        query = (
            f"[out:json][timeout:{timeout}];"
            f'(way["building"]({s},{w},{n},{e}););'
            f"out geom;"
        )
        elements = _overpass_request(query, timeout)
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(elements, f)

    buildings: List[Dict] = []
    for el in elements:
        geom = el.get("geometry")
        if not geom or len(geom) < 3:
            continue
        ring = [(pt["lon"], pt["lat"]) for pt in geom]
        cx = sum(p[0] for p in ring) / len(ring)
        cy = sum(p[1] for p in ring) / len(ring)
        buildings.append({
            "osm_id": el.get("id"),
            "ring": ring,
            "centroid": (round(cy, 6), round(cx, 6)),  # (lat, lon)
            "area_m2": _ring_area_m2(ring),
            "tags": el.get("tags", {}) or {},
        })
    return buildings
