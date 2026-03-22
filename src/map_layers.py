"""
RiskTwin Harita Katmanları
Folium tabanlı harita oluşturma, renk kodlama ve popup üretimi.
"""
import json
import os
from typing import Dict, List, Optional

import folium
from folium.plugins import MarkerCluster

from src.config import (
    DEFAULT_MAP_CENTER,
    DEFAULT_MAP_ZOOM,
    BUILDINGS_GEOJSON,
    NEIGHBORHOODS_GEOJSON,
    ROADS_GEOJSON,
    POIS_GEOJSON,
)


def risk_color(score: float) -> str:
    """Risk skorunu renk koduna çevir (yeşil → sarı → kırmızı)."""
    if score < 40:
        return "#27ae60"  # yeşil
    elif score < 65:
        return "#f39c12"  # turuncu
    else:
        return "#e74c3c"  # kırmızı


def create_base_map(
    center: List[float] = None,
    zoom: int = None,
) -> folium.Map:
    """İstanbul merkezli temel harita oluştur."""
    center = center or DEFAULT_MAP_CENTER
    zoom = zoom or DEFAULT_MAP_ZOOM
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="OpenStreetMap",
        control_scale=True,
    )
    return m


def add_building_markers(
    m: folium.Map,
    buildings: List[Dict],
    evaluations: Optional[Dict[str, Dict]] = None,
) -> folium.Map:
    """Bina noktalarını haritaya ekle. Değerlendirme varsa renklendir."""
    for bld in buildings:
        lat = bld.get("lat")
        lon = bld.get("lon")
        bid = bld.get("building_id", "")
        name = bld.get("location_name", bid)

        if lat is None or lon is None:
            continue

        # Değerlendirme varsa renkle
        color = "#3498db"  # varsayılan mavi
        risk_text = ""
        if evaluations and bid in evaluations:
            ev = evaluations[bid]
            color = risk_color(ev["risk_score"])
            risk_text = (
                f"<br><b>Risk Skoru:</b> {ev['risk_score']}/100"
                f"<br><b>Risk Bandı:</b> {ev['risk_band']['label']}"
                f"<br><b>Öncelik:</b> {ev['inspection_priority']}"
            )

        popup_html = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 0 0 5px 0;">{name}</h4>
            <b>ID:</b> {bid}
            {risk_text}
        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=name,
        ).add_to(m)

    return m


def add_location_marker(
    m: folium.Map,
    lat: float,
    lon: float,
    name: str = "Seçilen Konum",
    evaluation: Optional[Dict] = None,
) -> folium.Map:
    """Tek bir lokasyon işaretçisi ekle (kullanıcı seçimi için)."""
    color = "#3498db"
    if evaluation:
        color = risk_color(evaluation["risk_score"])

    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name,
        icon=folium.Icon(
            color="red" if color == "#e74c3c" else "orange" if color == "#f39c12" else "green",
            icon="building",
            prefix="fa",
        ),
    ).add_to(m)
    return m


def add_neighborhood_boundaries(m: folium.Map) -> folium.Map:
    """Mahalle sınırlarını haritaya ekle."""
    if not os.path.exists(NEIGHBORHOODS_GEOJSON):
        return m

    try:
        with open(NEIGHBORHOODS_GEOJSON, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        folium.GeoJson(
            geojson_data,
            name="Mahalle Sınırları",
            style_function=lambda x: {
                "fillColor": "#3498db",
                "color": "#2980b9",
                "weight": 2,
                "fillOpacity": 0.1,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["name", "district"],
                aliases=["Mahalle:", "İlçe:"],
            ),
        ).add_to(m)
    except Exception:
        pass  # Dosya okunamazsa sessizce geç

    return m


def add_geojson_layer(
    m: folium.Map,
    geojson_path: str,
    layer_name: str,
    style: Optional[Dict] = None,
) -> folium.Map:
    """Genel amaçlı GeoJSON katmanı ekle."""
    if not os.path.exists(geojson_path):
        return m

    try:
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        default_style = {
            "fillColor": "#95a5a6",
            "color": "#7f8c8d",
            "weight": 1,
            "fillOpacity": 0.3,
        }
        final_style = style or default_style

        folium.GeoJson(
            geojson_data,
            name=layer_name,
            style_function=lambda x, s=final_style: s,
        ).add_to(m)
    except Exception:
        pass

    return m


def create_risk_map(
    buildings: List[Dict],
    evaluations: Optional[Dict[str, Dict]] = None,
    selected_lat: Optional[float] = None,
    selected_lon: Optional[float] = None,
    selected_name: Optional[str] = None,
    selected_evaluation: Optional[Dict] = None,
    show_neighborhoods: bool = True,
) -> folium.Map:
    """Tam özellikli risk haritası oluştur."""
    # Haritayı oluştur
    if selected_lat and selected_lon:
        m = create_base_map(center=[selected_lat, selected_lon], zoom=14)
    else:
        m = create_base_map()

    # Mahalle sınırlarını ekle
    if show_neighborhoods:
        add_neighborhood_boundaries(m)

    # Bina işaretçilerini ekle
    add_building_markers(m, buildings, evaluations)

    # Seçilen lokasyonu vurgula
    if selected_lat and selected_lon:
        add_location_marker(
            m, selected_lat, selected_lon,
            name=selected_name or "Seçilen Konum",
            evaluation=selected_evaluation,
        )

    # Katman kontrolü ekle
    folium.LayerControl().add_to(m)

    return m
