"""
RiskTwin - Senaryo Karşılaştırma Sayfası
Before/after karşılaştırma, delta göstergeleri, öneriler.
"""
import streamlit as st

from src.config import SYSTEM_LABELS, SOIL_LABELS, RETROFIT_OPTIONS
from src.scoring_engine import evaluate_building
from src.scenario_engine import get_predefined_scenarios, create_custom_scenario
from src.explainability import generate_scenario_explanation

from components.metric_cards import render_rich_text_card, render_disclaimer
from components.charts import create_scenario_comparison_chart
from components.styles import RISK_COLORS


def render_scenario(locations):
    # ── Header ──
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Scenario Modeling</div>
        <h1 class="page-title">Senaryo Karşılaştırma</h1>
        <p class="page-summary">
            Güçlendirme, kat azaltma ve alternatif tasarım senaryolarının risk üzerindeki etkisini
            aynı karar çerçevesi içinde karşılaştırın.
        </p>
        <div class="page-tags">
            <span class="page-tag">Before / after karşılaştırma</span>
            <span class="page-tag">Delta okunabilirliği</span>
            <span class="page-tag">Özel senaryo üretimi</span>
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

    st.markdown(
        f"""
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1.1rem;">
            <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Baz Vaka</div>
                    <div class="summary-value" style="font-size:1.05rem;">{sc_loc_name}</div>
                    <div class="summary-caption">{sc_loc["hazard_level"]} tehlike seviyesi</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Yapı Profili</div>
                    <div class="summary-value" style="font-size:1.05rem;">{sc_age}Y / {sc_floors}K</div>
                    <div class="summary-caption">{SYSTEM_LABELS[sc_system]}</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Güçlendirme Durumu</div>
                    <div class="summary-value" style="font-size:1.05rem;">{ {"yok":"Yok","kismen":"Kısmi","tam":"Tam"}[sc_retrofit] }</div>
                    <div class="summary-caption">Senaryo öncesi durum</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Amaç</div>
                    <div class="status-chip" style="background:rgba(34,197,94,0.12); border-color:rgba(34,197,94,0.26); color:#86EFAC;">Delta okunabilirliği</div>
                    <div class="summary-caption" style="margin-top:0.4rem;">Hangi müdahale daha etkili sorusuna hızlı cevap</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Mevcut Durum Kartı ──
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">MEVCUT DURUM</div>', unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        band = base_eval["risk_band"]
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Risk Skoru</div>
            <div class="summary-value" style="color:{band['color']};">{base_eval['risk_score']}</div>
            <div class="summary-caption">{band['label']} bandı</div>
        </div>""", unsafe_allow_html=True)
    with mc2:
        fit = base_eval["project_fit_score"]
        fc = RISK_COLORS["low"] if fit >= 60 else RISK_COLORS["medium"] if fit >= 40 else RISK_COLORS["high"]
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Uygunluk</div>
            <div class="summary-value" style="color:{fc};">{fit}</div>
            <div class="summary-caption">{"Uygun" if fit >= 60 else "Koşullu" if fit >= 40 else "Riskli"}</div>
        </div>""", unsafe_allow_html=True)
    with mc3:
        pc = RISK_COLORS["high"] if base_eval["inspection_priority"] == "Yüksek" else RISK_COLORS["medium"] if base_eval["inspection_priority"] == "Orta" else RISK_COLORS["low"]
        st.markdown(f"""
        <div class="rt-card summary-card">
            <div class="summary-eyebrow">Öncelik</div>
            <div class="summary-value" style="font-size:1.55rem; color:{pc};">{base_eval['inspection_priority']}</div>
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
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">SENARYO KARŞILAŞTIRMASI</div>', unsafe_allow_html=True)

    scenarios = get_predefined_scenarios(base_params)

    if not scenarios:
        st.info("Mevcut parametreler için otomatik senaryo üretilemedi. Aşağıdan özel senaryo oluşturabilirsiniz.")
    else:
        st.markdown(
            """
            <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1rem;">
                <div style="display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
                    <div>
                        <div class="summary-eyebrow">Karşılaştırma Mantığı</div>
                        <div style="color:#F8FAFC; font-weight:600;">Delta ve uygunluk aynı kartta okunur.</div>
                        <div class="summary-caption">İyileşme yeşil, dikkat gerektiren farklar sıcak tonlarla vurgulanır.</div>
                    </div>
                    <div>
                        <div class="summary-eyebrow">Operasyon Modu</div>
                        <div class="status-chip">Senaryo komuta görünümü</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
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

            st.markdown(f"""
            <div class="rt-card" style="padding:1rem 1.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                    <div style="flex:1; min-width:200px;">
                        <div style="color:#F8FAFC; font-weight:600; font-size:0.95rem;">{sc['scenario_name']}</div>
                        <div style="color:#94A3B8; font-size:0.8rem; margin-top:0.25rem;">{recommendation_preview[:120]}...</div>
                    </div>
                    <div style="display:flex; gap:2rem; align-items:center; margin-top:0.5rem;">
                        <div style="text-align:center;">
                            <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase;">Risk</div>
                            <div style="color:#F8FAFC; font-weight:700;">{sc['base_risk_score']} → {sc['new_risk_score']}</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase;">Delta</div>
                            <div style="color:{delta_color}; font-weight:800; font-size:1.2rem;">{arrow} {abs(delta):.1f}</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="color:#64748B; font-size:0.7rem; text-transform:uppercase;">Uygunluk</div>
                            <div style="color:#F8FAFC; font-weight:700;">{sc['base_project_fit_score']} → {sc['new_project_fit_score']}</div>
                        </div>
                    </div>
                </div>
                <div style="margin-top:0.9rem; padding-top:0.9rem; border-top:1px solid rgba(148,163,184,0.08); display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
                    <div class="summary-caption" style="max-width:70%;">{recommendation_preview}</div>
                    <div class="status-chip" style="background:{'rgba(34,197,94,0.12)' if delta < 0 else 'rgba(245,158,11,0.12)'}; border-color:{'rgba(34,197,94,0.24)' if delta < 0 else 'rgba(245,158,11,0.24)'}; color:{'#86EFAC' if delta < 0 else '#FCD34D'};">
                        {"Risk azalıyor" if delta < 0 else "Dikkat gerekli"}
                    </div>
                </div>
                {band_change}
            </div>
            """, unsafe_allow_html=True)

    # ── Özel Senaryo ──
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
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

            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                st.metric("Mevcut Risk", f"{custom_sc['base_risk_score']}/100")
            with rc2:
                st.metric("Yeni Risk", f"{custom_sc['new_risk_score']}/100",
                           delta=f"{cd:+.1f}", delta_color="inverse")
            with rc3:
                st.metric("Uygunluk Değişimi", f"{custom_sc['new_project_fit_score']}/100",
                           delta=f"{custom_sc['delta_fit']:+.1f}")

            st.markdown(
                f"""
                <div class="rt-card" style="padding:1rem 1.15rem;">
                    <div class="summary-eyebrow">Özel Senaryo Özeti</div>
                    <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:0.9rem;">
                        <div>
                            <div class="summary-value" style="font-size:1.15rem; color:{cd_color};">{cd_arrow} {abs(cd):.1f}</div>
                            <div class="summary-caption">Risk delta</div>
                        </div>
                        <div>
                            <div class="summary-value" style="font-size:1.15rem;">{SYSTEM_LABELS[custom_system]}</div>
                            <div class="summary-caption">Yeni taşıyıcı sistem</div>
                        </div>
                        <div>
                            <div class="summary-value" style="font-size:1.15rem;">{ {"yok":"Yok","kismen":"Kısmi","tam":"Tam"}[custom_retrofit] }</div>
                            <div class="summary-caption">Güçlendirme kararı</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            render_rich_text_card(generate_scenario_explanation(custom_sc))

    render_disclaimer()
