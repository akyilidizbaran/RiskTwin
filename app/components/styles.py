"""
RiskTwin Global CSS ve Tema
Profesyonel, kurumsal PropTech / decision support görsel dili.
"""

# ── Renk Paleti ──
COLORS = {
    "primary": "#0F172A",
    "primary_light": "#172033",
    "secondary": "#38BDF8",
    "accent": "#22C55E",
    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "bg_dark": "#020617",
    "bg_card": "#0E1223",
    "bg_surface": "#F8FAFC",
    "text_primary": "#F8FAFC",
    "text_secondary": "#94A3B8",
    "text_dark": "#1E293B",
    "border": "#334155",
    "border_light": "#E2E8F0",
}

RISK_COLORS = {
    "low": "#10B981",
    "medium": "#F59E0B",
    "high": "#EF4444",
}

def get_risk_color(label: str) -> str:
    mapping = {"Düşük": RISK_COLORS["low"], "Orta": RISK_COLORS["medium"], "Yüksek": RISK_COLORS["high"]}
    return mapping.get(label, RISK_COLORS["medium"])

def get_risk_bg(label: str) -> str:
    mapping = {"Düşük": "#065F46", "Orta": "#78350F", "Yüksek": "#7F1D1D"}
    return mapping.get(label, "#78350F")


GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {
        --rt-bg: #020617;
        --rt-surface: #0B1120;
        --rt-surface-2: #0E172A;
        --rt-card: linear-gradient(180deg, rgba(15, 23, 42, 0.92) 0%, rgba(10, 15, 27, 0.96) 100%);
        --rt-border: rgba(148, 163, 184, 0.14);
        --rt-border-strong: rgba(56, 189, 248, 0.28);
        --rt-text: #E2E8F0;
        --rt-muted: #94A3B8;
        --rt-subtle: #64748B;
        --rt-blue: #38BDF8;
        --rt-emerald: #22C55E;
        --rt-amber: #F59E0B;
        --rt-red: #EF4444;
        --rt-shadow: 0 18px 60px rgba(2, 6, 23, 0.42);
        --rt-radius-lg: 22px;
        --rt-radius-md: 16px;
        --rt-mono: 'JetBrains Mono', monospace;
        --rt-sans: 'IBM Plex Sans', sans-serif;
    }

    /* ── Temel Sayfa ── */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(56, 189, 248, 0.18) 0%, rgba(2, 6, 23, 0) 28%),
            radial-gradient(circle at top right, rgba(34, 197, 94, 0.12) 0%, rgba(2, 6, 23, 0) 22%),
            linear-gradient(180deg, #020617 0%, #08111f 48%, #020617 100%);
        color: var(--rt-text);
        font-family: var(--rt-sans);
    }

    .main .block-container {
        max-width: 1320px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(10, 15, 27, 0.98) 100%);
        border-right: 1px solid var(--rt-border);
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        display: none;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label {
        color: var(--rt-text) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }

    /* ── Başlıklar ── */
    h1, h2, h3 { color: #F8FAFC !important; }
    h1, h2 {
        font-family: var(--rt-mono);
        letter-spacing: -0.04em;
    }
    h1 { font-weight: 700 !important; }
    h2 { font-weight: 600 !important; }
    p, li, span { color: #CBD5E1; }

    /* ── Streamlit kontrol katmanı ── */
    [data-testid="stToolbar"] {
        right: 1rem;
        top: 0.6rem;
    }
    [data-testid="stHeader"] {
        background: rgba(2, 6, 23, 0.72);
        backdrop-filter: blur(10px);
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    [data-testid="stSlider"] > div,
    .stTextInput > div > div,
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.82) !important;
        border: 1px solid var(--rt-border) !important;
        border-radius: 14px !important;
        box-shadow: none !important;
    }
    .stSelectbox label,
    .stSlider label,
    .stToggle label,
    .stTextInput label {
        color: var(--rt-muted) !important;
        font-size: 0.82rem !important;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    div[data-baseweb="select"] input,
    div[data-baseweb="input"] input {
        color: var(--rt-text) !important;
        font-family: var(--rt-sans) !important;
    }
    .stButton > button {
        border-radius: 999px;
        border: 1px solid rgba(56, 189, 248, 0.28);
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.16), rgba(34, 197, 94, 0.12));
        color: #F8FAFC;
        font-weight: 600;
        padding: 0.72rem 1.1rem;
        transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(56, 189, 248, 0.46);
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.22), rgba(34, 197, 94, 0.16));
    }
    .stExpander {
        border: 1px solid var(--rt-border) !important;
        border-radius: var(--rt-radius-md) !important;
        background: rgba(10, 15, 27, 0.72) !important;
    }
    iframe {
        border-radius: 18px !important;
        overflow: hidden !important;
    }

    /* ── Radio navigasyon ── */
    div[role="radiogroup"] > label {
        background: rgba(148, 163, 184, 0.05);
        border: 1px solid transparent;
        border-radius: 14px;
        margin-bottom: 0.45rem;
        padding: 0.35rem 0.5rem 0.35rem 0.2rem;
        transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
    }
    div[role="radiogroup"] > label:hover {
        background: rgba(56, 189, 248, 0.08);
        border-color: rgba(56, 189, 248, 0.14);
        transform: translateX(2px);
    }
    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.16), rgba(34, 197, 94, 0.08));
        border-color: rgba(56, 189, 248, 0.3);
    }
    div[role="radiogroup"] > label p {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #E2E8F0 !important;
    }
    div[role="radiogroup"] > label[data-checked="true"] p {
        color: #F8FAFC !important;
    }

    /* ── Kart Sistemi ── */
    .rt-card {
        background: var(--rt-card);
        border: 1px solid var(--rt-border);
        border-radius: var(--rt-radius-lg);
        padding: 1.35rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: var(--rt-shadow);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .rt-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.22);
        box-shadow: 0 20px 60px rgba(2, 6, 23, 0.5);
    }
    .rt-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(34, 197, 94, 0));
        pointer-events: none;
    }

    /* ── Skor Kartları ── */
    .score-card {
        border-radius: 22px;
        padding: 1.45rem 1.1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: var(--rt-shadow);
    }
    .score-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
    }
    .score-card.low { background: linear-gradient(145deg, rgba(6, 95, 70, 0.82) 0%, rgba(5, 46, 36, 0.96) 100%); }
    .score-card.low::before { background: #10B981; }
    .score-card.medium { background: linear-gradient(145deg, rgba(120, 53, 15, 0.82) 0%, rgba(69, 26, 3, 0.96) 100%); }
    .score-card.medium::before { background: #F59E0B; }
    .score-card.high { background: linear-gradient(145deg, rgba(127, 29, 29, 0.82) 0%, rgba(69, 10, 10, 0.96) 100%); }
    .score-card.high::before { background: #EF4444; }

    .score-value {
        font-size: 2.75rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
        margin: 0.5rem 0;
        font-family: var(--rt-mono);
    }
    .score-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(255,255,255,0.68);
        margin-bottom: 0.25rem;
    }
    .score-band {
        font-size: 0.9rem;
        font-weight: 600;
        color: #E2E8F0;
    }

    /* ── Hero ── */
    .hero-section {
        text-align: left;
        padding: 2.8rem 2.4rem 2.2rem;
        margin-bottom: 1.4rem;
        border: 1px solid var(--rt-border);
        border-radius: 30px;
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at top right, rgba(34, 197, 94, 0.16) 0%, rgba(15, 23, 42, 0) 24%),
            radial-gradient(circle at left center, rgba(56, 189, 248, 0.16) 0%, rgba(15, 23, 42, 0) 32%),
            linear-gradient(135deg, rgba(15, 23, 42, 0.96) 0%, rgba(8, 15, 28, 0.98) 100%);
        box-shadow: 0 30px 80px rgba(2, 6, 23, 0.4);
    }
    .hero-title {
        font-size: 3.8rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.75rem;
        line-height: 1.02;
        max-width: 10ch;
        font-family: var(--rt-mono);
    }
    .hero-subtitle {
        font-size: 1.06rem;
        color: #A9B5C9;
        max-width: 760px;
        margin: 0 0 1.6rem;
        line-height: 1.72;
    }
    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.2);
        color: #8AD4FF;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.72rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .hero-meta-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 1.5rem;
    }
    .hero-meta-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 18px;
        padding: 1rem 1.05rem;
    }
    .hero-meta-value {
        color: #F8FAFC;
        font-size: 1.4rem;
        font-weight: 700;
        font-family: var(--rt-mono);
    }
    .hero-meta-label {
        color: var(--rt-muted);
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 0.35rem;
    }

    /* ── Sayfa başlık sistemi ── */
    .page-hero {
        padding: 1.55rem 1.6rem;
        border: 1px solid var(--rt-border);
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.82) 0%, rgba(8, 15, 28, 0.95) 100%);
        border-radius: 24px;
        margin-bottom: 1.45rem;
        position: relative;
        overflow: hidden;
    }
    .page-kicker {
        color: #8AD4FF;
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
        font-weight: 600;
    }
    .page-title {
        font-size: 2.3rem;
        line-height: 1.05;
        margin: 0;
        font-family: var(--rt-mono);
        color: #F8FAFC;
    }
    .page-summary {
        color: #A9B5C9;
        margin-top: 0.7rem;
        max-width: 70ch;
        line-height: 1.7;
        font-size: 0.98rem;
    }
    .page-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
        margin-top: 1rem;
    }
    .page-tag {
        display: inline-flex;
        align-items: center;
        padding: 0.42rem 0.72rem;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        font-size: 0.8rem;
    }

    .stat-card {
        text-align: center;
        padding: 1.1rem 0.75rem;
    }
    .stat-card-value {
        font-family: var(--rt-mono);
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-card-label {
        font-size: 0.78rem;
        color: var(--rt-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ── Feature Kartları ── */
    .feature-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.78) 0%, rgba(11, 17, 32, 0.94) 100%);
        border: 1px solid var(--rt-border);
        border-radius: 20px;
        padding: 1.35rem 1.25rem;
        text-align: left;
        height: 100%;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .feature-card:hover {
        border-color: rgba(56, 189, 248, 0.22);
        transform: translateY(-2px);
    }
    .feature-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 48px;
        height: 48px;
        padding: 0 0.9rem;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.18), rgba(34, 197, 94, 0.1));
        border: 1px solid rgba(56, 189, 248, 0.2);
        color: #C8EEFF;
        font-family: var(--rt-mono);
        font-size: 0.86rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.89rem;
        color: #A8B3C6;
        line-height: 1.68;
    }

    .insight-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
    }
    .insight-item {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 20px;
        padding: 1.15rem 1.2rem;
    }
    .insight-item-head {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.75rem;
    }
    .insight-item-code {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(34, 197, 94, 0.1));
        border: 1px solid rgba(56, 189, 248, 0.18);
        color: #C8EEFF;
        font-family: var(--rt-mono);
        font-size: 0.78rem;
        font-weight: 700;
    }
    .insight-item-title {
        color: #F8FAFC;
        font-size: 0.98rem;
        font-weight: 700;
    }
    .insight-item-text {
        color: #A8B3C6;
        font-size: 0.88rem;
        line-height: 1.72;
    }

    .summary-card {
        height: 100%;
        text-align: center;
        padding: 1.2rem 1rem;
    }
    .summary-eyebrow {
        color: var(--rt-muted);
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }
    .summary-value {
        color: #F8FAFC;
        font-family: var(--rt-mono);
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.45rem;
    }
    .summary-caption {
        color: #CBD5E1;
        font-size: 0.84rem;
        line-height: 1.55;
    }
    .status-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.28rem 0.6rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border: 1px solid rgba(148, 163, 184, 0.12);
        background: rgba(148, 163, 184, 0.08);
        color: #CBD5E1;
    }

    .rich-text-card p {
        color: #CBD5E1;
        font-size: 0.91rem;
        line-height: 1.75;
        margin: 0 0 0.85rem;
    }
    .rich-text-card p:last-child {
        margin-bottom: 0;
    }
    .rich-text-card strong {
        color: #F8FAFC;
        font-weight: 700;
    }
    .rich-text-list {
        margin: 0.35rem 0 0.9rem;
        padding-left: 1.15rem;
    }
    .rich-text-list li {
        color: #CBD5E1;
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
        border: 1px solid rgba(245, 158, 11, 0.18);
        background: rgba(245, 158, 11, 0.08);
        color: #FCD34D;
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
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.92), rgba(59, 130, 246, 0.88));
        color: white;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.9rem;
    }

    /* ── Veri Kaynak Badge'leri ── */
    .source-badge {
        display: inline-block;
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
        color: #94A3B8;
        margin: 0.25rem;
    }
    .source-badge.active {
        border-color: #10B981;
        color: #10B981;
    }
    .source-badge.optional {
        border-color: #F59E0B;
        color: #F59E0B;
    }

    /* ── Disclaimer Kutusu ── */
    .disclaimer-box {
        background: linear-gradient(135deg, rgba(62, 37, 12, 0.66) 0%, rgba(30, 41, 59, 0.82) 100%);
        border: 1px solid rgba(245, 158, 11, 0.42);
        border-radius: 18px;
        padding: 1.25rem;
        margin: 1.5rem 0;
    }
    .disclaimer-box p {
        color: #FCD34D !important;
        font-size: 0.85rem;
        margin: 0;
    }

    /* ── Tablo ── */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* ── Divider ── */
    hr { border-color: rgba(148, 163, 184, 0.12) !important; }

    /* ── Senaryo Delta ── */
    .delta-positive { color: #10B981; font-weight: 700; }
    .delta-negative { color: #EF4444; font-weight: 700; }

    /* ── Sidebar Nav ── */
    .nav-item {
        padding: 0.6rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.25rem;
        cursor: pointer;
        transition: background 0.2s;
        color: #CBD5E1;
    }
    .nav-item:hover { background: rgba(14, 165, 233, 0.1); }
    .nav-item.active {
        background: rgba(14, 165, 233, 0.15);
        border-left: 3px solid #0EA5E9;
        color: #0EA5E9;
        font-weight: 600;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #1E293B !important;
        border-radius: 8px !important;
    }

    /* ── Section Header ── */
    .section-header {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #64748B;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
    }

    /* ── Metric inline ── */
    .metric-inline {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }
    .metric-inline-label { color: #94A3B8; font-size: 0.85rem; }
    .metric-inline-value { color: #F8FAFC; font-weight: 600; }

    /* ── Faz Kartları ── */
    .phase-card {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.74) 0%, rgba(9, 14, 26, 0.94) 100%);
        border-left: 4px solid #0EA5E9;
        border-radius: 0 18px 18px 0;
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
        border-top: 1px solid rgba(148, 163, 184, 0.08);
        border-right: 1px solid rgba(148, 163, 184, 0.08);
        border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }
    .phase-card.active { border-left-color: #10B981; }
    .phase-card.future { border-left-color: #64748B; opacity: 0.7; }

    .architecture-panel {
        display: grid;
        gap: 0.85rem;
    }
    .architecture-row {
        display: grid;
        grid-template-columns: 180px 1fr;
        gap: 1rem;
        padding: 0.9rem 1rem;
        background: rgba(148, 163, 184, 0.04);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 16px;
    }
    .architecture-label {
        color: #8AD4FF;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.76rem;
        font-weight: 600;
    }
    .architecture-text {
        color: #CBD5E1;
        font-size: 0.9rem;
        line-height: 1.65;
    }

    @media (max-width: 1200px) {
        .hero-meta-grid {
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
        .main .block-container {
            padding-top: 1.4rem;
        }
        .hero-section {
            padding: 1.8rem 1.2rem 1.4rem;
        }
        .hero-title {
            font-size: 2.7rem;
        }
        .hero-meta-grid {
            grid-template-columns: 1fr;
        }
        .page-title {
            font-size: 1.85rem;
        }
        .summary-value {
            font-size: 1.6rem;
        }
    }
</style>
"""
