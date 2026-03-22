"""
RiskTwin Grafik Bileşenleri
Plotly tabanlı profesyonel grafikler.
"""
import plotly.graph_objects as go
from typing import Dict, List

from components.styles import COLORS, RISK_COLORS


CHART_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#CBD5E1", family="IBM Plex Sans, sans-serif"),
    margin=dict(t=24, b=46, l=52, r=24),
    showlegend=False,
)


def create_factor_bar_chart(sub_scores: Dict[str, float], height: int = 320) -> go.Figure:
    """Yatay risk faktör bar chart."""
    factor_labels = {
        "hazard": "Deprem Tehlikesi",
        "soil": "Zemin Sınıfı",
        "age": "Bina Yaşı",
        "floors": "Kat Sayısı",
        "system": "Taşıyıcı Sistem",
    }
    # En yüksekten düşüğe sırala
    sorted_items = sorted(sub_scores.items(), key=lambda x: x[1])
    labels = [factor_labels.get(k, k) for k, _ in sorted_items]
    values = [v for _, v in sorted_items]
    colors = [
        RISK_COLORS["high"] if v >= 70 else RISK_COLORS["medium"] if v >= 40 else RISK_COLORS["low"]
        for v in values
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=values,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.0f}" for v in values],
        textposition="auto",
        textfont=dict(color="white", size=13, family="IBM Plex Sans, sans-serif"),
    ))
    fig.update_layout(
        **CHART_LAYOUT_DEFAULTS,
        height=height,
        xaxis=dict(range=[0, 100], title="Alt Skor (0-100)", gridcolor="#334155", zerolinecolor="#334155"),
        yaxis=dict(gridcolor="#334155"),
    )
    return fig


def create_scenario_comparison_chart(scenarios: List[Dict], height: int = 380) -> go.Figure:
    """Senaryo karşılaştırma grouped bar chart."""
    names = [sc["scenario_name"] for sc in scenarios]

    # Kısa isimler
    short_names = []
    for n in names:
        if len(n) > 25:
            short_names.append(n[:22] + "...")
        else:
            short_names.append(n)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Mevcut Risk",
        x=short_names,
        y=[sc["base_risk_score"] for sc in scenarios],
        marker_color=RISK_COLORS["high"],
        opacity=0.8,
        text=[f'{sc["base_risk_score"]:.0f}' for sc in scenarios],
        textposition="auto",
        textfont=dict(color="white", family="IBM Plex Sans, sans-serif"),
    ))
    fig.add_trace(go.Bar(
        name="Yeni Risk",
        x=short_names,
        y=[sc["new_risk_score"] for sc in scenarios],
        marker_color=RISK_COLORS["low"],
        opacity=0.8,
        text=[f'{sc["new_risk_score"]:.0f}' for sc in scenarios],
        textposition="auto",
        textfont=dict(color="white", family="IBM Plex Sans, sans-serif"),
    ))
    fig.update_layout(
        **{k: v for k, v in CHART_LAYOUT_DEFAULTS.items() if k != "showlegend"},
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            x=0.5,
            xanchor="center",
            bgcolor="rgba(10,15,27,0.0)",
            font=dict(color="#CBD5E1", family="IBM Plex Sans, sans-serif"),
        ),
        barmode="group",
        height=height,
        yaxis=dict(range=[0, 100], title="Risk Skoru", gridcolor="#334155", zerolinecolor="#334155"),
        xaxis=dict(gridcolor="#334155"),
    )
    return fig


def create_risk_gauge(score: float, height: int = 200) -> go.Figure:
    """Risk gauge/gösterge."""
    if score < 40:
        bar_color = RISK_COLORS["low"]
    elif score < 65:
        bar_color = RISK_COLORS["medium"]
    else:
        bar_color = RISK_COLORS["high"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(font=dict(size=36, color="#F8FAFC")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#64748B", tickwidth=1),
            bar=dict(color=bar_color, thickness=0.8),
            bgcolor="#1E293B",
            borderwidth=0,
            steps=[
                dict(range=[0, 39], color="rgba(16,185,129,0.15)"),
                dict(range=[40, 64], color="rgba(245,158,11,0.15)"),
                dict(range=[65, 100], color="rgba(239,68,68,0.15)"),
            ],
        ),
    ))
    fig.update_layout(
        **CHART_LAYOUT_DEFAULTS,
        height=height,
        margin=dict(t=30, b=10, l=30, r=30),
    )
    return fig


def create_feature_importance_chart(feature_names: list, importances: list, height: int = 300) -> go.Figure:
    """Feature importance bar chart (ML baseline)."""
    # Sırala
    sorted_pairs = sorted(zip(feature_names, importances), key=lambda x: x[1])
    labels = [p[0] for p in sorted_pairs]
    values = [p[1] for p in sorted_pairs]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels, x=values,
        orientation="h",
        marker_color=COLORS["secondary"],
        text=[f"{v:.3f}" for v in values],
        textposition="auto",
        textfont=dict(color="white", size=11, family="IBM Plex Sans, sans-serif"),
    ))
    fig.update_layout(
        **CHART_LAYOUT_DEFAULTS,
        height=height,
        xaxis=dict(title="Importance", gridcolor="#334155", zerolinecolor="#334155"),
        yaxis=dict(gridcolor="#334155"),
    )
    return fig
