"""
RiskTwin Metrik Kart Bileşenleri
Skor kartları, delta göstergeleri, bilgi kartları ve yeniden kullanılabilir layout bileşenleri.
"""
import html as html_lib
import re
from typing import List, Dict, Optional

import streamlit as st


# ── Skor Kartları (Birleştirilmiş) ──

def _render_score_card_base(label: str, value, band_class: str, band_text: str, value_style: str = ""):
    """Temel skor kartı renderer."""
    style_attr = f' style="{value_style}"' if value_style else ""
    markup = f"""
    <div class="score-card {band_class}">
        <div class="score-label">{label}</div>
        <div class="score-value"{style_attr}>{value}</div>
        <div class="score-band">{band_text}</div>
    </div>
    """
    st.markdown(markup, unsafe_allow_html=True)


def render_score_card(label: str, value, band_label: str, subtitle: str = ""):
    """Ana skor kartı."""
    band_class = {"Düşük": "low", "Orta": "medium", "Yüksek": "high"}.get(band_label, "medium")
    band_text = f"{band_label}{(' - ' + subtitle) if subtitle else ''}"
    _render_score_card_base(label, value, band_class, band_text)


def render_fit_card(label: str, value: float):
    """Proje uygunluk kartı."""
    if value >= 60:
        band_class, band_text = "low", "Uygun"
    elif value >= 40:
        band_class, band_text = "medium", "Koşullu"
    else:
        band_class, band_text = "high", "Riskli"
    _render_score_card_base(label, value, band_class, band_text)


def render_priority_card(label: str, priority: str):
    """İnceleme önceliği kartı."""
    band_class = {"Yüksek": "high", "Orta": "medium", "Düşük": "low"}.get(priority, "medium")
    _render_score_card_base(label, priority, band_class, "Öncelik Seviyesi", value_style="font-size:2rem;")


# ── Özellik ve Adım Kartları ──

def render_feature_card(icon: str, title: str, description: str):
    """Özellik tanıtım kartı."""
    markup = f"""
    <div class="feature-card">
        <div class="feature-badge">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """
    st.markdown(markup, unsafe_allow_html=True)


def render_step_card(number: int, title: str, description: str):
    """Adım kartı (nasıl çalışır akışı)."""
    markup = f"""
    <div class="rt-card step-card">
        <div class="step-number">{number}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """
    st.markdown(markup, unsafe_allow_html=True)


# ── Veri Kaynağı Badge ──

def render_data_source_badge(name: str, status: str = "active", description: str = ""):
    """Veri kaynağı badge'i."""
    cls = "active" if status == "active" else "optional"
    icon = "&#x2713;" if status == "active" else "&#x25CB;"
    markup = f"""
    <div class="source-badge {cls}">
        {icon} <strong>{name}</strong>{(' - ' + description) if description else ''}
    </div>
    """
    st.markdown(markup, unsafe_allow_html=True)


# ── Delta Göstergesi ──

def render_delta_indicator(label: str, base: float, new: float, inverse: bool = True):
    """Delta göstergesi (senaryo karşılaştırma için)."""
    delta = new - base
    if inverse:
        cls = "delta-positive" if delta < 0 else "delta-negative"
        arrow = "&#9660;" if delta < 0 else "&#9650;"
    else:
        cls = "delta-positive" if delta > 0 else "delta-negative"
        arrow = "&#9650;" if delta > 0 else "&#9660;"

    markup = f"""
    <div class="metric-inline">
        <span class="metric-inline-label">{label}</span>
        <span class="metric-inline-value">{base:.1f} &rarr; {new:.1f}
            <span class="{cls}">{arrow} {abs(delta):.1f}</span>
        </span>
    </div>
    """
    st.markdown(markup, unsafe_allow_html=True)


# ── Markdown → HTML ──

def _markdown_to_html(markdown_text: str) -> str:
    """Kısıtlı markdown içeriğini kart içinde gösterilecek HTML'e dönüştür."""
    blocks = []
    list_items = []

    for raw_line in markdown_text.strip().splitlines():
        line = raw_line.strip()

        if not line:
            if list_items:
                blocks.append("<ul class=\"rich-text-list\">" + "".join(list_items) + "</ul>")
                list_items = []
            continue

        if line.startswith("- "):
            item = html_lib.escape(line[2:].strip())
            item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item)
            list_items.append(f"<li>{item}</li>")
            continue

        if list_items:
            blocks.append("<ul class=\"rich-text-list\">" + "".join(list_items) + "</ul>")
            list_items = []

        paragraph = html_lib.escape(line)
        paragraph = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", paragraph)
        blocks.append(f"<p>{paragraph}</p>")

    if list_items:
        blocks.append("<ul class=\"rich-text-list\">" + "".join(list_items) + "</ul>")

    return "".join(blocks)


# ── Rich Text Kart ──

def render_rich_text_card(markdown_text: str, extra_class: str = ""):
    """Markdown tabanlı açıklamayı kart içinde tipografik olarak göster."""
    classes = "rt-card rich-text-card"
    if extra_class:
        classes = f"{classes} {extra_class}"

    html_content = _markdown_to_html(markdown_text)
    st.markdown(f'<div class="{classes}">{html_content}</div>', unsafe_allow_html=True)


# ── Disclaimer ──

def render_disclaimer():
    """Standart disclaimer kutusu."""
    st.markdown("""
    <div class="disclaimer-box">
        <p>&#9888; <strong>Önemli:</strong> RiskTwin bir ön değerlendirme ve karar destek MVP'sidir.
        Nihai mühendislik projelendirmesi veya resmi güvenlik kararı yerine geçmez.
        Tüm sonuçlar detaylı mühendislik incelemesiyle doğrulanmalıdır.</p>
    </div>
    """, unsafe_allow_html=True)


# ── Yeniden Kullanılabilir Layout Bileşenleri ──

def render_summary_grid(items: List[Dict], columns: int = 4):
    """Özet bilgi grid'i. Her item dict'i: eyebrow, value (veya chip), caption.
    Opsiyonel key'ler: value_color, value_size, chip_variant.
    """
    col_class = f"rt-grid-{columns}" if columns in (2, 3, 4) else "rt-grid-4"

    cells = []
    for item in items:
        eyebrow = item.get("eyebrow", "")
        caption = item.get("caption", "")

        if "chip" in item:
            variant = item.get("chip_variant", "")
            chip_cls = f"status-chip status-chip--{variant}" if variant else "status-chip"
            value_html = f'<div class="{chip_cls}">{item["chip"]}</div>'
        else:
            value = item.get("value", "")
            color = item.get("value_color", "")
            size = item.get("value_size", "")
            style_parts = []
            if size:
                style_parts.append(f"font-size:{size}")
            if color:
                style_parts.append(f"color:{color}")
            style_attr = f' style="{"; ".join(style_parts)}"' if style_parts else ""
            value_html = f'<div class="summary-value"{style_attr}>{value}</div>'

        cells.append(f"""<div>
            <div class="summary-eyebrow">{eyebrow}</div>
            {value_html}
            <div class="summary-caption">{caption}</div>
        </div>""")

    st.markdown(
        f'<div class="rt-card rt-card--compact"><div class="{col_class}">{"".join(cells)}</div></div>',
        unsafe_allow_html=True,
    )


def render_phase_card(label: str, title: str, description: str, variant: str = "default"):
    """Faz/yol haritası kartı. variant: 'active', 'default', 'future'."""
    card_cls = "phase-card"
    if variant == "active":
        card_cls += " active"
        label_cls = "phase-card__label phase-card__label--active"
    elif variant == "future":
        card_cls += " future"
        label_cls = "phase-card__label phase-card__label--future"
    else:
        label_cls = "phase-card__label phase-card__label--current"

    st.markdown(f"""
    <div class="{card_cls}">
        <div class="{label_cls}">{label}</div>
        <div class="phase-card__title">{title}</div>
        <div class="phase-card__desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)
