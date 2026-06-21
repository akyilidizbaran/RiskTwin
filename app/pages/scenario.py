"""
RiskTwin - Senaryo Karşılaştırma Sayfası
Before/after karşılaştırma, delta göstergeleri, öneriler.
"""
import streamlit as st

from src.config import SYSTEM_LABELS, SOIL_LABELS, RETROFIT_OPTIONS
from src.scoring_engine import evaluate_building
from src.scenario_engine import get_predefined_scenarios, create_custom_scenario
from src.explainability import generate_scenario_explanation

from components.metric_cards import render_rich_text_card, render_disclaimer, render_summary_grid
from components.charts import create_scenario_comparison_chart
from components.styles import RISK_COLORS


def render_scenario(locations):
    # ── Header ──
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Scenario Modeling</div>
        <h1 class="page-title">Senaryo Karşılaştırma</h1>
        <p class="page-summary">
            Güçlendirme, kat azaltma ve alternatif senaryoların risk etkisini karşılaştırın. Consequence odaklı çıktı uzayı ile karar desteği.
        </p>
        <div class="page-tags">
            <span class="page-tag">Before / After</span>
            <span class="page-tag">Delta analizi</span>
            <span class="page-tag">Özel senaryo</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Temel Parametreler ──
    st.markdown('<div class="section-header">TEMEL YAPI PARAMETRELERİ</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        loc_options = {v["location_name"]: k for k, v in locations.items()}
        sc_loc_name = st.selectbox("Lokasyon", list(loc_options.keys()), key="sc_loc")
        sc_loc_id = loc_options[sc_loc_name]
        sc_loc = locations[sc_loc_id]
        sc_age = st.slider("Bina Yaşı", 0, 100, 30, key="sc_age")

    with col2:
        sc_floors = st.slider("Kat Sayısı", 1, 40, 6, key="sc_floors")
        sc_system = st.selectbox("Taşıyıcı Sistem", list(SYSTEM_LABELS.keys()),
                                  format_func=lambda x: SYSTEM_LABELS[x], index=2, key="sc_system")

    with col3:
        sc_soil = st.selectbox("Zemin Sınıfı", list(SOIL_LABELS.keys()),
                                format_func=lambda x: SOIL_LABELS[x], index=2, key="sc_soil")
        sc_existing = st.toggle("Mevcut Bina", value=True, key="sc_existing")
        sc_retrofit = st.selectbox("Güçlendirme", RETROFIT_OPTIONS,
                                    format_func=lambda x: {"yok": "Yok", "kismen": "Kısmi", "tam": "Tam"}[x],
                                    key="sc_retrofit")

    base_params = {
        "hazard_score": sc_loc["hazard_score"],
        "hazard_level": sc_loc["hazard_level"],
        "soil_class": sc_soil,
        "building_age": sc_age,
        "floor_count": sc_floors,
        "structural_system": sc_system,
        "is_existing_building": sc_existing,
        "retrofit_status": sc_retrofit,
    }

    base_eval = evaluate_building(**base_params)
    retrofit_label = {"yok": "Yok", "kismen": "Kısmi", "tam": "Tam"}[sc_retrofit]

    st.markdown('<div class="rt-spacer-sm"></div>', unsafe_allow_html=True)

    # ── Mevcut Durum Kartı ──
    st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">MEVCUT DURUM</div>', unsafe_allow_html=True)

    band = base_eval["risk_band"]
    fit = base_eval["project_fit_score"]
    fit_color = RISK_COLORS["low"] if fit >= 60 else RISK_COLORS["medium"] if fit >= 40 else RISK_COLORS["high"]
    fit_label = "Uygun" if fit >= 60 else "Koşullu" if fit >= 40 else "Riskli"
    priority = base_eval["inspection_priority"]
    priority_color = RISK_COLORS["high"] if priority == "Yüksek" else RISK_COLORS["medium"] if priority == "Orta" else RISK_COLORS["low"]

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Risk Skoru</div>
            <div class="summary-value" style="color:{band['color']};">{base_eval['risk_score']}</div>
            <div class="summary-caption">{band['label']} bandı</div>
        </div>""", unsafe_allow_html=True)
    with mc2:
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Uygunluk</div>
            <div class="summary-value" style="color:{fit_color};">{fit}</div>
            <div class="summary-caption">{fit_label}</div>
        </div>""", unsafe_allow_html=True)
    with mc3:
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Öncelik</div>
            <div class="summary-value" style="font-size:1.55rem; color:{priority_color};">{priority}</div>
            <div class="summary-caption">İnceleme seviyesi</div>
        </div>""", unsafe_allow_html=True)
    with mc4:
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Lokasyon</div>
            <div class="summary-value" style="font-size:1.05rem;">{sc_loc_name}</div>
            <div class="summary-caption">Tehlike skoru {sc_loc['hazard_score']}/100</div>
        </div>""", unsafe_allow_html=True)

    # ── Senaryo Sonuçları ──
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">SENARYO KARŞILAŞTIRMASI</div>', unsafe_allow_html=True)

    scenarios = get_predefined_scenarios(base_params)

    if not scenarios:
        st.info("Mevcut parametreler için otomatik senaryo üretilemedi. Aşağıdan özel senaryo oluşturabilirsiniz.")
    else:
        # Grafik
        fig = create_scenario_comparison_chart(scenarios)
        st.plotly_chart(fig, use_container_width=True)

        # Senaryo kartları
        for sc in scenarios:
            delta = sc["delta_risk"]
            delta_color = RISK_COLORS["low"] if delta < 0 else RISK_COLORS["high"]
            arrow = "↓" if delta < 0 else "↑"
            recommendation_preview = sc["recommendation"].strip("'\"")
            band_change = ""
            if sc["base_band"] != sc["new_band"]:
                band_change = (
                    f'<span class="status-chip" style="margin-top:0.8rem;">'
                    f'{sc["base_band"]} → {sc["new_band"]}</span>'
                )

            chip_cls = "status-chip--positive" if delta < 0 else "status-chip--warning"
            chip_text = "Risk azalıyor" if delta < 0 else "Dikkat gerekli"

            st.markdown(f"""
            <div class="rt-card" style="padding:var(--rt-space-md) var(--rt-space-lg);">
                <div class="rt-scenario-row">
                    <div class="rt-scenario-row__info">
                        <div class="rt-scenario-row__title">{sc['scenario_name']}</div>
                        <div class="rt-scenario-row__preview">{recommendation_preview[:120]}...</div>
                    </div>
                    <div class="rt-scenario-metrics">
                        <div class="rt-scenario-metrics__item">
                            <div class="rt-scenario-metrics__label">Risk</div>
                            <div class="rt-scenario-metrics__value">{sc['base_risk_score']} → {sc['new_risk_score']}</div>
                        </div>
                        <div class="rt-scenario-metrics__item">
                            <div class="rt-scenario-metrics__label">Delta</div>
                            <div class="rt-scenario-metrics__delta" style="color:{delta_color};">{arrow} {abs(delta):.1f}</div>
                        </div>
                        <div class="rt-scenario-metrics__item">
                            <div class="rt-scenario-metrics__label">Uygunluk</div>
                            <div class="rt-scenario-metrics__value">{sc['base_project_fit_score']} → {sc['new_project_fit_score']}</div>
                        </div>
                    </div>
                </div>
                <div class="rt-scenario-footer">
                    <div class="summary-caption" style="max-width:70%;">{recommendation_preview}</div>
                    <div class="status-chip {chip_cls}">{chip_text}</div>
                </div>
                {band_change}
            </div>
            """, unsafe_allow_html=True)

    # ── Özel Senaryo ──
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">ÖZEL SENARYO</div>', unsafe_allow_html=True)

    with st.expander("Özel senaryo parametreleri belirle", expanded=False):
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            custom_floors = st.slider("Yeni Kat Sayısı", 1, 40, sc_floors, key="cust_fl")
        with cc2:
            custom_system = st.selectbox("Yeni Taşıyıcı Sistem", list(SYSTEM_LABELS.keys()),
                                          format_func=lambda x: SYSTEM_LABELS[x], key="cust_sys")
        with cc3:
            custom_soil = st.selectbox("Yeni Zemin Sınıfı", list(SOIL_LABELS.keys()),
                                        format_func=lambda x: SOIL_LABELS[x], key="cust_soil")
            custom_retrofit = st.selectbox("Yeni Güçlendirme", RETROFIT_OPTIONS,
                                            format_func=lambda x: {"yok": "Yok", "kismen": "Kısmi", "tam": "Tam"}[x],
                                            key="cust_ret")

        if st.button("Hesapla", type="primary"):
            custom_sc = create_custom_scenario(
                base_params, "Özel Senaryo",
                floor_count=custom_floors, structural_system=custom_system,
                soil_class=custom_soil, retrofit_status=custom_retrofit,
            )

            cd = custom_sc["delta_risk"]
            cd_color = RISK_COLORS["low"] if cd < 0 else RISK_COLORS["high"]
            cd_arrow = "↓" if cd < 0 else "↑"
            custom_retrofit_label = {"yok": "Yok", "kismen": "Kısmi", "tam": "Tam"}[custom_retrofit]

            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                st.metric("Mevcut Risk", f"{custom_sc['base_risk_score']}/100")
            with rc2:
                st.metric("Yeni Risk", f"{custom_sc['new_risk_score']}/100",
                           delta=f"{cd:+.1f}", delta_color="inverse")
            with rc3:
                st.metric("Uygunluk Değişimi", f"{custom_sc['new_project_fit_score']}/100",
                           delta=f"{custom_sc['delta_fit']:+.1f}")

            render_summary_grid([
                {"eyebrow": "Risk Delta", "value": f"{cd_arrow} {abs(cd):.1f}", "value_size": "var(--rt-text-lg)", "value_color": cd_color, "caption": "Risk delta"},
                {"eyebrow": "Taşıyıcı Sistem", "value": SYSTEM_LABELS[custom_system], "value_size": "var(--rt-text-lg)", "caption": "Yeni taşıyıcı sistem"},
                {"eyebrow": "Güçlendirme", "value": custom_retrofit_label, "value_size": "var(--rt-text-lg)", "caption": "Güçlendirme kararı"},
            ], columns=3)

            render_rich_text_card(generate_scenario_explanation(custom_sc))

    render_disclaimer()
