"""
RiskTwin Metrik Kart Bileşenleri
Skor kartları, delta göstergeleri ve bilgi kartları.
"""
import html
import re

import streamlit as st


def render_score_card(label: str, value, band_label: str, subtitle: str = ""):
    """Ana skor kartı."""
    band_class = {"Düşük": "low", "Orta": "medium", "Yüksek": "high"}.get(band_label, "medium")
    html = f"""
    <div class="score-card {band_class}">
        <div class="score-label">{label}</div>
        <div class="score-value">{value}</div>
        <div class="score-band">{band_label}{(' - ' + subtitle) if subtitle else ''}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_fit_card(label: str, value: float):
    """Proje uygunluk kartı."""
    if value >= 60:
        band_class, band_text = "low", "Uygun"
    elif value >= 40:
        band_class, band_text = "medium", "Koşullu"
    else:
        band_class, band_text = "high", "Riskli"

    html = f"""
    <div class="score-card {band_class}">
        <div class="score-label">{label}</div>
        <div class="score-value">{value}</div>
        <div class="score-band">{band_text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_priority_card(label: str, priority: str):
    """İnceleme önceliği kartı."""
    band_class = {"Yüksek": "high", "Orta": "medium", "Düşük": "low"}.get(priority, "medium")
    html = f"""
    <div class="score-card {band_class}">
        <div class="score-label">{label}</div>
        <div class="score-value" style="font-size:2rem;">{priority}</div>
        <div class="score-band">Öncelik Seviyesi</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_feature_card(icon: str, title: str, description: str):
    """Özellik tanıtım kartı."""
    html = f"""
    <div class="feature-card">
        <div class="feature-badge">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_step_card(number: int, title: str, description: str):
    """Adım kartı (nasıl çalışır akışı)."""
    html = f"""
    <div class="rt-card step-card">
        <div class="step-number">{number}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_data_source_badge(name: str, status: str = "active", description: str = ""):
    """Veri kaynağı badge'i."""
    cls = "active" if status == "active" else "optional"
    icon = "&#x2713;" if status == "active" else "&#x25CB;"
    html = f"""
    <div class="source-badge {cls}">
        {icon} <strong>{name}</strong>{(' - ' + description) if description else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_delta_indicator(label: str, base: float, new: float, inverse: bool = True):
    """Delta göstergesi (senaryo karşılaştırma için)."""
    delta = new - base
    if inverse:
        cls = "delta-positive" if delta < 0 else "delta-negative"
        arrow = "&#9660;" if delta < 0 else "&#9650;"
    else:
        cls = "delta-positive" if delta > 0 else "delta-negative"
        arrow = "&#9650;" if delta > 0 else "&#9660;"

    html = f"""
    <div class="metric-inline">
        <span class="metric-inline-label">{label}</span>
        <span class="metric-inline-value">{base:.1f} &rarr; {new:.1f}
            <span class="{cls}">{arrow} {abs(delta):.1f}</span>
        </span>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


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
            item = html.escape(line[2:].strip())
            item = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", item)
            list_items.append(f"<li>{item}</li>")
            continue

        if list_items:
            blocks.append("<ul class=\"rich-text-list\">" + "".join(list_items) + "</ul>")
            list_items = []

        paragraph = html.escape(line)
        paragraph = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", paragraph)
        blocks.append(f"<p>{paragraph}</p>")

    if list_items:
        blocks.append("<ul class=\"rich-text-list\">" + "".join(list_items) + "</ul>")

    return "".join(blocks)


def render_rich_text_card(markdown_text: str, extra_class: str = ""):
    """Markdown tabanlı açıklamayı kart içinde tipografik olarak göster."""
    classes = "rt-card rich-text-card"
    if extra_class:
        classes = f"{classes} {extra_class}"

    html_content = _markdown_to_html(markdown_text)
    st.markdown(f'<div class="{classes}">{html_content}</div>', unsafe_allow_html=True)


def render_disclaimer():
    """Standart disclaimer kutusu."""
    st.markdown("""
    <div class="disclaimer-box">
        <p>&#9888; <strong>Önemli:</strong> RiskTwin bir ön değerlendirme ve karar destek MVP'sidir.
        Nihai mühendislik projelendirmesi veya resmi güvenlik kararı yerine geçmez.
        Tüm sonuçlar detaylı mühendislik incelemesiyle doğrulanmalıdır.</p>
    </div>
    """, unsafe_allow_html=True)
