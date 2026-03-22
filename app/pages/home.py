"""
RiskTwin - Ana Sayfa / Proje Tanıtımı
Yarışma showcase sayfası: Hero, Problem, Çözüm, Nasıl Çalışır, Veri Kaynakları, Yol Haritası.
"""
import streamlit as st
from components.metric_cards import render_feature_card, render_step_card, render_disclaimer


def render_home():
    # ═══════════════════════════════════════════
    # HERO BÖLÜMÜ
    # ═══════════════════════════════════════════
    st.markdown("""
    <div class="hero-section">
        <div class="hero-kicker">Risk Intelligence Command</div>
        <div class="hero-title">RiskTwin</div>
        <div class="hero-subtitle">
            Bina ve parsel verisini deprem tehlikesi ve temel yapı parametreleriyle birleştirerek
            ön değerlendirme, senaryo kıyası ve inceleme önceliği üreten açıklanabilir bir karar destek platformu.
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
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1.15rem;">
            <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Stratejik Etiket</div>
                    <div class="status-chip" style="background:rgba(56,189,248,0.12); border-color:rgba(56,189,248,0.24); color:#8AD4FF;">KURUMSAL_TARAMA</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Karar Türü</div>
                    <div class="status-chip" style="background:rgba(34,197,94,0.12); border-color:rgba(34,197,94,0.24); color:#86EFAC;">AÇIKLANABİLİR_SKOR</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Ürün Çekirdeği</div>
                    <div class="summary-value" style="font-size:1.15rem;">3 Skor</div>
                    <div class="summary-caption">Risk, uygunluk, inceleme önceliği</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Olgunluk</div>
                    <div class="summary-value" style="font-size:1.15rem;">TRL-8</div>
                    <div class="summary-caption">Heuristic-first ürün ailesi</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="rt-card stat-card">
            <div class="stat-card-value" style="color:#38BDF8;">5</div>
            <div class="stat-card-label">Veri katmanı</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="rt-card stat-card">
            <div class="stat-card-value" style="color:#22C55E;">3</div>
            <div class="stat-card-label">Karar skoru</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="rt-card stat-card">
            <div class="stat-card-value" style="color:#F59E0B;">4+</div>
            <div class="stat-card-label">Aksiyon tipi</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="rt-card stat-card">
            <div class="stat-card-value" style="color:#F97316;">%100</div>
            <div class="stat-card-label">İzlenebilir mantık</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem;">
            <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Ürün Vaadi</div>
                    <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.3rem;">Parçalı saha verisini tek karar yüzeyinde toplamak.</div>
                    <div class="summary-caption">Belediye, geliştirici ve denetim ekipleri aynı sinyalleri aynı dilde okur.</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Zamanlama</div>
                    <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.3rem;">Risk taraması artık toplu ve erken yapılmak zorunda.</div>
                    <div class="summary-caption">Kentsel dönüşüm ve saha inceleme bütçeleri daha veri odaklı yönetilmeli.</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Uygulama Hedefi</div>
                    <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.3rem;">Streamlit içinde uygulanabilir premium arayüz.</div>
                    <div class="summary-caption">Gösterişli mockup değil, ürünleşebilir karar ekranı.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # PROBLEM BÖLÜMÜ
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">PROBLEM</div>', unsafe_allow_html=True)

    pc1, pc2 = st.columns([2, 1])
    with pc1:
        st.markdown("""
        <div class="rt-card">
            <h3 style="color:#F8FAFC; margin-top:0;">Parçalı Değerlendirme, Geç Kalan Kararlar</h3>
            <p style="color:#CBD5E1; line-height:1.7; font-size:0.95rem;">
            Türkiye'de bina ve proje kararları çoğu zaman deprem tehlikesi, yapı özellikleri ve mekânsal veriler
            arasında <strong style="color:#F59E0B;">parçalı biçimde</strong> değerlendiriliyor.
            Bu durum riskin geç fark edilmesine, yanlış önceliklendirmeye ve yavaş karar süreçlerine yol açıyor.
            </p>
            <p style="color:#CBD5E1; line-height:1.7; font-size:0.95rem;">
            Mevcut süreçler <strong style="color:#EF4444;">uzman bağımlı, zaman alıcı ve yüksek maliyetli</strong>.
            Milyonlarca yapının ön değerlendirmesi ölçeklenebilir bir yaklaşım gerektiriyor.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with pc2:
        st.markdown("""
        <div class="rt-card" style="text-align:center; padding:2rem 1rem;">
            <div style="font-size:2.5rem; font-weight:800; color:#EF4444;">6.7M+</div>
            <div style="font-size:0.85rem; color:#94A3B8; margin-top:0.25rem;">
                Türkiye'de deprem riski altında<br/>tahmini yapı sayısı
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # ÇÖZÜM BÖLÜMÜ
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">ÇÖZÜM</div>', unsafe_allow_html=True)

    sol1, sol2, sol3 = st.columns(3)
    with sol1:
        render_feature_card(
            "RT", "Deprem Risk Taraması",
            "Bina ve lokasyon parametrelerini deprem tehlikesi verileriyle birleştirerek hızlı ve açıklanabilir risk skoru üretir."
        )
    with sol2:
        render_feature_card(
            "PQ", "Proje Uygunluk Kıyası",
            "Mevcut veya planlanan yapıların deprem bölgesine uygunluğunu değerlendirir ve proje uygunluk skoru hesaplar."
        )
    with sol3:
        render_feature_card(
            "IO", "İnceleme Önceliği",
            "Risk seviyesine göre detaylı inceleme ve güçlendirme önceliği belirler, karar vericilere yol haritası sunar."
        )

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-top:1rem;">
            <div class="summary-eyebrow">Çözüm Çerçevesi</div>
            <div class="summary-caption">
                RiskTwin tek bir skor üreten araç değil; lokasyon, yapı durumu ve müdahale alternatiflerini
                aynı karar ailesine bağlayan kurumsal bir ön değerlendirme katmanıdır.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # NEDEN ŞİMDİ?
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">NEDEN ŞİMDİ?</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div class="insight-grid">
            <div class="insight-item">
                <div class="insight-item-head">
                    <div class="insight-item-code">RS</div>
                    <div class="insight-item-title">Deprem Gerçeği</div>
                </div>
                <div class="insight-item-text">
                    Türkiye dünyanın en aktif sismik bölgelerinden birinde. 2023 Kahramanmaraş depremleri bu gerçeği
                    bir kez daha hatırlattı. Proaktif risk taraması artık bir tercih değil, zorunluluk.
                </div>
            </div>
            <div class="insight-item">
                <div class="insight-item-head">
                    <div class="insight-item-code">KD</div>
                    <div class="insight-item-title">Kentsel Dönüşüm İhtiyacı</div>
                </div>
                <div class="insight-item-text">
                    Büyük geliştiriciler ve belediyeler için proje öncesi ön değerlendirme,
                    karar hızını artırır ve doğru yapılara öncelik verilmesini sağlar.
                </div>
            </div>
            <div class="insight-item">
                <div class="insight-item-head">
                    <div class="insight-item-code">VO</div>
                    <div class="insight-item-title">Veri Odaklı Karar Eksikliği</div>
                </div>
                <div class="insight-item-text">
                    Deprem riski, yapı durumu ve mekânsal veriler genellikle ayrı ayrı değerlendiriliyor.
                    Bütünleşik ve açıklanabilir bir karar destek aracı eksikliği giderilmelidir.
                </div>
            </div>
            <div class="insight-item">
                <div class="insight-item-head">
                    <div class="insight-item-code">ML</div>
                    <div class="insight-item-title">AI ile Ölçeklenebilirlik</div>
                </div>
                <div class="insight-item-text">
                    ML modelleriyle binlerce yapının eş zamanlı ön değerlendirilmesi mümkün hale geliyor.
                    Heuristic ile başla, veri toplandıkça öğrenen sisteme geç.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

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

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # VERİ KAYNAKLARI
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">VERİ KAYNAKLARI</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1rem;">
            <div class="summary-eyebrow">Kanıt Mantığı</div>
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.35rem;">Her veri kaynağı ürün içindeki rolüyle gösterilir.</div>
            <div class="summary-caption">Amaç veri adı saymak değil, karar mekanizmasına hangi girdinin nasıl girdiğini görünür yapmak.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    d1, d2, d3, d4 = st.columns(4)
    with d1:
        render_feature_card(
            "AF", "AFAD",
            "Deprem tehlike verisi. Lokasyon bazlı hazard input olarak kullanılır."
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

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # ÜRÜN ÖZELLİKLERİ
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">ÜRÜN ÖZELLİKLERİ</div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""
        <div class="rt-card">
            <div style="color:#10B981; font-weight:700; margin-bottom:0.5rem;">Açıklanabilir Skor</div>
            <div style="color:#94A3B8; font-size:0.85rem;">Her skor kararı Türkçe doğal dil ile açıklanır. Hangi faktörler riski artırıyor, neden bu öncelik verildi?</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="rt-card">
            <div style="color:#10B981; font-weight:700; margin-bottom:0.5rem;">Harita Destekli Analiz</div>
            <div style="color:#94A3B8; font-size:0.85rem;">Folium tabanlı interaktif harita ile lokasyon bazlı risk görselleştirmesi ve mahalle sınırları.</div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="rt-card">
            <div style="color:#10B981; font-weight:700; margin-bottom:0.5rem;">Senaryo Karşılaştırma</div>
            <div style="color:#94A3B8; font-size:0.85rem;">Güçlendirme, kat azaltma, zemin iyileştirme senaryolarının risk üzerindeki etkisini yan yana görün.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="rt-card">
            <div style="color:#10B981; font-weight:700; margin-bottom:0.5rem;">ML-Ready Mimari</div>
            <div style="color:#94A3B8; font-size:0.85rem;">Heuristic baseline + eğitilebilir ML pipeline. Veri toplandıkça supervised modele geçiş hazır.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem;">
            <div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Aksiyon Modeli</div>
                    <div class="summary-value" style="font-size:1.1rem;">4+</div>
                    <div class="summary-caption">Tara, kıyasla, önceliklendir, güçlendir</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Teknik İz</div>
                    <div class="summary-value" style="font-size:1.1rem;">%100</div>
                    <div class="summary-caption">Geri izlenebilir açıklama üretimi</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Ürün Dili</div>
                    <div class="summary-value" style="font-size:1.1rem;">TR</div>
                    <div class="summary-caption">Operasyon odaklı yerel karar metni</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # YOL HARİTASI
    # ═══════════════════════════════════════════
    st.markdown('<div class="section-header">YOL HARİTASI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="phase-card active">
        <div style="color:#10B981; font-weight:700; font-size:0.8rem; letter-spacing:0.05em;">FAZ 1 — ŞU AN</div>
        <div style="color:#F8FAFC; font-weight:600; margin:0.3rem 0;">Heuristic MVP + Baseline ML</div>
        <div style="color:#94A3B8; font-size:0.85rem;">Kural tabanlı skorlama, senaryo karşılaştırma, açıklanabilir çıktı, demo veri seti, Streamlit dashboard</div>
    </div>
    <div class="phase-card">
        <div style="color:#0EA5E9; font-weight:700; font-size:0.8rem; letter-spacing:0.05em;">FAZ 2 — YAKIN GELECEK</div>
        <div style="color:#F8FAFC; font-weight:600; margin:0.3rem 0;">Gerçek Veri + Supervised Model</div>
        <div style="color:#94A3B8; font-size:0.85rem;">AFAD/OSM otomatik entegrasyon, çoklu şehir, hasar etiketli veri ile model eğitimi, SHAP açıklanabilirlik</div>
    </div>
    <div class="phase-card future">
        <div style="color:#64748B; font-weight:700; font-size:0.8rem; letter-spacing:0.05em;">FAZ 3 — VİZYON</div>
        <div style="color:#F8FAFC; font-weight:600; margin:0.3rem 0;">Derin Entegrasyon + BIM</div>
        <div style="color:#94A3B8; font-size:0.85rem;">TUCBS/belediye açık veri, BIM dosya okuma, zemin etüdü katmanı, API layer, çok kullanıcılı erişim</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # DISCLAIMER
    # ═══════════════════════════════════════════
    render_disclaimer()
