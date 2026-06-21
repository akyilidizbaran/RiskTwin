"""
RiskTwin - Deprem Risk Değerlendirme ve Karar Destek Sistemi
Ana Streamlit Uygulaması (Çok Sayfalı)
"""
import sys
import os
import base64

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
    initial_sidebar_state="collapsed",
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

# ── Session State ──
if "page" not in st.session_state:
    st.session_state.page = "Proje Tanıtımı"

PAGES = ["Proje Tanıtımı", "Risk Analizi", "Senaryo Karşılaştırma", "Metodoloji", "Hakkında"]

# ── Query param ile sayfa geçişi (mobil hamburger menüden) ──
_qp = st.query_params.get("page", None)
if _qp and _qp in PAGES and st.session_state.page != _qp:
    st.session_state.page = _qp

# ── Logo yükle ──
_logo_path = os.path.join(APP_DIR, "static", "logo.svg")
with open(_logo_path, "r") as _f:
    _logo_svg = _f.read()
_logo_b64 = base64.b64encode(_logo_svg.encode()).decode()

# ── Hamburger menü linkleri ──
_active = st.session_state.page
_menu_items = ""
for _idx, _p in enumerate(PAGES):
    _cls = "rt-mobile-menu__item--active" if _p == _active else ""
    _href = f"?page={_p.replace(' ', '+')}"
    _delay = f'style="transition-delay: {0.06 * (_idx + 1):.2f}s"'
    _menu_items += f'<a href="{_href}" class="rt-mobile-menu__item {_cls}" {_delay}>{_p}</a>\n'

# ── Üst Navigasyon Barı ──
st.markdown(f"""
<div class="rt-topnav">
    <div class="rt-topnav-brand">
        <img src="data:image/svg+xml;base64,{_logo_b64}" class="rt-topnav-brand__icon" alt="RiskTwin" />
        <span class="rt-topnav-brand__logo">RiskTwin</span>
        <span class="rt-topnav-brand__badge">Risk Intelligence</span>
    </div>
    <input type="checkbox" id="rt-hamburger-toggle" class="rt-hamburger-input" />
    <label for="rt-hamburger-toggle" class="rt-hamburger-btn" aria-label="Menüyü aç/kapat">
        <span class="rt-hamburger-line"></span>
        <span class="rt-hamburger-line"></span>
        <span class="rt-hamburger-line"></span>
    </label>
    <div class="rt-mobile-menu">
        <label for="rt-hamburger-toggle" class="rt-mobile-menu__overlay" aria-label="Menüyü kapat"></label>
        <nav class="rt-mobile-menu__nav">
            <div class="rt-mobile-menu__header">
                <img src="data:image/svg+xml;base64,{_logo_b64}" class="rt-mobile-menu__logo-icon" alt="" />
                <span class="rt-mobile-menu__logo-text">RiskTwin</span>
            </div>
            {_menu_items}
            <div class="rt-mobile-menu__footer">
                <span>Deprem Risk Karar Destek Sistemi</span>
            </div>
        </nav>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Desktop nav butonları ──
with st.container():
    st.markdown('<div class="rt-nav-desktop"><div class="rt-nav-buttons">', unsafe_allow_html=True)
    nav_cols = st.columns(len(PAGES))
    for col, page_name in zip(nav_cols, PAGES):
        with col:
            is_active = st.session_state.page == page_name
            if st.button(
                page_name,
                key=f"nav_{page_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state.page = page_name
                st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ── Sayfa Yönlendirme ──
active = st.session_state.page

if active == "Proje Tanıtımı":
    from pages.home import render_home
    render_home()
elif active == "Risk Analizi":
    from pages.risk_analysis import render_risk_analysis
    render_risk_analysis(locations, hazard_df, building_df)
elif active == "Senaryo Karşılaştırma":
    from pages.scenario import render_scenario
    render_scenario(locations)
elif active == "Metodoloji":
    from pages.methodology import render_methodology
    render_methodology()
elif active == "Hakkında":
    from pages.about import render_about
    render_about()

# ── Footer ──
st.markdown("""
<div class="rt-footer">
    <div class="rt-footer__info">
        <span class="rt-footer__item"><strong>Lokasyon:</strong> 5 İstanbul noktası</span>
        <span class="rt-footer__item"><strong>Veri:</strong> 36 demo kayıt</span>
        <span class="rt-footer__item"><strong>Motor:</strong> Heuristic + ML-ready</span>
    </div>
    <span class="rt-footer__disclaimer">⚠ Ön değerlendirme aracıdır. Mühendislik kararı yerine geçmez.</span>
</div>
""", unsafe_allow_html=True)
