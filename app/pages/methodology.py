"""
RiskTwin - Veri ve Metodoloji Sayfası
Final Report ile uyumlu: Hazard bağlamı, veri kaynakları, scoring, explainability, ML readiness.
"""
import streamlit as st
import pandas as pd
import os
import pickle

from src.config import SCORE_WEIGHTS, MODELS_DIR
from components.metric_cards import render_disclaimer, render_summary_grid
from components.charts import create_feature_importance_chart


def render_methodology():
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Evidence Layer</div>
        <h1 class="page-title">Veri ve Metodoloji</h1>
        <p class="page-summary">
            Hazard bağlamı, skorlama mantığı, veri kaynakları ve hibrit ML altyapısı hakkında teknik çerçeve.
        </p>
        <div class="page-tags">
            <span class="page-tag">Hazard bağlamı</span>
            <span class="page-tag">Veri kaynakları</span>
            <span class="page-tag">Ağırlık mantığı</span>
            <span class="page-tag">ML hazırlığı</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_summary_grid([
        {"eyebrow": "Kanıt Modu", "value": "Açık", "value_size": "var(--rt-text-lg)", "caption": "Her veri katmanı görünür durumda"},
        {"eyebrow": "Skor Mantığı", "value": "5 Ağırlık", "value_size": "var(--rt-text-lg)", "caption": "Normalize edilmiş karar çerçevesi"},
        {"eyebrow": "XAI Hazırlığı", "value": "TRL-8", "value_size": "var(--rt-text-lg)", "value_color": "var(--rt-blue)", "caption": "Heuristic + ML birlikte okunabilir"},
        {"eyebrow": "Teknik Yorum", "chip": "Denetlenebilir metodoloji", "caption": "Pitch değil, ürün kanıt ekranı"},
    ])

    # ═══════════════════════════════════════
    # 1. HAZARD BAĞLAMI
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">HAZARD BAĞLAMI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8;">
            <strong style="color:var(--rt-text);">Hazard bağlamı, riskin tamamı değildir.</strong>
            Ayrıca hasar kanıtı da değildir. Hazard bağlamı, bir binanın bulunduğu konumun
            <strong style="color:var(--rt-blue);">deprem tehlikesi karakterini anlatan fiziksel çevre katmanıdır</strong>.
        </p>
        <div class="rt-grid-2" style="gap:var(--rt-space-lg); margin-top:var(--rt-space-md);">
            <div>
                <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">Bileşenler</div>
                <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Fay yakınlığı ve fay etkinliği</li>
                    <li>Beklenen sarsıntı profili</li>
                    <li>Jeolojik birim</li>
                    <li>Zeminsel tehlike özellikleri</li>
                    <li>Sıvılaşma, zemin büyütmesi, heyelan benzeri ek yer etkileri</li>
                </ul>
            </div>
            <div>
                <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">Kavramsal Ayrım</div>
                <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li><strong>Hazard bağlamı:</strong> yerin tehlike profili</li>
                    <li><strong>Kırılganlık (vulnerability):</strong> binanın bu tehlikeye nasıl tepki vereceği</li>
                    <li><strong>Damage evidence:</strong> deprem sonrası gözlenen hasar kanıtı</li>
                    <li><strong>Risk:</strong> bu katmanların karar bağlamı içinde birlikte değerlendirilmiş sonucu</li>
                </ul>
            </div>
        </div>
        <div class="rt-card__footer" style="color:var(--rt-text);">
            Eğer bina yalnız bina özellikleri üzerinden değerlendirilirse, iki benzer yapının tamamen farklı tehlike
            bağlamlarında bulunabileceği gözden kaçabilir. Bu nedenle hazard bağlamı bir ek özellik değil,
            <strong>sistemin çekirdek karar katmanlarından biridir</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 2. VERİ KAYNAKLARI
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">VERİ KAYNAKLARI</div>', unsafe_allow_html=True)

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
        <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">Bugün Gerçekten Kullanılan Veriler</div>
        <div class="rt-grid-2">
            <div class="metric-inline">
                <span class="metric-inline-label">AFAD Tehlike</span>
                <span class="rt-data-cell__label rt-data-cell__label--active">&#x2713; 5 lokasyon</span>
            </div>
            <div class="metric-inline">
                <span class="metric-inline-label">Bina Footprint</span>
                <span class="rt-data-cell__label rt-data-cell__label--active">&#x2713; 12 bina GeoJSON</span>
            </div>
            <div class="metric-inline">
                <span class="metric-inline-label">Kullanıcı Girdileri</span>
                <span class="rt-data-cell__label rt-data-cell__label--active">&#x2713; 7 parametre</span>
            </div>
            <div class="metric-inline">
                <span class="metric-inline-label">Nüfus Bağlamı</span>
                <span class="rt-data-cell__label rt-data-cell__label--pending">&#x25CB; Opsiyonel</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card rt-card--compact" style="margin-top:var(--rt-space-md);">
            <div class="rt-grid-3">
                <div class="rt-weight-cell">
                    <div class="summary-eyebrow">Hazard</div>
                    <div class="summary-value" style="font-size:var(--rt-text-lg);">30%</div>
                    <div class="summary-caption">Tehlike sinyali</div>
                </div>
                <div class="rt-weight-cell">
                    <div class="summary-eyebrow">Exposure</div>
                    <div class="summary-value" style="font-size:var(--rt-text-lg);">30%</div>
                    <div class="summary-caption">Yapı ve bağlam etkisi</div>
                </div>
                <div class="rt-weight-cell">
                    <div class="summary-eyebrow">Vulnerability</div>
                    <div class="summary-value" style="font-size:var(--rt-text-lg);">40%</div>
                    <div class="summary-caption">Kırılganlık ve dayanım</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 3. SKORLAMA METODOLOJİSİ
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">SKORLAMA METODOLOJİSİ</div>', unsafe_allow_html=True)

    col_formula, col_weights = st.columns([1, 1])

    with col_formula:
        st.markdown("""
        <div class="rt-card">
            <div class="rt-accent-text" style="margin-bottom:0.75rem;">Risk Skoru Formülü</div>
            <div class="rt-code-block">
                risk_score =<br/>
                &nbsp;&nbsp;hazard_score &times; 0.30<br/>
                + soil_score &times; 0.25<br/>
                + age_score &times; 0.15<br/>
                + floor_score &times; 0.15<br/>
                + system_score &times; 0.15
            </div>
            <div class="rt-card__footer" style="border-top:none; color:var(--rt-muted);">
                Her alt skor 0-100 aralığında normalize edilir. Nihai skor da 0-100 bandındadır.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_weights:
        st.markdown("""
        <div class="rt-card">
            <div class="rt-accent-text" style="margin-bottom:0.75rem;">Risk Bandları</div>
            <div class="rt-risk-band-display">
                <div class="rt-risk-band-item rt-risk-band-item--low">
                    <div class="rt-risk-band-item__value">0-39</div>
                    <div class="rt-risk-band-item__label">Düşük</div>
                </div>
                <div class="rt-risk-band-item rt-risk-band-item--medium">
                    <div class="rt-risk-band-item__value">40-64</div>
                    <div class="rt-risk-band-item__label">Orta</div>
                </div>
                <div class="rt-risk-band-item rt-risk-band-item--high">
                    <div class="rt-risk-band-item__value">65-100</div>
                    <div class="rt-risk-band-item__label">Yüksek</div>
                </div>
            </div>
            <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">Ağırlık Dağılımı</div>
            <div class="metric-inline"><span class="metric-inline-label">Deprem Tehlikesi</span><span class="metric-inline-value">%30</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Zemin Sınıfı</span><span class="metric-inline-value">%25</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Bina Yaşı</span><span class="metric-inline-value">%15</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Kat Sayısı</span><span class="metric-inline-value">%15</span></div>
            <div class="metric-inline"><span class="metric-inline-label">Taşıyıcı Sistem</span><span class="metric-inline-value">%15</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 4. VERİ BOŞLUĞU YÖNETİMİ
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">VERİ BOŞLUĞU YÖNETİMİ</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8; margin-bottom:var(--rt-space-md);">
            RiskTwin'in en kritik tasarım tercihlerinden biri, <strong style="color:var(--rt-blue);">eksik veriyi inkâr etmek yerine onu yönetmektir</strong>.
        </p>
        <div class="rt-grid-2" style="gap:var(--rt-space-lg);">
            <div>
                <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">Birincil Veri Hattı</div>
                <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Kurumlar tarafından sağlanan hazard verileri</li>
                    <li>Belediye bina envanteri</li>
                    <li>Geçmiş deprem hasarı ve dayanıklılık davranışı</li>
                </ul>
            </div>
            <div>
                <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">İkincil Veri Hattı</div>
                <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Eski envanter + yeni post-deprem gözlem eşleştirmesi</li>
                    <li>Açık veri tabanları ve benchmark</li>
                    <li>Kontrollü proxy kullanımı</li>
                </ul>
            </div>
        </div>
        <div style="margin-top:var(--rt-space-md);">
            <div class="rt-accent-text" style="margin-bottom:var(--rt-space-sm);">Eksik Alan Karar Zinciri</div>
            <ol style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                <li>Açık kaynakta kesin eşleşme varsa <strong>doğrudan doldur</strong></li>
                <li>Semantik olarak savunulabilir proxy varsa <strong>kullan</strong></li>
                <li>Aksi durumda <strong>unknown/pending</strong> bırak</li>
            </ol>
        </div>
        <div class="rt-card__footer" style="color:var(--rt-text);">
            <strong>İlke:</strong> Şeffaflık, güvenin ön koşuludur. Eksik veriyi gizlemektense görünür kılmak daha doğrudur.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 5. AÇIKLANABİLİRLİK
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">AÇIKLANABİLİRLİK YAKLAŞIMI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div class="rt-accent-text" style="margin-bottom:0.75rem;">Kural Tabanlı Doğal Dil Açıklama</div>
        <p style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.7;">
            Her risk değerlendirmesi sonucunda sistem, Türkçe doğal dil ile açıklama üretir.
            Explainability isteğe bağlı bir süs değil, akademik ve kurumsal meşruiyet sağlayan ana bileşendir.
        </p>
        <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8;">
            <li>Riski en fazla artıran <strong style="color:var(--rt-text);">ilk 3 faktör</strong> belirlenir</li>
            <li>Her faktör için <strong style="color:var(--rt-text);">eşik tabanlı açıklama</strong> şablonu seçilir</li>
            <li>Senaryo karşılaştırmalarında <strong style="color:var(--rt-text);">delta açıklaması</strong> üretilir</li>
            <li>İnceleme önceliği ve önerilen aksiyon <strong style="color:var(--rt-text);">doğal dil ile</strong> sunulur</li>
        </ul>
        <div class="rt-card__footer">
            İleriki fazda: SHAP (SHapley Additive exPlanations) entegrasyonu ve counterfactual açıklamalar planlanmaktadır.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # 6. ML READINESS / BASELINE
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">ML ALT YAPISI VE BASELINE MODEL</div>', unsafe_allow_html=True)

    # Model durumu kontrol
    model_path = os.path.join(MODELS_DIR, "risk_model.pkl")
    model_available = os.path.exists(model_path)

    ml1, ml2 = st.columns([1, 1])

    with ml1:
        st.markdown("""
        <div class="rt-card">
            <div class="rt-accent-text" style="margin-bottom:0.75rem;">Hibrit Mimari: Heuristic + ML</div>
            <p style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.7;">
                Sistem heuristic-first, ML-optional tasarımla çalışır:
            </p>
            <ol style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8;">
                <li>Heuristic skorlama motoru her zaman çalışır (fallback)</li>
                <li>Eğitilmiş model varsa ML tahmini de üretilir</li>
                <li>Model yoksa yalnızca heuristic sonuç gösterilir</li>
                <li>Gerçek etiketli veri geldiğinde supervised model eğitilir</li>
            </ol>
            <div class="rt-card__footer">
                Pipeline: feature_engineering.py &rarr; train.py &rarr; predict.py
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
                    <div class="rt-ml-status">
                        <div class="rt-accent-text--emerald" style="font-weight:700;">Baseline Model: Aktif</div>
                        <div class="rt-ml-badge rt-ml-badge--trained">TRAINED</div>
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
                    st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)
                    st.markdown("**Feature Importance (Baseline Model)**")
                    fig = create_feature_importance_chart(features, list(model.feature_importances_))
                    st.plotly_chart(fig, use_container_width=True)

            except Exception:
                st.markdown("""
                <div class="rt-card">
                    <div class="rt-accent-text--amber">Model dosyası okunamadı</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="rt-card">
                <div class="rt-ml-status">
                    <div class="rt-accent-text--amber" style="font-weight:700;">Model: Eğitilmedi</div>
                    <div class="rt-ml-badge rt-ml-badge--untrained">NOT TRAINED</div>
                </div>
                <p style="color:var(--rt-muted); font-size:var(--rt-text-base);">
                    Baseline model henüz eğitilmemiş. Eğitmek için:<br/>
                    <code style="color:var(--rt-orange);">python3 src/train.py</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

    render_disclaimer()
