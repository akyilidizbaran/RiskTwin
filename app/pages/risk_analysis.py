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
            Bina parametrelerini girin, deprem risk skoru ile inceleme önceliğini aynı akışta görün
            ve etkili faktörleri görsel olarak yorumlayın.
        </p>
        <div class="page-tags">
            <span class="page-tag">Harita destekli karar ekranı</span>
            <span class="page-tag">Açıklanabilir skor dağılımı</span>
            <span class="page-tag">ML-ready tahmin katmanı</span>
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
            f'<div style="background:rgba(15,23,42,0.72); border:1px solid rgba(148,163,184,0.12); border-radius:14px; padding:0.6rem 0.8rem; margin-bottom:1rem;">'
            f'<span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:9px; '
            f'background:rgba(56,189,248,0.14); color:#8AD4FF; font-family:JetBrains Mono, monospace; font-size:0.72rem; margin-right:0.55rem;">LOC</span>'
            f'<span style="color:#CBD5E1; font-size:0.85rem;">{selected_loc["district"]}, {selected_loc["city"]}</span>'
            f'<span style="color:#64748B; font-size:0.75rem; margin-left:0.5rem;">'
            f'{selected_loc["lat"]:.4f}, {selected_loc["lon"]:.4f}</span>'
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

    st.markdown(
        f"""
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1.2rem;">
            <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Seçili Lokasyon</div>
                    <div class="summary-value" style="font-size:1.1rem;">{selected_name}</div>
                    <div class="summary-caption">{selected_loc["district"]}, {selected_loc["city"]}</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Tehlike Skoru</div>
                    <div class="summary-value" style="font-size:1.35rem; color:#38BDF8;">{selected_loc["hazard_score"]}</div>
                    <div class="summary-caption">{selected_loc["hazard_level"]} bandı</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Parametre Durumu</div>
                    <div class="summary-value" style="font-size:1.1rem;">7 / 7</div>
                    <div class="summary-caption">Karar girdisi tamamlandı</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Model Katmanı</div>
                    <div class="summary-value" style="font-size:1.1rem; color:#22C55E;">{model_status}</div>
                    <div class="summary-caption">{model_caption}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Harita ──
    with col_main:
        st.markdown('<div class="section-header">HARİTA</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="rt-card" style="padding:0.95rem 1.1rem; margin-bottom:0.85rem;">
                <div style="display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
                    <div>
                        <div class="summary-eyebrow">Coğrafi Bağlam</div>
                        <div style="color:#F8FAFC; font-weight:700; font-size:0.98rem;">{selected_loc["district"]} / {selected_loc["city"]}</div>
                        <div class="summary-caption">{selected_loc["lat"]:.4f}, {selected_loc["lon"]:.4f}</div>
                    </div>
                    <div>
                        <div class="summary-eyebrow">Risk Operasyonu</div>
                        <div class="status-chip" style="background:rgba(56,189,248,0.12); border-color:rgba(56,189,248,0.28); color:#8AD4FF;">Canlı lokasyon odaklı yorum</div>
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
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">DEĞERLENDİRME SONUÇLARI</div>', unsafe_allow_html=True)

    risk_band = evaluation["risk_band"]
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        render_score_card("Deprem Risk Skoru", evaluation["risk_score"],
                          risk_band["label"], "Risk seviyesi")
    with sc2:
        render_fit_card("Proje Uygunluk Skoru", evaluation["project_fit_score"])
    with sc3:
        render_priority_card("İnceleme Önceliği", evaluation["inspection_priority"])

    # ── Faktör Analizi + Açıklama ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    col_chart, col_explain = st.columns([1, 1])

    with col_chart:
        st.markdown('<div class="section-header">SKORA KATKI YAPAN FAKTÖRLER</div>', unsafe_allow_html=True)
        fig = create_factor_bar_chart(evaluation["sub_scores"])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            <div class="rt-card" style="padding:1rem 1.1rem;">
                <div class="summary-eyebrow">Analist Notu</div>
                <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.35rem;">Katkı dağılımı doğrudan aksiyon önceliğine çevrilir.</div>
                <div class="summary-caption">
                    Grafikte öne çıkan faktörler, öneri kartındaki doğal dil açıklaması ile birebir hizalanır.
                    Amaç sadece skor göstermek değil, karar gerekçesini görünür kılmaktır.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_explain:
        st.markdown('<div class="section-header">AÇIKLAMA VE ÖNERİ</div>', unsafe_allow_html=True)
        explanation = generate_risk_explanation(evaluation)
        render_rich_text_card(explanation)
        st.markdown(
            f"""
            <div class="rt-card" style="padding:1rem 1.1rem;">
                <div class="summary-eyebrow">Operasyon Özeti</div>
                <div class="metric-inline"><span class="metric-inline-label">Risk bandı</span><span class="metric-inline-value">{risk_band["label"]}</span></div>
                <div class="metric-inline"><span class="metric-inline-label">İnceleme önceliği</span><span class="metric-inline-value">{evaluation["inspection_priority"]}</span></div>
                <div class="metric-inline"><span class="metric-inline-label">Tahmin modu</span><span class="metric-inline-value">{model_status}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Veri Bileşenleri ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">VERİ BİLEŞENLERİ</div>', unsafe_allow_html=True)

    vb1, vb2, vb3, vb4 = st.columns(4)
    with vb1:
        st.markdown("""
        <div class="rt-card" style="text-align:center; padding:1rem;">
            <div style="color:#10B981; font-weight:600; font-size:0.8rem;">&#x2713; AFAD Tehlike</div>
            <div style="color:#64748B; font-size:0.75rem; margin-top:0.25rem;">Risk çekirdeği</div>
        </div>""", unsafe_allow_html=True)
    with vb2:
        st.markdown("""
        <div class="rt-card" style="text-align:center; padding:1rem;">
            <div style="color:#10B981; font-weight:600; font-size:0.8rem;">&#x2713; Zemin Sınıfı</div>
            <div style="color:#64748B; font-size:0.75rem; margin-top:0.25rem;">Kritik hassasiyet girdisi</div>
        </div>""", unsafe_allow_html=True)
    with vb3:
        st.markdown("""
        <div class="rt-card" style="text-align:center; padding:1rem;">
            <div style="color:#10B981; font-weight:600; font-size:0.8rem;">&#x2713; Yapı Özellikleri</div>
            <div style="color:#64748B; font-size:0.75rem; margin-top:0.25rem;">Yapısal karar tabanı</div>
        </div>""", unsafe_allow_html=True)
    with vb4:
        st.markdown("""
        <div class="rt-card" style="text-align:center; padding:1rem;">
            <div style="color:#F59E0B; font-weight:600; font-size:0.8rem;">&#x25CB; Bağlam Verisi</div>
            <div style="color:#64748B; font-size:0.75rem; margin-top:0.25rem;">İkinci faz genişleme</div>
        </div>""", unsafe_allow_html=True)

    # ── Baseline ML Insight (model varsa) ──
    if ml_result.get("prediction_method") == "ml":
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">BASELINE ML INSIGHT</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="rt-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:#0EA5E9; font-weight:600; font-size:0.85rem;">Model Status: Aktif</div>
                    <div style="color:#94A3B8; font-size:0.8rem; margin-top:0.25rem;">
                        Model: {ml_result.get('model_name', 'N/A')} |
                        Tahmin: {ml_result.get('ml_risk_label', 'N/A')} risk sınıfı
                    </div>
                </div>
                <div style="background:#1B2A4A; border-radius:8px; padding:0.5rem 1rem;">
                    <div style="color:#F59E0B; font-size:0.7rem; text-transform:uppercase;">Experimental</div>
                </div>
            </div>
            <div style="color:#64748B; font-size:0.75rem; margin-top:0.75rem; border-top:1px solid #334155; padding-top:0.5rem;">
                Not: Baseline model demo veri üzerinde heuristic skorlardan bootstrap edilmiştir.
                Gerçek etiketli veri ile yeniden eğitim önerilir.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Disclaimer ──
    render_disclaimer()
