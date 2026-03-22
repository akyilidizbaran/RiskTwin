"""
RiskTwin - Veri ve Metodoloji Sayfası
Jüri ve teknik inceleme için: veri kaynakları, scoring, explainability, ML readiness.
"""
import streamlit as st
import pandas as pd
import os
import pickle

from src.config import SCORE_WEIGHTS, MODELS_DIR
from components.metric_cards import render_disclaimer
from components.charts import create_feature_importance_chart


def render_methodology():
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Evidence Layer</div>
        <h1 class="page-title">Veri ve Metodoloji</h1>
        <p class="page-summary">
            Skorlama mantığı, veri kaynakları, açıklanabilirlik yaklaşımı ve ML altyapısı hakkında
            karar vericinin denetleyebileceği teknik çerçeve.
        </p>
        <div class="page-tags">
            <span class="page-tag">Veri kaynağı görünürlüğü</span>
            <span class="page-tag">Ağırlık mantığı</span>
            <span class="page-tag">ML hazırlık seviyesi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1.2rem;">
            <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Kanıt Modu</div>
                    <div class="summary-value" style="font-size:1.1rem;">Açık</div>
                    <div class="summary-caption">Her veri katmanı görünür durumda</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Skor Mantığı</div>
                    <div class="summary-value" style="font-size:1.1rem;">5 Ağırlık</div>
                    <div class="summary-caption">Normalize edilmiş karar çerçevesi</div>
                </div>
                <div>
                    <div class="summary-eyebrow">XAI Hazırlığı</div>
                    <div class="summary-value" style="font-size:1.1rem; color:#38BDF8;">TRL-8</div>
                    <div class="summary-caption">Heuristic + ML birlikte okunabilir</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Teknik Yorum</div>
                    <div class="status-chip">Denetlenebilir metodoloji</div>
                    <div class="summary-caption" style="margin-top:0.4rem;">Pitch değil, ürün kanıt ekranı</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ═══════════════════════════════════════
    # 1. VERİ KAYNAKLARI
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">VERİ KAYNAKLARI</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1rem;">
            <div class="summary-eyebrow">Kaynak Okuma Kuralı</div>
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.35rem;">Tablo, veri kökeni ile ürün kullanımı arasındaki bağı göstermek için tasarlandı.</div>
            <div class="summary-caption">Varsayılan spreadsheet hissi yerine ürünle bütünleşik kanıt panelleri hedefleniyor.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    data_sources = pd.DataFrame([
        {"Kaynak": "AFAD", "Tür": "Deprem Tehlike", "Kullanım": "Hazard input (tehlike skoru)", "Bugün Aktif": "Evet (demo)", "Not": "5 İstanbul lokasyonu, 0-100 normalize skor"},
        {"Kaynak": "OSM / Geofabrik", "Tür": "Geospatial", "Kullanım": "Bina, yol, POI, mahalle sınırı", "Bugün Aktif": "Evet (sentetik)", "Not": "Demo GeoJSON, gerçek veri entegrasyona hazır"},
        {"Kaynak": "Kullanıcı Girdisi", "Tür": "Yapı Parametreleri", "Kullanım": "Yaş, kat, sistem, zemin, güçlendirme", "Bugün Aktif": "Evet", "Not": "Ana girdi kaynağı"},
        {"Kaynak": "TÜİK ADNKS", "Tür": "Nüfus / Bağlam", "Kullanım": "Yoğunluk, etki potansiyeli", "Bugün Aktif": "Opsiyonel", "Not": "Örnek şema hazır, veri doldurulabilir"},
        {"Kaynak": "TUCBS", "Tür": "Coğrafi Referans", "Kullanım": "Kadastro, zemin, altyapı katmanları", "Bugün Aktif": "Referans", "Not": "WFS/WMS entegrasyonu ileriki fazda"},
    ])

    st.dataframe(data_sources, use_container_width=True, hide_index=True)

    # Bugün gerçekten ne kullanıldı
    st.markdown("""
    <div class="rt-card">
        <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.5rem;">Bugün Gerçekten Kullanılan Veriler</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
            <div class="metric-inline">
                <span class="metric-inline-label">AFAD Tehlike</span>
                <span style="color:#10B981; font-weight:600;">&#x2713; 5 lokasyon</span>
            </div>
            <div class="metric-inline">
                <span class="metric-inline-label">Bina Footprint</span>
                <span style="color:#10B981; font-weight:600;">&#x2713; 12 bina GeoJSON</span>
            </div>
            <div class="metric-inline">
                <span class="metric-inline-label">Kullanıcı Girdileri</span>
                <span style="color:#10B981; font-weight:600;">&#x2713; 7 parametre</span>
            </div>
            <div class="metric-inline">
                <span class="metric-inline-label">Nüfus Bağlamı</span>
                <span style="color:#F59E0B; font-weight:600;">&#x25CB; Opsiyonel</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-top:1rem;">
            <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:0.85rem;">
                <div style="background:rgba(15,23,42,0.56); border:1px solid rgba(148,163,184,0.1); border-radius:16px; padding:0.9rem;">
                    <div class="summary-eyebrow">Hazard</div>
                    <div class="summary-value" style="font-size:1.1rem;">30%</div>
                    <div class="summary-caption">Tehlike sinyali</div>
                </div>
                <div style="background:rgba(15,23,42,0.56); border:1px solid rgba(148,163,184,0.1); border-radius:16px; padding:0.9rem;">
                    <div class="summary-eyebrow">Exposure</div>
                    <div class="summary-value" style="font-size:1.1rem;">30%</div>
                    <div class="summary-caption">Yapı ve bağlam etkisi</div>
                </div>
                <div style="background:rgba(15,23,42,0.56); border:1px solid rgba(148,163,184,0.1); border-radius:16px; padding:0.9rem;">
                    <div class="summary-eyebrow">Vulnerability</div>
                    <div class="summary-value" style="font-size:1.1rem;">40%</div>
                    <div class="summary-caption">Kırılganlık ve dayanım</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 2. SKORLAMA METODOLOJİSİ
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">SKORLAMA METODOLOJİSİ</div>', unsafe_allow_html=True)

    col_formula, col_weights = st.columns([1, 1])

    with col_formula:
        st.markdown("""
        <div class="rt-card">
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.75rem;">Risk Skoru Formülü</div>
            <div style="background:#0F172A; border-radius:8px; padding:1rem; font-family:monospace; color:#0EA5E9; font-size:0.85rem; line-height:1.8;">
                risk_score =<br/>
                &nbsp;&nbsp;hazard_score &times; 0.30<br/>
                + soil_score &times; 0.25<br/>
                + age_score &times; 0.15<br/>
                + floor_score &times; 0.15<br/>
                + system_score &times; 0.15
            </div>
            <div style="color:#94A3B8; font-size:0.8rem; margin-top:0.75rem;">
                Her alt skor 0-100 aralığında normalize edilir. Nihai skor da 0-100 bandındadır.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_weights:
        st.markdown("""
        <div class="rt-card">
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.75rem;">Risk Bandları</div>
            <div style="display:flex; gap:0.5rem; margin-bottom:1rem;">
                <div style="flex:1; background:#065F46; border-radius:8px; padding:0.5rem; text-align:center;">
                    <div style="color:#10B981; font-weight:700;">0-39</div>
                    <div style="color:#94A3B8; font-size:0.75rem;">Düşük</div>
                </div>
                <div style="flex:1; background:#78350F; border-radius:8px; padding:0.5rem; text-align:center;">
                    <div style="color:#F59E0B; font-weight:700;">40-64</div>
                    <div style="color:#94A3B8; font-size:0.75rem;">Orta</div>
                </div>
                <div style="flex:1; background:#7F1D1D; border-radius:8px; padding:0.5rem; text-align:center;">
                    <div style="color:#EF4444; font-weight:700;">65-100</div>
                    <div style="color:#94A3B8; font-size:0.75rem;">Yüksek</div>
                </div>
            </div>
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.5rem;">Ağırlık Dağılımı</div>
            <div class="metric-inline"><span class="metric-inline-label">Deprem Tehlikesi</span><span class="metric-inline-value">%30</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Zemin Sınıfı</span><span class="metric-inline-value">%25</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Bina Yaşı</span><span class="metric-inline-value">%15</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Kat Sayısı</span><span class="metric-inline-value">%15</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Taşıyıcı Sistem</span><span class="metric-inline-value">%15</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 3. AÇIKLANABİLİRLİK
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">AÇIKLANABİLİRLİK YAKLAŞIMI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.75rem;">Kural Tabanlı Doğal Dil Açıklama</div>
        <p style="color:#CBD5E1; font-size:0.9rem; line-height:1.7;">
            Her risk değerlendirmesi sonucunda sistem, Türkçe doğal dil ile açıklama üretir:
        </p>
        <ul style="color:#CBD5E1; font-size:0.85rem; line-height:1.8;">
            <li>Riski en fazla artıran <strong style="color:#F8FAFC;">ilk 3 faktör</strong> belirlenir</li>
            <li>Her faktör için <strong style="color:#F8FAFC;">eşik tabanlı açıklama</strong> şablonu seçilir</li>
            <li>Senaryo karşılaştırmalarında <strong style="color:#F8FAFC;">delta açıklaması</strong> üretilir</li>
            <li>İnceleme önceliği ve önerilen aksiyon <strong style="color:#F8FAFC;">doğal dil ile</strong> sunulur</li>
        </ul>
        <div style="color:#64748B; font-size:0.8rem; margin-top:0.75rem; border-top:1px solid #334155; padding-top:0.5rem;">
            İleriki fazda: SHAP (SHapley Additive exPlanations) entegrasyonu ve counterfactual açıklamalar planlanmaktadır.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem;">
            <div class="summary-eyebrow">XAI Notu</div>
            <div class="summary-caption">
                Heuristic açıklamalar bugün doğrudan üretimde kullanılabilir. SHAP ve karşı-olgusal açıklama katmanı,
                veri derinliği arttığında aynı panel ailesine eklenecek şekilde planlandı.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 4. ML READINESS / BASELINE
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">ML ALT YAPISI VE BASELINE MODEL</div>', unsafe_allow_html=True)

    # Model durumu kontrol
    model_path = os.path.join(MODELS_DIR, "risk_model.pkl")
    model_available = os.path.exists(model_path)

    ml1, ml2 = st.columns([1, 1])

    with ml1:
        st.markdown("""
        <div class="rt-card">
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.75rem;">Hibrit Mimari: Heuristic + ML</div>
            <p style="color:#CBD5E1; font-size:0.85rem; line-height:1.7;">
                Sistem heuristic-first, ML-optional tasarımla çalışır:
            </p>
            <ol style="color:#CBD5E1; font-size:0.85rem; line-height:1.8;">
                <li>Heuristic skorlama motoru her zaman çalışır (fallback)</li>
                <li>Eğitilmiş model varsa ML tahmini de üretilir</li>
                <li>Model yoksa yalnızca heuristic sonuç gösterilir</li>
                <li>Gerçek etiketli veri geldiğinde supervised model eğitilir</li>
            </ol>
            <div style="color:#64748B; font-size:0.8rem; margin-top:0.5rem;">
                Pipeline: feature_engineering.py → train.py → predict.py
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ml2:
        if model_available:
            try:
                with open(model_path, "rb") as f:
                    model_data = pickle.load(f)
                model_name = model_data.get("model_name", "N/A")
                accuracy = model_data.get("accuracy", 0)
                f1 = model_data.get("f1", 0)
                features = model_data.get("feature_names", [])

                st.markdown(f"""
                <div class="rt-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                        <div style="color:#10B981; font-weight:700;">Baseline Model: Aktif</div>
                        <div style="background:#065F46; border-radius:6px; padding:0.25rem 0.75rem; font-size:0.75rem; color:#10B981;">TRAINED</div>
                    </div>
                    <div class="metric-inline"><span class="metric-inline-label">Model</span><span class="metric-inline-value">{model_name}</span></div>
                    <div class="metric-inline"><span class="metric-inline-label">Accuracy</span><span class="metric-inline-value">{accuracy:.3f}</span></div>
                    <div class="metric-inline"><span class="metric-inline-label">F1 Score</span><span class="metric-inline-value">{f1:.3f}</span></div>
                    <div class="metric-inline"><span class="metric-inline-label">Feature Sayısı</span><span class="metric-inline-value">{len(features)}</span></div>
                    <div class="note-inline">
                        Demo bootstrap model: heuristic skorlardan türetilmiş başlangıç eğitimi
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Feature importance
                model = model_data.get("model")
                if hasattr(model, "feature_importances_") and features:
                    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                    st.markdown("**Feature Importance (Baseline Model)**")
                    fig = create_feature_importance_chart(features, list(model.feature_importances_))
                    st.plotly_chart(fig, use_container_width=True)

            except Exception:
                st.markdown("""
                <div class="rt-card">
                    <div style="color:#F59E0B; font-weight:600;">Model dosyası okunamadı</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="rt-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
                    <div style="color:#F59E0B; font-weight:700;">Model: Eğitilmedi</div>
                    <div style="background:#78350F; border-radius:6px; padding:0.25rem 0.75rem; font-size:0.75rem; color:#F59E0B;">NOT TRAINED</div>
                </div>
                <p style="color:#94A3B8; font-size:0.85rem;">
                    Baseline model henüz eğitilmemiş. Eğitmek için:<br/>
                    <code style="color:#0EA5E9;">python3 src/train.py</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

    render_disclaimer()
