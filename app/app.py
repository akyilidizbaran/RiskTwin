"""
RiskTwin - Deprem Risk Değerlendirme ve Karar Destek Sistemi
Ana Streamlit Uygulaması (Çok Sayfalı)
"""
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, APP_DIR)

import streamlit as st

from components.styles import GLOBAL_CSS
from src.data_ingestion import load_hazard_data, load_building_data, get_location_options
from src.data_processing import clean_building_data

# ── Sayfa Ayarları ──
st.set_page_config(
    page_title="RiskTwin",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Veri Yükleme (cache) ──
@st.cache_data
def load_data():
    hazard_df = load_hazard_data()
    building_df = load_building_data()
    building_df = clean_building_data(building_df)
    locations = get_location_options(hazard_df)
    return hazard_df, building_df, locations

try:
    hazard_df, building_df, locations = load_data()
except Exception as e:
    st.error(f"Veri yükleme hatası: {e}")
    st.stop()

# ── Sidebar Navigasyon ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 0.6rem 0 0.9rem;">
        <div style="display:inline-flex; align-items:center; gap:0.55rem; padding:0.4rem 0.7rem; border-radius:999px;
            border:1px solid rgba(56,189,248,0.18); background:rgba(56,189,248,0.08); color:#8AD4FF; font-size:0.72rem;
            text-transform:uppercase; letter-spacing:0.16em; margin-bottom:1rem;">
            Risk Intelligence
        </div>
        <div style="font-size:2.2rem; font-weight:800; color:#F8FAFC; font-family:'JetBrains Mono', monospace;">
            RiskTwin
        </div>
        <div style="font-size:0.82rem; color:#94A3B8; letter-spacing:0.06em; margin-top:0.45rem; line-height:1.7;">
            Deprem risk ve proje uygunluk kararlarını daha hızlı,
            daha okunabilir ve daha güvenilir hale getiren analiz katmanı.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    PAGES = {
        "Proje Tanıtımı": "Overview",
        "Risk Analizi": "Analysis",
        "Senaryo Karşılaştırma": "Scenarios",
        "Veri ve Metodoloji": "Method",
        "Hakkında": "Context",
    }

    page = st.radio(
        "Navigasyon",
        list(PAGES.keys()),
        format_func=lambda x: f"{x}",
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div class="rt-card" style="padding:1rem 1rem 0.9rem; margin-bottom:0.9rem;">
        <div class="section-header" style="margin-bottom:0.7rem;">CANLI DEMO</div>
        <div class="metric-inline"><span class="metric-inline-label">Lokasyon</span><span class="metric-inline-value">5 İstanbul noktası</span></div>
        <div class="metric-inline"><span class="metric-inline-label">Bina girdisi</span><span class="metric-inline-value">36 demo kayıt</span></div>
        <div class="metric-inline"><span class="metric-inline-label">Çalışma modu</span><span class="metric-inline-value">Heuristic + ML-ready</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer-box" style="margin:0;">
        <p style="font-size:0.75rem;">&#9888; Ön değerlendirme aracıdır. Mühendislik kararı yerine geçmez.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Sayfa Yönlendirme ──
if page == "Proje Tanıtımı":
    from pages.home import render_home
    render_home()
elif page == "Risk Analizi":
    from pages.risk_analysis import render_risk_analysis
    render_risk_analysis(locations, hazard_df, building_df)
elif page == "Senaryo Karşılaştırma":
    from pages.scenario import render_scenario
    render_scenario(locations)
elif page == "Veri ve Metodoloji":
    from pages.methodology import render_methodology
    render_methodology()
elif page == "Hakkında":
    from pages.about import render_about
    render_about()
