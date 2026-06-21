"""
RiskTwin - Ana Sayfa / Proje Tanıtımı
Final Report ile uyumlu: Hero, Problem, Çözüm, Nasıl Çalışır, Veri Kaynakları, Yol Haritası.
"""
import streamlit as st
from components.metric_cards import (
    render_feature_card,
    render_step_card,
    render_disclaimer,
    render_summary_grid,
    render_phase_card,
)


def render_home():
    # ═══════════════════════════════════════════
    # HERO BÖLÜMÜ
    # ═══════════════════════════════════════════
    st.markdown("""
    <div class="hero-section">
        <div class="hero-main">
            <div class="hero-kicker">Explainable Risk Decision Support</div>
            <div class="hero-title">RiskTwin</div>
            <div class="hero-subtitle">
                Belediye envanteri, hazard bağlamı, olay-bazlı hasar kanıtı ve açıklanabilir karar desteğini
                Digital Twin veri modelinde birleştiren deprem risk karar destek sistemi.
            </div>
            <div class="hero-meta-grid">
                <div class="hero-meta-card">
                    <div class="hero-meta-value">05</div>
                    <div class="hero-meta-label">Aktif lokasyon seti</div>
                </div>
                <div class="hero-meta-card">
                    <div class="hero-meta-value">36</div>
                    <div class="hero-meta-label">Demo bina girdisi</div>
                </div>
                <div class="hero-meta-card">
                    <div class="hero-meta-value">04</div>
                    <div class="hero-meta-label">Senaryo aksiyonu</div>
                </div>
                <div class="hero-meta-card">
                    <div class="hero-meta-value">TR</div>
                    <div class="hero-meta-label">Açıklanabilir çıktı dili</div>
                </div>
            </div>
        </div>
        <div class="hero-side">
            <div class="hero-side-card hero-side-card--signal">
                <div class="hero-side-label">Karar Destek Omurgası</div>
                <div class="hero-side-value">Event-aware, explainable, Digital Twin tabanlı</div>
                <div class="hero-side-desc">
                    Amaç güzel görünen bir demo değil; belediye, geliştirici ve teknik ekip için
                    aynı veriyi aynı karar zincirine bağlamak.
                </div>
                <div class="hero-signal-list">
                    <div class="hero-signal-item">
                        <div class="hero-signal-item__label">Karar Ailesi</div>
                        <div class="hero-signal-item__value">Risk + Uygunluk + Öncelik</div>
                    </div>
                    <div class="hero-signal-item">
                        <div class="hero-signal-item__label">Çekirdek Katman</div>
                        <div class="hero-signal-item__value">Hazard Bağlamı + Kırılganlık + Kanıt</div>
                    </div>
                    <div class="hero-signal-item">
                        <div class="hero-signal-item__label">Mimari</div>
                        <div class="hero-signal-item__value">Heuristic-first, ML-ready, Digital Twin</div>
                    </div>
                </div>
            </div>
            <div class="hero-side-card hero-side-card--command">
                <div class="hero-side-label">Akademik Kimlik</div>
                <div class="hero-side-desc">
                    Explainable, event-aware, Digital Twin tabanlı deprem risk karar destek sistemi.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-md"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="editorial-grid">
            <div class="editorial-card editorial-card--accent">
                <div class="summary-eyebrow">Ürün Vaadi</div>
                <h3 class="editorial-title">Deprem olmadan önce hangi yapıların daha kırılgan, daha öncelikli olduğunu açıklanabilir biçimde ayırt etmek.</h3>
                <p class="editorial-text">
                    RiskTwin bir dashboard koleksiyonu değil. Belediyenin risk taraması, geliştiricinin proje ön analizi
                    ve teknik ekibin inceleme önceliği aynı yüzeyde, aynı hazard bağlamı ve kırılganlık verileriyle okunur.
                    Her binaya aynı refleksle yaklaşmak yerine, önceden önceliklendirme yapabilmek temel hedeftir.
                </p>
            </div>
            <div class="editorial-card">
                <div class="summary-eyebrow">Neden RiskTwin?</div>
                <div class="editorial-list">
                    <div class="editorial-item">
                        <div class="editorial-item__code">RP</div>
                        <div>
                            <div class="editorial-item__title">Reaktiften proaktife geçiş</div>
                            <div class="editorial-item__desc">Deprem sonrası reaksiyon mantığı can kaybı ve kaynak israfı riskini artırır. Önceden önceliklendirme şarttır.</div>
                        </div>
                    </div>
                    <div class="editorial-item">
                        <div class="editorial-item__code">HB</div>
                        <div>
                            <div class="editorial-item__title">Hazard bağlamı olmadan karar verilemez</div>
                            <div class="editorial-item__desc">İki benzer yapı tamamen farklı tehlike bağlamlarında bulunabilir. Mekânsal zeka zorunludur.</div>
                        </div>
                    </div>
                    <div class="editorial-item">
                        <div class="editorial-item__code">EH</div>
                        <div>
                            <div class="editorial-item__title">Parçalı değerlendirme ekonomik hata üretir</div>
                            <div class="editorial-item__desc">Yanlış risk önceliklendirmesi yalnız teknik hata değil, güçlendirme bütçesinde ciddi maliyet zaafiyetine yol açar.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # PROBLEM BÖLÜMÜ
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">PROBLEM</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns([2, 1])
    with pc1:
        st.markdown("""
        <div class="rt-card">
            <h3 style="color:var(--rt-text); margin-top:0;">Deprem Öncesi Önceliklendirme Eksikliği</h3>
            <p style="color:var(--rt-text); line-height:1.7; font-size:0.95rem;">
            Depremle ilgili asıl problem çoğu zaman yalnızca deprem anı değildir. Asıl problem,
            <strong style="color:var(--rt-amber);">deprem öncesinde hangi yapının daha dikkat gerektirdiğini yeterince ayırt edememek</strong>
            ve deprem sonrasında çok büyük bir bina stoğu üzerinde zaman baskısı altında karar vermek zorunda kalmaktır.
            </p>
            <p style="color:var(--rt-text); line-height:1.7; font-size:0.95rem;">
            Eğer süreçler yalnız deprem sonrası reaksiyon mantığıyla yürütülürse üç büyük sorun ortaya çıkar:
            </p>
            <ol style="color:var(--rt-text); line-height:1.8; font-size:0.95rem;">
                <li><strong style="color:var(--rt-red);">Sınırlı insan kaynağı ve saha kapasitesi</strong> yanlış yere harcanabilir</li>
                <li><strong style="color:var(--rt-red);">Gerçekten yüksek öncelikli yapılar</strong> zamanında ele alınamayabilir</li>
                <li>Düşük öncelikli yapılara aşırı müdahale edilirken <strong style="color:var(--rt-red);">yüksek riskli alanlar gölgede kalabilir</strong></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    with pc2:
        st.markdown("""
        <div class="rt-card" style="text-align:center; padding:var(--rt-space-xl) var(--rt-space-md);">
            <div style="font-size:2.5rem; font-weight:800; color:var(--rt-red);">6.7M+</div>
            <div class="summary-caption" style="margin-top:var(--rt-space-xs);">
                Türkiye'de deprem riski altında<br/>tahmini yapı sayısı
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # ÇÖZÜM BÖLÜMÜ
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">ÇÖZÜM</div>', unsafe_allow_html=True)

    sol1, sol2, sol3 = st.columns(3)
    with sol1:
        render_feature_card(
            "RT", "Deprem Risk Taraması",
            "Bina parametrelerini hazard bağlamı (fay yakınlığı, zemin tehlikesi, sarsıntı profili) ile birleştirerek açıklanabilir risk skoru üretir."
        )
    with sol2:
        render_feature_card(
            "PQ", "Proje Uygunluk Kıyası",
            "Yapıların deprem bölgesine uygunluğunu kırılganlık (vulnerability) perspektifinden değerlendirir ve proje uygunluk skoru hesaplar."
        )
    with sol3:
        render_feature_card(
            "IO", "İnceleme Önceliği",
            "Risk seviyesine göre inceleme önceliği ve uyarı semantiği belirler. Hangi bina önce incelenmeli ve bu karar neden verildi?"
        )

    st.markdown(
        """
        <div class="rt-card rt-card--compact" style="margin-top:var(--rt-space-md);">
            <div class="summary-eyebrow">Çözüm Çerçevesi</div>
            <div class="summary-caption">
                RiskTwin yeni bir hasar sınıflandırıcı yarışına girmemektedir.
                Explainable, event-aware, bina düzeyi karar destek sistemi kurmaktadır.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # NASIL ÇALIŞIR?
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">NASIL ÇALIŞIR?</div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_step_card(1, "Konum Seç", "Haritadan veya listeden deprem bölgesindeki lokasyonu seç.")
    with s2:
        render_step_card(2, "Parametreleri Gir", "Bina yaşı, kat sayısı, taşıyıcı sistem ve zemin sınıfını belirle.")
    with s3:
        render_step_card(3, "Skoru Al", "Deprem risk skoru, proje uygunluk ve inceleme önceliğini gör.")
    with s4:
        render_step_card(4, "Senaryoları Kıyasla", "Güçlendirme, kat azaltma gibi alternatiflerin etkisini karşılaştır.")

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # VERİ KAYNAKLARI
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">VERİ KAYNAKLARI</div>', unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        render_feature_card(
            "AF", "AFAD",
            "Deprem tehlike verisi ve hazard bağlamı. Lokasyon bazlı tehlike profili üretilir."
        )
    with d2:
        render_feature_card(
            "OS", "OSM / Geofabrik",
            "Bina footprint, yol ağı, POI ve mahalle sınırı katmanları."
        )
    with d3:
        render_feature_card(
            "KG", "Kullanıcı Girdisi",
            "Bina yaşı, kat sayısı, taşıyıcı sistem, zemin sınıfı ve güçlendirme durumu."
        )
    with d4:
        render_feature_card(
            "TC", "TÜİK / TUCBS",
            "Nüfus yoğunluğu bağlam verisi ve coğrafi referans katmanları (opsiyonel)."
        )

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # ÜRÜN ÖZELLİKLERİ
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">ÜRÜN ÖZELLİKLERİ</div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
        <div class="rt-card">
            <div class="rt-feature-highlight">Açıklanabilir Skor</div>
            <div class="rt-feature-highlight__desc">Explainability isteğe bağlı bir süs değil, akademik ve kurumsal meşruiyet sağlayan ana bileşendir. Her skor kararı Türkçe doğal dil ile açıklanır.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="rt-card">
            <div class="rt-feature-highlight">Harita Destekli Analiz</div>
            <div class="rt-feature-highlight__desc">Folium tabanlı interaktif harita ile hazard bağlamı ve lokasyon bazlı risk görselleştirmesi.</div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="rt-card">
            <div class="rt-feature-highlight">Senaryo Karşılaştırma</div>
            <div class="rt-feature-highlight__desc">Güçlendirme, kat azaltma, zemin iyileştirme senaryolarının risk üzerindeki etkisini yan yana görün.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="rt-card">
            <div class="rt-feature-highlight">Hibrit Mimari: Heuristic + ML</div>
            <div class="rt-feature-highlight__desc">Heuristic ile başla, veri toplandıkça ML'e geç. Etiketli veri gerektirmez, hemen çalışır, uzmanlar doğrulayabilir. Veri büyüdükçe supervised modele geçiş hazır.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # YOL HARİTASI
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">YOL HARİTASI</div>', unsafe_allow_html=True)

    render_phase_card(
        "FAZ 1 — ŞU AN",
        "Heuristic MVP + Baseline ML",
        "Kural tabanlı skorlama, hazard bağlamı entegrasyonu, event-aware bina kaydı, senaryo karşılaştırma, açıklanabilir çıktı, demo veri seti, Streamlit dashboard",
        variant="active",
    )
    render_phase_card(
        "FAZ 2 — YAKIN GELECEK",
        "Gerçek Veri + Supervised Model",
        "AFAD/OSM otomatik entegrasyon, çoklu şehir, hasar etiketli veri ile supervised model eğitimi, SHAP açıklanabilirlik, PostGIS, provenance-rich kayıt",
        variant="default",
    )
    render_phase_card(
        "FAZ 3 — VİZYON",
        "Derin Entegrasyon + BIM",
        "BIM (IFC) dosya okuma, TUCBS/belediye açık veri entegrasyonu, zemin etüdü katmanı, FastAPI backend, çok kullanıcılı erişim, CI/CD",
        variant="future",
    )

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # DISCLAIMER
    # ═══════════════════════════════════════════
    render_disclaimer()
