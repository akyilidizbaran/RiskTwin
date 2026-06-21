"""
RiskTwin Grafik Bileşenleri
Plotly tabanlı profesyonel grafikler.
"""
import plotly.graph_objects as go
from typing import Dict, List

from components.styles import COLORS, RISK_COLORS


_FONT_FAMILY = "Inter, sans-serif"

_AXIS_DEFAULTS = dict(
    gridcolor="rgba(0, 0, 0, 0.06)",
    zerolinecolor="rgba(0, 0, 0, 0.06)",
)

CHART_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#1A1A2E", family=_FONT_FAMILY),
    margin=dict(t=24, b=46, l=52, r=24),
    showlegend=False,
)

_TEXT_FONT = dict(color="#FFFFFF", family=_FONT_FAMILY)


def create_factor_bar_chart(sub_scores: Dict[str, float], height: int = 320) -> go.Figure:
    """Yatay risk faktör bar chart."""
    factor_labels = {
        "hazard": "Deprem Tehlikesi",
        "soil": "Zemin Sınıfı",
        "age": "Bina Yaşı",
        "floors": "Kat Sayısı",
        "system": "Taşıyıcı Sistem",
    }
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
        textfont=dict(**_TEXT_FONT, size=13),
    ))
    fig.update_layout(
        **CHART_LAYOUT_DEFAULTS,
        height=height,
        xaxis=dict(range=[0, 100], title="Alt Skor (0-100)", **_AXIS_DEFAULTS),
        yaxis=dict(**_AXIS_DEFAULTS),
    )
    return fig


def create_scenario_comparison_chart(scenarios: List[Dict], height: int = 380) -> go.Figure:
    """Senaryo karşılaştırma grouped bar chart."""
    names = [sc["scenario_name"] for sc in scenarios]
    short_names = [n[:22] + "..." if len(n) > 25 else n for n in names]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Mevcut Risk",
        x=short_names,
        y=[sc["base_risk_score"] for sc in scenarios],
        marker_color=RISK_COLORS["high"],
        opacity=0.8,
        text=[f'{sc["base_risk_score"]:.0f}' for sc in scenarios],
        textposition="auto",
        textfont=_TEXT_FONT,
    ))
    fig.add_trace(go.Bar(
        name="Yeni Risk",
        x=short_names,
        y=[sc["new_risk_score"] for sc in scenarios],
        marker_color=RISK_COLORS["low"],
        opacity=0.8,
        text=[f'{sc["new_risk_score"]:.0f}' for sc in scenarios],
        textposition="auto",
        textfont=_TEXT_FONT,
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
            bgcolor="rgba(255,255,255,0)",
            font=dict(color="#1A1A2E", family=_FONT_FAMILY),
        ),
        barmode="group",
        height=height,
        yaxis=dict(range=[0, 100], title="Risk Skoru", **_AXIS_DEFAULTS),
        xaxis=dict(**_AXIS_DEFAULTS),
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
        number=dict(font=dict(size=36, color="#1A1A2E")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#9CA3AF", tickwidth=1),
            bar=dict(color=bar_color, thickness=0.8),
            bgcolor="#F8F9FA",
            borderwidth=0,
            steps=[
                dict(range=[0, 39], color="rgba(64,145,108,0.12)"),
                dict(range=[40, 64], color="rgba(242,140,40,0.12)"),
                dict(range=[65, 100], color="rgba(230,57,70,0.10)"),
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
        textfont=dict(**_TEXT_FONT, size=11),
    ))
    fig.update_layout(
        **CHART_LAYOUT_DEFAULTS,
        height=height,
        xaxis=dict(title="Importance", **_AXIS_DEFAULTS),
        yaxis=dict(**_AXIS_DEFAULTS),
    )
    return fig
