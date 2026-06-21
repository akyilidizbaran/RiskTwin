"""
RiskTwin - Risk Analizi Sayfası
Profesyonel dashboard: harita, skor kartları, faktör analizi, açıklama.
"""
import streamlit as st
from streamlit_folium import st_folium

from src.config import SYSTEM_LABELS, SOIL_LABELS, USAGE_TYPES, RETROFIT_OPTIONS, SCORE_WEIGHTS
from src.scoring_engine import evaluate_building
from src.explainability import generate_risk_explanation
from src.map_layers import create_risk_map
from src.predict import predict_risk_class

from components.metric_cards import (
    render_score_card,
    render_fit_card,
    render_priority_card,
    render_rich_text_card,
    render_disclaimer,
    render_summary_grid,
)
from components.charts import create_factor_bar_chart, create_risk_gauge
from components.styles import COLORS


def render_risk_analysis(locations, hazard_df, building_df):
    # ── Header ──
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Interactive Evaluation</div>
        <h1 class="page-title">Risk Analizi</h1>
        <p class="page-summary">
            Bina parametrelerini hazard bağlamı ile birleştirerek deprem risk skoru,
            inceleme önceliği ve açıklanabilir faktör analizi üretin.
        </p>
        <div class="page-tags">
            <span class="page-tag">Hazard bağlamı</span>
            <span class="page-tag">Açıklanabilir skor</span>
            <span class="page-tag">İnceleme önceliği</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Layout: Input | Harita ──
    col_input, col_main = st.columns([1, 2])

    with col_input:
        st.markdown('<div class="section-header">YAPI PARAMETRELERİ</div>', unsafe_allow_html=True)

        # Lokasyon
        loc_options = {v["location_name"]: k for k, v in locations.items()}
        selected_name = st.selectbox("Lokasyon", list(loc_options.keys()), key="ra_loc")
        selected_loc_id = loc_options[selected_name]
        selected_loc = locations[selected_loc_id]

        st.markdown(
            f'<div class="rt-location-badge">'
            f'<span class="rt-location-badge__icon">LOC</span>'
            f'<span class="rt-location-badge__text">{selected_loc["district"]}, {selected_loc["city"]}</span>'
            f'<span class="rt-location-badge__coords">{selected_loc["lat"]:.4f}, {selected_loc["lon"]:.4f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        building_age = st.slider("Bina Yaşı (yıl)", 0, 100, 30, key="ra_age",
                                 help="Binanın inşaat tarihinden bu yana geçen süre")
        floor_count = st.slider("Kat Sayısı", 1, 40, 5, key="ra_floors",
                                help="Bodrum katlar dahil toplam kat sayısı")
        structural_system = st.selectbox("Taşıyıcı Sistem", list(SYSTEM_LABELS.keys()),
                                         format_func=lambda x: SYSTEM_LABELS[x], index=2, key="ra_system")
        soil_class = st.selectbox("Zemin Sınıfı", list(SOIL_LABELS.keys()),
                                   format_func=lambda x: SOIL_LABELS[x], index=2, key="ra_soil")
        usage_type = st.selectbox("Kullanım Tipi", USAGE_TYPES, key="ra_usage")

        uc1, uc2 = st.columns(2)
        with uc1:
            is_existing = st.toggle("Mevcut Bina", value=True, key="ra_existing")
        with uc2:
            retrofit_status = st.selectbox(
                "Güçlendirme",
                RETROFIT_OPTIONS,
                format_func=lambda x: {"yok": "Yok", "kismen": "Kısmi", "tam": "Tam"}[x],
                key="ra_retrofit",
            )

    # ── Değerlendirme ──
    evaluation = evaluate_building(
        hazard_score=selected_loc["hazard_score"],
        hazard_level=selected_loc["hazard_level"],
        soil_class=soil_class,
        building_age=building_age,
        floor_count=floor_count,
        structural_system=structural_system,
        is_existing_building=is_existing,
        retrofit_status=retrofit_status,
    )

    # ML prediction
    ml_result = predict_risk_class(
        hazard_score=selected_loc["hazard_score"],
        soil_class=soil_class,
        building_age=building_age,
        floor_count=floor_count,
        structural_system=structural_system,
        is_existing_building=is_existing,
        retrofit_status=retrofit_status,
    )

    model_status = "Aktif" if ml_result.get("prediction_method") == "ml" else "Hazır"
    model_caption = (
        ml_result.get("model_name", "Heuristic fallback")
        if ml_result.get("prediction_method") == "ml"
        else "ML pipeline hazır, heuristic öncelikli"
    )

    # ── Anlık skor göstergesi (input panelinde) ──
    risk_band = evaluation["risk_band"]
    _risk_color = {"Düşük": "#40916C", "Orta": "#F28C28", "Yüksek": "#E63946"}.get(risk_band["label"], "#F28C28")
    with col_input:
        st.markdown(f"""
        <div class="rt-card" style="margin-top:var(--rt-space-md); text-align:center; border-left:4px solid {_risk_color};">
            <div style="font-size:2rem; font-weight:800; color:{_risk_color};">{evaluation["risk_score"]}</div>
            <div style="font-size:0.8rem; font-weight:700; color:{_risk_color}; text-transform:uppercase; letter-spacing:0.1em;">{risk_band["label"]} Risk</div>
            <div style="margin-top:0.5rem; display:flex; justify-content:space-around;">
                <div style="text-align:center;">
                    <div style="font-size:1.1rem; font-weight:700; color:var(--rt-text);">{evaluation["project_fit_score"]}</div>
                    <div style="font-size:0.65rem; color:var(--rt-muted);">Uygunluk</div>
                </div>
                <div style="text-align:center;">
                    <div style="font-size:0.85rem; font-weight:700; color:var(--rt-text);">{evaluation["inspection_priority"]}</div>
                    <div style="font-size:0.65rem; color:var(--rt-muted);">Öncelik</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    render_summary_grid([
        {"eyebrow": "Seçili Lokasyon", "value": selected_name, "value_size": "var(--rt-text-lg)", "caption": f'{selected_loc["district"]}, {selected_loc["city"]}'},
        {"eyebrow": "Tehlike Skoru", "value": selected_loc["hazard_score"], "value_size": "1.35rem", "value_color": "var(--rt-blue)", "caption": f'{selected_loc["hazard_level"]} bandı'},
        {"eyebrow": "Parametre Durumu", "value": "7 / 7", "value_size": "var(--rt-text-lg)", "caption": "Karar girdisi tamamlandı"},
        {"eyebrow": "Model Katmanı", "value": model_status, "value_size": "var(--rt-text-lg)", "value_color": "var(--rt-emerald)", "caption": model_caption},
    ])

    # ── Harita ──
    with col_main:
        st.markdown('<div class="section-header">HARİTA</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="rt-card rt-card--compact">
                <div class="rt-flex-bar">
                    <div>
                        <div class="summary-eyebrow">Coğrafi Bağlam</div>
                        <div class="rt-accent-text" style="font-size:0.98rem;">{selected_loc["district"]} / {selected_loc["city"]}</div>
                        <div class="summary-caption">{selected_loc["lat"]:.4f}, {selected_loc["lon"]:.4f}</div>
                    </div>
                    <div>
                        <div class="summary-eyebrow">Risk Operasyonu</div>
                        <div class="status-chip status-chip--blue">Canlı lokasyon odaklı yorum</div>
                    </div>
                    <div>
                        <div class="summary-eyebrow">Okuma Notu</div>
                        <div class="summary-caption">Harita görseli, skor kartları ve açıklama aynı karar zincirine bağlıdır.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        building_list = [
            {"building_id": k, "location_name": v["location_name"], "lat": v["lat"], "lon": v["lon"]}
            for k, v in locations.items()
        ]

        risk_map = create_risk_map(
            buildings=building_list,
            selected_lat=selected_loc["lat"],
            selected_lon=selected_loc["lon"],
            selected_name=selected_name,
            selected_evaluation=evaluation,
        )
        st_folium(risk_map, width=None, height=420, returned_objects=[])

    # ── Skor Kartları ──
    st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">DEĞERLENDİRME SONUÇLARI</div>', unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        render_score_card("Deprem Risk Skoru", evaluation["risk_score"],
                          risk_band["label"], "Risk seviyesi")
    with sc2:
        render_fit_card("Proje Uygunluk Skoru", evaluation["project_fit_score"])
    with sc3:
        render_priority_card("İnceleme Önceliği", evaluation["inspection_priority"])

    # ── Faktör Analizi + Açıklama ──
    st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)
    col_chart, col_explain = st.columns([1, 1])

    with col_chart:
        st.markdown('<div class="section-header">SKORA KATKI YAPAN FAKTÖRLER</div>', unsafe_allow_html=True)
        fig = create_factor_bar_chart(evaluation["sub_scores"])
        st.plotly_chart(fig, use_container_width=True)

    with col_explain:
        st.markdown('<div class="section-header">AÇIKLAMA VE ÖNERİ</div>', unsafe_allow_html=True)
        explanation = generate_risk_explanation(evaluation)
        render_rich_text_card(explanation)
        st.markdown(
            f"""
            <div class="rt-card rt-card--compact">
                <div class="summary-eyebrow">Operasyon Özeti</div>
                <div class="metric-inline"><span class="metric-inline-label">Risk bandı</span><span class="metric-inline-value">{risk_band["label"]}</span></div>
                <div class="metric-inline"><span class="metric-inline-label">İnceleme önceliği</span><span class="metric-inline-value">{evaluation["inspection_priority"]}</span></div>
                <div class="metric-inline"><span class="metric-inline-label">Tahmin modu</span><span class="metric-inline-value">{model_status}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Veri Bileşenleri ──
    st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">VERİ BİLEŞENLERİ</div>', unsafe_allow_html=True)

    vb1, vb2, vb3, vb4 = st.columns(4)
    with vb1:
        st.markdown("""
        <div class="rt-card rt-data-cell">
            <div class="rt-data-cell__label rt-data-cell__label--active">&#x2713; AFAD Tehlike</div>
            <div class="rt-data-cell__caption">Risk çekirdeği</div>
        </div>""", unsafe_allow_html=True)
    with vb2:
        st.markdown("""
        <div class="rt-card rt-data-cell">
            <div class="rt-data-cell__label rt-data-cell__label--active">&#x2713; Zemin Sınıfı</div>
            <div class="rt-data-cell__caption">Kritik hassasiyet girdisi</div>
        </div>""", unsafe_allow_html=True)
    with vb3:
        st.markdown("""
        <div class="rt-card rt-data-cell">
            <div class="rt-data-cell__label rt-data-cell__label--active">&#x2713; Yapı Özellikleri</div>
            <div class="rt-data-cell__caption">Yapısal karar tabanı</div>
        </div>""", unsafe_allow_html=True)
    with vb4:
        st.markdown("""
        <div class="rt-card rt-data-cell">
            <div class="rt-data-cell__label rt-data-cell__label--pending">&#x25CB; Bağlam Verisi</div>
            <div class="rt-data-cell__caption">İkinci faz genişleme</div>
        </div>""", unsafe_allow_html=True)

    # ── Baseline ML Insight (model varsa) ──
    if ml_result.get("prediction_method") == "ml":
        st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">BASELINE ML INSIGHT</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rt-card">
            <div class="rt-ml-status">
                <div>
                    <div class="rt-accent-text--blue" style="font-size:var(--rt-text-base);">Model Status: Aktif</div>
                    <div class="summary-caption" style="margin-top:var(--rt-space-xs);">
                        Model: {ml_result.get('model_name', 'N/A')} |
                        Tahmin: {ml_result.get('ml_risk_label', 'N/A')} risk sınıfı
                    </div>
                </div>
                <div class="rt-ml-badge rt-ml-badge--untrained">Experimental</div>
            </div>
            <div class="rt-card__footer">
                Not: Baseline model demo veri üzerinde heuristic skorlardan bootstrap edilmiştir.
                Gerçek etiketli veri ile yeniden eğitim önerilir.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Disclaimer ──
    render_disclaimer()
