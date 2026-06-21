"""
RiskTwin Global CSS ve Tema
Profesyonel beyaz/turuncu/yeşil tasarım dili.
"""

# ── Renk Paleti ──
COLORS = {
    "primary": "#1B4332",
    "primary_light": "#2D6A4F",
    "secondary": "#F28C28",
    "accent": "#40916C",
    "success": "#40916C",
    "warning": "#F28C28",
    "danger": "#E63946",
    "orange": "#F28C28",
    "bg_dark": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "bg_surface": "#F8F9FA",
    "text_primary": "#1A1A2E",
    "text_secondary": "#6B7280",
    "text_dark": "#1A1A2E",
    "border": "#E5E7EB",
    "border_light": "#F3F4F6",
}

RISK_COLORS = {
    "low": "#40916C",
    "medium": "#F28C28",
    "high": "#E63946",
}

def get_risk_color(label: str) -> str:
    mapping = {"Düşük": RISK_COLORS["low"], "Orta": RISK_COLORS["medium"], "Yüksek": RISK_COLORS["high"]}
    return mapping.get(label, RISK_COLORS["medium"])

def get_risk_bg(label: str) -> str:
    mapping = {"Düşük": "#E6F9ED", "Orta": "#FFF4E6", "Yüksek": "#FDE8E8"}
    return mapping.get(label, "#FFF4E6")


GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {
        --rt-bg: #FFFFFF;
        --rt-surface: #FFFFFF;
        --rt-surface-2: #F8F9FA;
        --rt-surface-3: #F0FFF4;
        --rt-card: #FFFFFF;
        --rt-border: #E5E7EB;
        --rt-border-strong: #F28C28;
        --rt-text: #1A1A2E;
        --rt-muted: #6B7280;
        --rt-subtle: #9CA3AF;
        --rt-blue: #F28C28;
        --rt-emerald: #40916C;
        --rt-amber: #F59E0B;
        --rt-red: #E63946;
        --rt-orange: #F28C28;
        --rt-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
        --rt-shadow-lg: 0 4px 16px rgba(0,0,0,0.08), 0 12px 32px rgba(0,0,0,0.06);
        --rt-shadow-hover: 0 8px 24px rgba(0,0,0,0.10), 0 16px 40px rgba(0,0,0,0.06);
        --rt-radius-lg: 16px;
        --rt-radius-md: 12px;
        --rt-mono: 'JetBrains Mono', monospace;
        --rt-sans: 'Inter', sans-serif;
        /* Spacing scale */
        --rt-space-xs: 0.25rem;
        --rt-space-sm: 0.5rem;
        --rt-space-md: 1rem;
        --rt-space-lg: 1.5rem;
        --rt-space-xl: 2rem;
        --rt-space-2xl: 3rem;
        /* Typography scale */
        --rt-text-xs: 0.72rem;
        --rt-text-sm: 0.8rem;
        --rt-text-base: 0.9rem;
        --rt-text-md: 1rem;
        --rt-text-lg: 1.15rem;
        --rt-text-xl: 1.4rem;
    }

    /* ══════════════════════════════════════════════
       ANA LAYOUT
       ══════════════════════════════════════════════ */

    html, body, [data-testid="stAppViewContainer"] {
        background: #F8F9FA !important;
        font-family: var(--rt-sans) !important;
    }

    /* Streamlit üst header — beyaz yap */
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background: #FFFFFF !important;
        border-bottom: 1px solid var(--rt-border) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }

    /* Deploy butonunu gizle */
    [data-testid="stHeader"] [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Streamlit başlık override */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: var(--rt-text) !important;
    }

    .main .block-container {
        background: #FFFFFF;
        max-width: 1200px;
        padding: 2rem 2.5rem 3rem;
        margin: 1rem auto;
        border-radius: var(--rt-radius-lg);
        box-shadow: var(--rt-shadow);
        border: 1px solid var(--rt-border);
    }

    /* ══════════════════════════════════════════════
       SIDEBAR GİZLE
       ══════════════════════════════════════════════ */

    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    button[data-testid="stSidebarNavCollapseButton"] {
        display: none !important;
    }

    /* ══════════════════════════════════════════════
       ÜST NAVİGASYON BARI
       ══════════════════════════════════════════════ */

    .rt-topnav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border-bottom: 2px solid var(--rt-border);
        padding: 0.75rem 0;
        margin: -1rem -1.5rem 1rem -1.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    .rt-topnav-brand {
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }
    .rt-topnav-brand__icon {
        width: 36px;
        height: 36px;
        flex-shrink: 0;
    }
    .rt-topnav-brand__logo {
        font-size: 1.65rem;
        font-weight: 800;
        color: #1B4332;
        letter-spacing: -0.02em;
        font-family: var(--rt-sans);
    }
    .rt-topnav-brand__badge {
        display: inline-flex;
        padding: 0.2rem 0.5rem;
        border-radius: 999px;
        background: rgba(242, 140, 40, 0.1);
        border: 1px solid rgba(242, 140, 40, 0.2);
        color: #D97706;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-weight: 700;
    }

    /* ── Hamburger menü (mobil) ── */
    .rt-hamburger-input {
        display: none !important;
    }
    .rt-hamburger-btn {
        display: none;
        flex-direction: column;
        justify-content: center;
        gap: 5px;
        cursor: pointer;
        padding: 8px;
        border-radius: 8px;
        transition: background 0.2s;
        z-index: 1001;
    }
    .rt-hamburger-btn:hover {
        background: var(--rt-surface-2);
    }
    .rt-hamburger-line {
        display: block;
        width: 22px;
        height: 2.5px;
        background: #1B4332;
        border-radius: 2px;
        transition: all 0.3s ease;
    }
    /* Hamburger animasyonu — X'e dönüşme */
    .rt-hamburger-input:checked ~ .rt-hamburger-btn .rt-hamburger-line:nth-child(1) {
        transform: translateY(7.5px) rotate(45deg);
    }
    .rt-hamburger-input:checked ~ .rt-hamburger-btn .rt-hamburger-line:nth-child(2) {
        opacity: 0;
    }
    .rt-hamburger-input:checked ~ .rt-hamburger-btn .rt-hamburger-line:nth-child(3) {
        transform: translateY(-7.5px) rotate(-45deg);
    }

    /* Mobil dropdown menü */
    .rt-mobile-menu {
        display: none;
        position: absolute;
        top: 100%;
        right: 0;
        left: 0;
        background: #FFFFFF;
        border-bottom: 2px solid var(--rt-border);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        z-index: 1000;
        padding: 0.5rem 0;
    }
    .rt-hamburger-input:checked ~ .rt-mobile-menu {
        display: flex;
        flex-direction: column;
    }
    .rt-mobile-menu__item {
        display: block;
        padding: 0.85rem 1.5rem;
        color: var(--rt-muted);
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 500;
        font-family: var(--rt-sans);
        border-left: 3px solid transparent;
        transition: all 0.2s ease;
    }
    .rt-mobile-menu__item:hover {
        color: var(--rt-text);
        background: var(--rt-surface-2);
        border-left-color: rgba(242, 140, 40, 0.3);
    }
    .rt-mobile-menu__item--active {
        color: #1B4332 !important;
        font-weight: 700;
        background: rgba(64, 145, 108, 0.06);
        border-left-color: #F28C28 !important;
    }

    /* Nav butonlarını menü öğesi gibi göster */
    .rt-nav-buttons .stButton > button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        color: var(--rt-muted) !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 0.85rem !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
        margin-bottom: -2px;
    }
    .rt-nav-buttons .stButton > button:hover {
        color: var(--rt-text) !important;
        border-bottom-color: rgba(242, 140, 40, 0.3) !important;
        background: transparent !important;
    }
    /* Aktif sayfa butonu — primary type */
    .rt-nav-buttons .stButton > button[kind="primary"] {
        background: transparent !important;
        color: #1B4332 !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #F28C28 !important;
    }

    /* ── Footer ── */
    .rt-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid var(--rt-border);
    }
    .rt-footer__info {
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
    }
    .rt-footer__item {
        font-size: 0.78rem;
        color: var(--rt-subtle);
    }
    .rt-footer__item strong {
        color: var(--rt-muted);
        font-weight: 600;
    }
    .rt-footer__disclaimer {
        font-size: 0.75rem;
        color: var(--rt-orange);
        font-weight: 500;
    }

    /* ══════════════════════════════════════════════
       KARTLAR
       ══════════════════════════════════════════════ */

    .rt-card {
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
        padding: 1.25rem 1.35rem;
        margin-bottom: 0.75rem;
        box-shadow: var(--rt-shadow);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .rt-card:hover {
        box-shadow: var(--rt-shadow-hover);
    }
    .rt-card--compact { padding: var(--rt-space-md) 1.15rem; }

    /* ── Score Kartları ── */
    .score-card {
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
        padding: 1.5rem 1.25rem;
        text-align: center;
        border-top: 4px solid var(--rt-emerald);
        box-shadow: var(--rt-shadow);
        transition: all 0.2s ease;
    }
    .score-card:hover {
        box-shadow: var(--rt-shadow-hover);
        transform: translateY(-2px);
    }
    .score-card.high { border-top-color: var(--rt-red); }
    .score-card.medium { border-top-color: var(--rt-orange); }
    .score-card.low { border-top-color: var(--rt-emerald); }
    .score-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--rt-muted);
        margin-bottom: 0.6rem;
        font-weight: 600;
    }
    .score-value {
        font-family: var(--rt-sans);
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 0.4rem;
        color: var(--rt-text);
    }
    .score-band {
        font-size: 0.82rem;
        color: var(--rt-muted);
        font-weight: 500;
    }

    /* ── Feature Kartları ── */
    .feature-card {
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
        padding: 1.35rem;
        height: 100%;
        transition: all 0.2s ease;
        box-shadow: var(--rt-shadow);
    }
    .feature-card:hover {
        border-color: var(--rt-orange);
        box-shadow: 0 4px 16px rgba(242,140,40,0.12);
        transform: translateY(-2px);
    }
    .feature-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #F28C28, #F59E0B);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.82rem;
        margin-bottom: 0.85rem;
        font-family: var(--rt-mono);
        box-shadow: 0 2px 8px rgba(242,140,40,0.25);
    }
    .feature-title {
        color: var(--rt-text);
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        color: var(--rt-muted);
        font-size: 0.88rem;
        line-height: 1.65;
    }

    /* ══════════════════════════════════════════════
       HERO BÖLÜMÜ — Ana Sayfa
       ══════════════════════════════════════════════ */

    .hero-section {
        display: grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap: 1.5rem;
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-lg);
        border-top: 4px solid #40916C;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--rt-shadow-lg);
    }
    .hero-main { }
    .hero-kicker {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(242, 140, 40, 0.1);
        border: 1px solid rgba(242, 140, 40, 0.25);
        color: #D97706;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #1B4332;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-bottom: 0.85rem;
    }
    .hero-subtitle {
        color: var(--rt-muted);
        font-size: 1.02rem;
        line-height: 1.75;
        max-width: 540px;
        margin-bottom: 1.5rem;
    }
    .hero-meta-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.75rem;
    }
    .hero-meta-card {
        background: var(--rt-surface-2);
        border: 1px solid var(--rt-border);
        border-radius: 10px;
        padding: 0.75rem 0.65rem;
        text-align: center;
    }
    .hero-meta-value {
        font-family: var(--rt-mono);
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--rt-orange);
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .hero-meta-label {
        font-size: 0.7rem;
        color: var(--rt-subtle);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ── Hero Side ── */
    .hero-side {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .hero-side-card {
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
        padding: 1.25rem;
        flex: 1;
    }
    .hero-side-card--signal {
        border-left: 4px solid var(--rt-emerald);
        background: linear-gradient(135deg, #F0FFF4 0%, #FFFFFF 40%);
    }
    .hero-side-card--command {
        border-left: 4px solid var(--rt-orange);
        background: linear-gradient(135deg, #FFF7ED 0%, #FFFFFF 40%);
    }
    .hero-side-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--rt-subtle);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .hero-side-value {
        color: var(--rt-text);
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.4rem;
    }
    .hero-side-desc {
        color: var(--rt-muted);
        font-size: 0.86rem;
        line-height: 1.7;
    }
    .hero-signal-list {
        margin-top: 0.85rem;
        display: grid;
        gap: 0.5rem;
    }
    .hero-signal-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.45rem 0;
        border-bottom: 1px solid var(--rt-border);
    }
    .hero-signal-item:last-child { border-bottom: none; }
    .hero-signal-item__label {
        font-size: 0.78rem;
        color: var(--rt-subtle);
        font-weight: 500;
    }
    .hero-signal-item__value {
        font-size: 0.82rem;
        color: var(--rt-text);
        font-weight: 600;
    }

    /* ── Signal Strip ── */
    .signal-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.25rem 0;
    }
    .signal-strip__item {
        background: #F0FFF4;
        border: 1px solid rgba(64,145,108,0.15);
        border-radius: var(--rt-radius-md);
        padding: 1.15rem;
    }
    .signal-strip__label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--rt-subtle);
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .signal-strip__value {
        color: var(--rt-emerald);
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
    }
    .signal-strip__desc {
        color: var(--rt-muted);
        font-size: 0.82rem;
        line-height: 1.65;
    }

    /* ══════════════════════════════════════════════
       SAYFA HERO (iç sayfalar)
       ══════════════════════════════════════════════ */

    .page-hero {
        background: linear-gradient(135deg, #F0FFF4 0%, #FFFFFF 50%);
        border: 1px solid var(--rt-border);
        border-left: 4px solid var(--rt-orange);
        border-radius: 0 var(--rt-radius-lg) var(--rt-radius-lg) 0;
        padding: 2rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--rt-shadow);
    }
    .page-hero__main { }
    .page-kicker {
        display: inline-flex;
        align-items: center;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        background: rgba(242, 140, 40, 0.1);
        border: 1px solid rgba(242, 140, 40, 0.25);
        color: #D97706;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 700;
        margin-bottom: 0.85rem;
    }
    .page-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #1B4332 !important;
        letter-spacing: -0.02em;
        margin: 0 0 0.65rem !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    .page-summary {
        color: var(--rt-muted);
        font-size: 0.95rem;
        line-height: 1.7;
        max-width: 540px;
        margin: 0;
    }
    .page-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin-top: 1rem;
    }
    .page-tag {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        background: rgba(64, 145, 108, 0.08);
        border: 1px solid rgba(64, 145, 108, 0.18);
        color: #2D6A4F;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }
    .page-hero__side {
        display: flex;
        flex-direction: column;
        gap: 0.85rem;
    }
    .page-hero__card {
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-left: 3px solid var(--rt-orange);
        border-radius: 0 var(--rt-radius-md) var(--rt-radius-md) 0;
        padding: 1.1rem 1rem;
        flex: 1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }
    .page-hero__card-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--rt-orange);
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .page-hero__card-value {
        color: var(--rt-text);
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    .page-hero__card-desc {
        color: var(--rt-muted);
        font-size: 0.82rem;
        line-height: 1.6;
    }

    /* ══════════════════════════════════════════════
       SUMMARY ve METRİK
       ══════════════════════════════════════════════ */

    .summary-eyebrow {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--rt-subtle);
        margin-bottom: 0.4rem;
        font-weight: 600;
    }
    .summary-card {
        text-align: center;
        padding: 1rem 0.75rem;
    }
    .summary-value {
        color: var(--rt-text);
        font-family: var(--rt-sans);
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.45rem;
    }
    .summary-caption {
        color: var(--rt-muted);
        font-size: 0.84rem;
        line-height: 1.55;
    }

    /* ── Status Chip ── */
    .status-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border: 1px solid rgba(242, 140, 40, 0.2);
        background: rgba(242, 140, 40, 0.08);
        color: #D97706;
    }
    .status-chip--blue {
        background: rgba(242, 140, 40, 0.1);
        border-color: rgba(242, 140, 40, 0.25);
        color: #D97706;
    }
    .status-chip--green {
        background: rgba(64, 145, 108, 0.1);
        border-color: rgba(64, 145, 108, 0.2);
        color: #2D6A4F;
    }
    .status-chip--amber {
        background: rgba(245, 158, 11, 0.1);
        border-color: rgba(245, 158, 11, 0.2);
        color: #B45309;
    }
    .status-chip--positive {
        background: rgba(64, 145, 108, 0.1);
        border-color: rgba(64, 145, 108, 0.2);
        color: #2D6A4F;
    }
    .status-chip--warning {
        background: rgba(245, 158, 11, 0.1);
        border-color: rgba(245, 158, 11, 0.2);
        color: #B45309;
    }

    /* ── Rich Text Card ── */
    .rich-text-card p {
        color: var(--rt-text);
        font-size: 0.91rem;
        line-height: 1.75;
        margin: 0 0 0.85rem;
    }
    .rich-text-card p:last-child { margin-bottom: 0; }
    .rich-text-card strong {
        color: var(--rt-text);
        font-weight: 700;
    }
    .rich-text-list {
        margin: 0.35rem 0 0.9rem;
        padding-left: 1.15rem;
    }
    .rich-text-list li {
        color: var(--rt-text);
        font-size: 0.9rem;
        line-height: 1.75;
        margin-bottom: 0.45rem;
    }
    .note-inline {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        margin-top: 0.75rem;
        padding: 0.38rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(242, 140, 40, 0.25);
        background: rgba(242, 140, 40, 0.08);
        color: #D97706;
        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    /* ── Adım Akışı ── */
    .step-card {
        text-align: left;
        height: 100%;
    }
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 12px;
        background: linear-gradient(135deg, #F28C28, #40916C);
        color: white;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 8px rgba(242,140,40,0.2);
    }

    /* ── Veri Kaynak Badge'leri ── */
    .source-badge {
        display: inline-block;
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        color: var(--rt-muted);
        margin: 0.25rem;
    }
    .source-badge.active {
        border-color: var(--rt-emerald);
        color: var(--rt-emerald);
    }
    .source-badge.optional {
        border-color: var(--rt-orange);
        color: var(--rt-orange);
    }

    /* ── Disclaimer Kutusu ── */
    .disclaimer-box {
        background: #FFF7ED;
        border: 1px solid rgba(242, 140, 40, 0.2);
        border-left: 4px solid var(--rt-orange);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1.5rem 0;
    }
    .disclaimer-box p {
        color: #92400E !important;
        font-size: 0.85rem;
        margin: 0;
    }

    /* ── Tablo ── */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* ── Divider ── */
    hr { border-color: var(--rt-border) !important; }

    /* ── Senaryo Delta ── */
    .delta-positive { color: var(--rt-emerald); font-weight: 700; }
    .delta-negative { color: var(--rt-red); font-weight: 700; }

    /* ── Nav Item ── */
    .nav-item {
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.25rem;
        cursor: pointer;
        transition: all 0.2s;
        color: var(--rt-text);
    }
    .nav-item:hover { background: rgba(242, 140, 40, 0.06); }
    .nav-item.active {
        background: rgba(242, 140, 40, 0.1);
        border-left: 3px solid var(--rt-orange);
        color: #D97706;
        font-weight: 600;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--rt-surface-2) !important;
        border-radius: 8px !important;
    }

    /* ── Section Header ── */
    .section-header {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #1B4332;
        font-weight: 700;
        margin-bottom: 1.25rem;
        padding-bottom: 0.6rem;
        padding-left: 0.75rem;
        border-left: 3px solid var(--rt-emerald);
        border-bottom: 1px solid var(--rt-border);
    }

    /* ── Metric inline ── */
    .metric-inline {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 0.7rem 0;
        border-bottom: 1px solid var(--rt-border);
    }
    .metric-inline:last-child { border-bottom: none; }
    .metric-inline-label { color: var(--rt-muted); font-size: 0.85rem; }
    .metric-inline-value { color: var(--rt-text); font-weight: 600; }

    /* ── Faz Kartları ── */
    .phase-card {
        background: #FFFFFF;
        border: 1px solid var(--rt-border);
        border-left: 4px solid var(--rt-orange);
        border-radius: 0 var(--rt-radius-md) var(--rt-radius-md) 0;
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .phase-card:hover {
        box-shadow: var(--rt-shadow);
    }
    .phase-card.active {
        border-left-color: var(--rt-emerald);
        background: #F0FFF4;
    }
    .phase-card.future {
        border-left-color: #D1D5DB;
        opacity: 0.6;
    }

    /* ── Phase Card İç Elemanları ── */
    .phase-card__label {
        font-weight: 700;
        font-size: var(--rt-text-sm);
        letter-spacing: 0.05em;
    }
    .phase-card__label--active { color: var(--rt-emerald); }
    .phase-card__label--current { color: var(--rt-orange); }
    .phase-card__label--future { color: var(--rt-subtle); }
    .phase-card__title {
        color: var(--rt-text);
        font-weight: 600;
        margin: 0.3rem 0;
    }
    .phase-card__desc {
        color: var(--rt-muted);
        font-size: var(--rt-text-base);
    }

    /* ── Architecture Panel ── */
    .architecture-panel {
        display: grid;
        gap: 0.85rem;
    }
    .architecture-row {
        display: grid;
        grid-template-columns: 180px 1fr;
        gap: 1rem;
        padding: 0.9rem 1rem;
        background: var(--rt-surface-2);
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
    }
    .architecture-label {
        color: var(--rt-orange);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .architecture-text {
        color: var(--rt-text);
        font-size: 0.9rem;
        line-height: 1.65;
    }

    /* ══════════════════════════════════════════════
       GRID SİSTEMİ
       ══════════════════════════════════════════════ */

    .rt-grid-4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--rt-space-md); }
    .rt-grid-3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--rt-space-md); }
    .rt-grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--rt-space-md); }

    /* ── Spacer ── */
    .rt-spacer-sm { height: var(--rt-space-sm); }
    .rt-spacer-md { height: var(--rt-space-md); }
    .rt-spacer-lg { height: var(--rt-space-xl); }

    /* ── Accent Text ── */
    .rt-accent-text { color: var(--rt-text); font-weight: 600; }
    .rt-accent-text--blue { color: var(--rt-orange); }
    .rt-accent-text--emerald { color: var(--rt-emerald); }
    .rt-accent-text--amber { color: var(--rt-amber); }
    .rt-accent-text--red { color: var(--rt-red); }

    /* ── Stat Card Renk Varyantları ── */
    .stat-card-value--blue { color: var(--rt-orange); }
    .stat-card-value--emerald { color: var(--rt-emerald); }
    .stat-card-value--amber { color: var(--rt-amber); }
    .stat-card-value--orange { color: var(--rt-orange); }

    /* ── Flex Bar ── */
    .rt-flex-bar {
        display: flex;
        justify-content: space-between;
        gap: var(--rt-space-md);
        flex-wrap: wrap;
    }

    /* ── Location Badge ── */
    .rt-location-badge {
        background: var(--rt-surface-2);
        border: 1px solid var(--rt-border);
        border-radius: 10px;
        padding: 0.6rem 0.85rem;
        margin-bottom: var(--rt-space-md);
        display: flex;
        align-items: center;
    }
    .rt-location-badge__icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: linear-gradient(135deg, #F28C28, #F59E0B);
        color: #FFFFFF;
        font-family: var(--rt-mono);
        font-size: var(--rt-text-xs);
        font-weight: 700;
        margin-right: 0.55rem;
        flex-shrink: 0;
    }
    .rt-location-badge__text {
        color: var(--rt-text);
        font-size: var(--rt-text-base);
        font-weight: 500;
    }
    .rt-location-badge__coords {
        color: var(--rt-subtle);
        font-size: 0.75rem;
        margin-left: var(--rt-space-sm);
    }

    /* ── Data Cell ── */
    .rt-data-cell {
        text-align: center;
        padding: var(--rt-space-md);
    }
    .rt-data-cell__label {
        font-weight: 600;
        font-size: var(--rt-text-sm);
    }
    .rt-data-cell__label--active { color: var(--rt-emerald); }
    .rt-data-cell__label--pending { color: var(--rt-amber); }
    .rt-data-cell__caption {
        color: var(--rt-subtle);
        font-size: 0.75rem;
        margin-top: var(--rt-space-xs);
    }

    /* ══════════════════════════════════════════════
       EDITORIAL GRID
       ══════════════════════════════════════════════ */

    .editorial-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
        gap: 1rem;
    }
    .editorial-card {
        border-radius: var(--rt-radius-md);
        padding: 1.35rem 1.3rem;
        border: 1px solid var(--rt-border);
        background: #FFFFFF;
        box-shadow: var(--rt-shadow);
    }
    .editorial-card--accent {
        border-top: 3px solid var(--rt-orange);
    }
    .editorial-title,
    h3.editorial-title {
        color: var(--rt-text) !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        margin: 0 0 0.8rem !important;
    }
    .editorial-text {
        color: var(--rt-muted);
        font-size: 0.92rem;
        line-height: 1.8;
        margin: 0;
    }
    .editorial-list {
        display: grid;
        gap: 0.8rem;
        margin-top: 1rem;
    }
    .editorial-item {
        display: flex;
        gap: 0.8rem;
        align-items: flex-start;
        padding-top: 0.8rem;
        border-top: 1px solid var(--rt-border);
    }
    .editorial-item:first-child {
        padding-top: 0;
        border-top: 0;
    }
    .editorial-item__code {
        flex-shrink: 0;
        min-width: 42px;
        height: 42px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: linear-gradient(135deg, #F28C28, #40916C);
        color: #FFFFFF;
        font-family: var(--rt-mono);
        font-size: 0.74rem;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(242,140,40,0.2);
    }
    .editorial-item__title {
        color: var(--rt-text);
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .editorial-item__desc {
        color: var(--rt-muted);
        font-size: 0.84rem;
        line-height: 1.7;
    }

    /* ══════════════════════════════════════════════
       INSIGHT GRID
       ══════════════════════════════════════════════ */

    .insight-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    .insight-item {
        background: var(--rt-surface-2);
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
        padding: 1.1rem;
    }
    .insight-item-head {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin-bottom: 0.55rem;
    }
    .insight-item-code {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 8px;
        background: #1B4332;
        color: #FFFFFF;
        font-family: var(--rt-mono);
        font-size: 0.7rem;
        font-weight: 700;
    }
    .insight-item-title {
        color: var(--rt-text);
        font-weight: 600;
        font-size: 0.95rem;
    }
    .insight-item-text {
        color: var(--rt-muted);
        font-size: 0.86rem;
        line-height: 1.7;
    }

    /* ══════════════════════════════════════════════
       SENARYO BÖLÜMÜ
       ══════════════════════════════════════════════ */

    .rt-scenario-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .rt-scenario-row__info {
        flex: 1;
        min-width: 200px;
    }
    .rt-scenario-row__title {
        color: var(--rt-text);
        font-weight: 600;
        font-size: 0.95rem;
    }
    .rt-scenario-row__preview {
        color: var(--rt-muted);
        font-size: var(--rt-text-sm);
        margin-top: var(--rt-space-xs);
    }
    .rt-scenario-metrics {
        display: flex;
        gap: var(--rt-space-xl);
        align-items: center;
        margin-top: var(--rt-space-sm);
    }
    .rt-scenario-metrics__item {
        text-align: center;
    }
    .rt-scenario-metrics__label {
        color: var(--rt-subtle);
        font-size: 0.7rem;
        text-transform: uppercase;
    }
    .rt-scenario-metrics__value {
        color: var(--rt-text);
        font-weight: 700;
    }
    .rt-scenario-metrics__delta {
        font-weight: 800;
        font-size: 1.2rem;
    }
    .rt-scenario-footer {
        margin-top: 0.9rem;
        padding-top: 0.9rem;
        border-top: 1px solid var(--rt-border);
        display: flex;
        justify-content: space-between;
        gap: var(--rt-space-md);
        flex-wrap: wrap;
    }

    /* ── Code Block ── */
    .rt-code-block {
        background: var(--rt-surface-2);
        border: 1px solid var(--rt-border);
        border-radius: 8px;
        padding: var(--rt-space-md);
        font-family: var(--rt-mono);
        color: #1B4332;
        font-size: var(--rt-text-base);
        line-height: 1.8;
    }

    /* ── Weight Cell ── */
    .rt-weight-cell {
        background: var(--rt-surface-2);
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-md);
        padding: 0.9rem;
    }

    /* ── Risk Band Display ── */
    .rt-risk-band-display {
        display: flex;
        gap: var(--rt-space-sm);
        margin-bottom: var(--rt-space-md);
    }
    .rt-risk-band-item {
        flex: 1;
        border-radius: 8px;
        padding: var(--rt-space-sm) var(--rt-space-md);
        text-align: center;
    }
    .rt-risk-band-item--low { background: #E6F9ED; }
    .rt-risk-band-item--low .rt-risk-band-item__value { color: var(--rt-emerald); font-weight: 700; }
    .rt-risk-band-item--medium { background: #FFF4E6; }
    .rt-risk-band-item--medium .rt-risk-band-item__value { color: var(--rt-orange); font-weight: 700; }
    .rt-risk-band-item--high { background: #FDE8E8; }
    .rt-risk-band-item--high .rt-risk-band-item__value { color: var(--rt-red); font-weight: 700; }
    .rt-risk-band-item__label {
        color: var(--rt-muted);
        font-size: 0.75rem;
    }

    /* ── Scenario Item (about.py) ── */
    .rt-scenario-item {
        margin-bottom: var(--rt-space-md);
    }
    .rt-scenario-item:last-child { margin-bottom: 0; }
    .rt-scenario-item__title {
        color: var(--rt-emerald);
        font-weight: 600;
    }
    .rt-scenario-item__text {
        color: var(--rt-muted);
        font-size: var(--rt-text-base);
        line-height: 1.6;
        margin-top: 0.3rem;
    }

    /* ── Feature Highlight ── */
    .rt-feature-highlight {
        color: var(--rt-emerald);
        font-weight: 700;
        margin-bottom: var(--rt-space-sm);
        font-size: 1rem;
    }
    .rt-feature-highlight__desc {
        color: var(--rt-muted);
        font-size: var(--rt-text-base);
        line-height: 1.65;
    }

    /* ── Card Footer ── */
    .rt-card__footer {
        color: var(--rt-subtle);
        font-size: var(--rt-text-sm);
        margin-top: 0.75rem;
        border-top: 1px solid var(--rt-border);
        padding-top: var(--rt-space-sm);
    }

    /* ── ML Status ── */
    .rt-ml-status {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .rt-ml-badge {
        border-radius: 6px;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .rt-ml-badge--trained { background: #E6F9ED; color: var(--rt-emerald); }
    .rt-ml-badge--untrained { background: #FFF4E6; color: var(--rt-orange); }

    /* ══════════════════════════════════════════════
       STREAMLIT WIDGET OVERRIDES
       ══════════════════════════════════════════════ */

    /* Butonlar */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #F28C28, #E07B1E) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.5rem !important;
        box-shadow: 0 2px 8px rgba(242,140,40,0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 16px rgba(242,140,40,0.4) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button {
        border-radius: 10px !important;
        border-color: var(--rt-border) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    /* Slider */
    .stSlider > div > div > div > div {
        background: var(--rt-emerald) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border-color: var(--rt-border) !important;
    }

    /* Toggle */
    .stCheckbox label span[data-checked="true"] {
        background-color: var(--rt-emerald) !important;
    }

    /* ══════════════════════════════════════════════
       RESPONSIVE
       ══════════════════════════════════════════════ */

    @media (max-width: 1200px) {
        .hero-section,
        .page-hero,
        .editorial-grid {
            grid-template-columns: 1fr;
        }
        .hero-meta-grid,
        .rt-grid-4 {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        .architecture-row {
            grid-template-columns: 1fr;
        }
        .insight-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 768px) {
        /* Hamburger menüyü göster, desktop navı gizle */
        .rt-hamburger-btn {
            display: flex !important;
        }
        .rt-nav-desktop {
            display: none !important;
        }
        /* Topnav relative yaparak dropdown pozisyonlama */
        .rt-topnav {
            position: relative;
        }
        .rt-topnav-brand__badge {
            display: none;
        }
        .rt-topnav-brand__logo {
            font-size: 1.3rem;
        }
        .rt-topnav-brand__icon {
            width: 28px;
            height: 28px;
        }

        .main .block-container {
            padding: 1rem 0.75rem 2rem;
            margin: 0.25rem;
            border-radius: var(--rt-radius-md);
        }
        .hero-section {
            padding: 1.5rem 1.25rem;
        }
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 0.9rem;
        }
        .hero-side {
            display: none;
        }
        .hero-meta-grid,
        .rt-grid-4,
        .rt-grid-3 {
            grid-template-columns: repeat(2, 1fr);
        }
        .signal-strip {
            grid-template-columns: 1fr;
        }
        .page-hero {
            padding: 1.25rem 1rem;
        }
        .page-title {
            font-size: 1.6rem !important;
        }
        .page-summary {
            font-size: 0.85rem;
        }
        .summary-value {
            font-size: 1.4rem;
        }
        .editorial-grid {
            grid-template-columns: 1fr;
        }
        .editorial-title {
            font-size: 1rem !important;
        }
        .rt-scenario-metrics {
            gap: var(--rt-space-md);
        }
        .section-header {
            font-size: 0.65rem;
        }
        .rt-card {
            padding: var(--rt-space-md);
        }
        .feature-card {
            padding: var(--rt-space-md);
        }
        .architecture-row {
            grid-template-columns: 1fr;
        }
        /* Footer */
        .rt-footer {
            flex-direction: column;
            text-align: center;
            gap: 0.5rem;
        }
        .rt-footer__info {
            flex-direction: column;
            gap: 0.25rem;
        }
    }

    @media (max-width: 480px) {
        .hero-title { font-size: 1.7rem; }
        .hero-section { padding: 1rem 0.75rem; }
        .hero-meta-grid { grid-template-columns: 1fr; }
        .page-title { font-size: 1.4rem !important; }
        .rt-grid-4, .rt-grid-3, .rt-grid-2 { grid-template-columns: 1fr; }
        .score-value { font-size: 1.8rem; }
        .rt-risk-band-display { flex-direction: column; }
        .rt-location-badge { flex-wrap: wrap; }
        .rt-topnav {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
        }
    }
</style>
"""
