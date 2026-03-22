"""
RiskTwin - Hakkında / Yol Haritası Sayfası
Projenin amacı, hedef kullanıcı, mimari ve gelişim planı.
"""
import streamlit as st
from components.metric_cards import render_disclaimer


def render_about():
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Strategy & Context</div>
        <h1 class="page-title">Hakkında</h1>
        <p class="page-summary">
            Proje vizyonu, hedef kullanıcı, mimari kararlar ve uzun vadeli gelişim çerçevesi.
            Bu sayfa ürünün neden var olduğunu ve hangi karar çevrelerinde değer ürettiğini özetler.
        </p>
        <div class="page-tags">
            <span class="page-tag">Kurumsal karar desteği</span>
            <span class="page-tag">Açıklanabilir risk mantığı</span>
            <span class="page-tag">Yol haritası görünümü</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem; margin-bottom:1.2rem;">
            <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:0.9rem;">
                <div>
                    <div class="summary-eyebrow">Bağlam Etiketi</div>
                    <div class="status-chip" style="background:rgba(56,189,248,0.12); border-color:rgba(56,189,248,0.24); color:#8AD4FF;">SİSMİK_GÜVENLİK</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Karar Katmanı</div>
                    <div class="status-chip" style="background:rgba(34,197,94,0.12); border-color:rgba(34,197,94,0.24); color:#86EFAC;">KURUMSAL_KARAR</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Teknik Yöntem</div>
                    <div class="status-chip" style="background:rgba(245,158,11,0.12); border-color:rgba(245,158,11,0.24); color:#FCD34D;">ML_TABANLI</div>
                </div>
                <div>
                    <div class="summary-eyebrow">Olgunluk Seviyesi</div>
                    <div class="summary-value" style="font-size:1.15rem;">TRL-8</div>
                    <div class="summary-caption">Heuristic-first ürün çekirdeği</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ═══════════════════════════════════════
    # PROJE AMACI
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">PROJE AMACI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.8;">
            <strong style="color:#F8FAFC;">RiskTwin</strong>, bina veya parsel verisini deprem tehlikesi, temel yapı/proje
            parametreleri ve coğrafi katmanlarla birleştirerek deprem risk taraması, proje uygunluk kıyası ve
            inceleme/güçlendirme önceliği üreten <strong style="color:#0EA5E9;">AI destekli bir karar destek dijital twini</strong> MVP'sidir.
        </p>
        <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.8;">
            Amacımız mühendislik kararını vermek değil, <strong style="color:#F59E0B;">doğru soruların doğru zamanda
            sorulmasını sağlamak</strong> ve karar vericileri veri odaklı biçimde bilgilendirmektir.
        </p>
    </div>
    """, unsafe_allow_html=True)

    mc1, mc2 = st.columns([1, 1])
    with mc1:
        st.markdown("""
        <div class="rt-card">
            <div class="summary-eyebrow">Ürün Misyonu</div>
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.45rem;">Doğru binaya, doğru inceleme sırasını vermek.</div>
            <div class="summary-caption">RiskTwin sahadaki belirsizliği azaltır, kararı görünür veriye bağlar.</div>
        </div>
        """, unsafe_allow_html=True)
    with mc2:
        st.markdown("""
        <div class="rt-card">
            <div class="summary-eyebrow">Kurumsal Vaad</div>
            <div style="color:#F8FAFC; font-weight:600; margin-bottom:0.45rem;">Uzman bilgisini ölçeklenebilir dijital karar ekranına çevirmek.</div>
            <div class="summary-caption">Belediye, geliştirici ve denetim ekipleri için ortak bir okuma zemini üretir.</div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # HEDEF KULLANICI
    # ═══════════════════════════════════════
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">HEDEF KULLANICI</div>', unsafe_allow_html=True)

    u1, u2, u3, u4 = st.columns(4)
    users = [
        ("BLD", "Belediyeler", "Risk değerlendirme birimleri, kentsel dönüşüm müdürlükleri"),
        ("YD", "Yapı Denetim", "İnşaat denetim firmaları, proje kontrol ekipleri"),
        ("GD", "Geliştiriciler", "Kentsel dönüşüm projecileri, büyük inşaat firmaları"),
        ("AF", "AFAD / İl Öİ", "Afet yönetimi karar vericileri, il özel idareleri"),
    ]
    for col, (icon, title, desc) in zip([u1, u2, u3, u4], users):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-badge">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # KULLANIM SENARYOLARI
    # ═══════════════════════════════════════
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">KULLANIM SENARYOLARI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div style="margin-bottom:1rem;">
            <div style="color:#0EA5E9; font-weight:600;">Senaryo 1: Belediye Toplu Risk Taraması</div>
            <div style="color:#94A3B8; font-size:0.85rem; line-height:1.6; margin-top:0.3rem;">
                Bir ilçede öncelikli inceleme gerektiren binaları hızla belirlemek.
                RiskTwin ile tüm binaları parametre bazlı tarayarak yüksek risk grubundakileri listeleyin.
            </div>
        </div>
        <div style="margin-bottom:1rem;">
            <div style="color:#0EA5E9; font-weight:600;">Senaryo 2: Yeni Proje Ön Değerlendirme</div>
            <div style="color:#94A3B8; font-size:0.85rem; line-height:1.6; margin-top:0.3rem;">
                Yeni bir konut projesi için lokasyon ve yapı parametrelerini girerek proje uygunluğunu kontrol etmek.
                Alternatif kat sayısı ve sistem senaryolarını karşılaştırmak.
            </div>
        </div>
        <div>
            <div style="color:#0EA5E9; font-weight:600;">Senaryo 3: Güçlendirme Önceliklendirme</div>
            <div style="color:#94A3B8; font-size:0.85rem; line-height:1.6; margin-top:0.3rem;">
                Mevcut yapı stoku içinde güçlendirme bütçesinin en etkili şekilde kullanılacağı binaları belirlemek.
                Güçlendirme senaryosunun risk düşürme potansiyelini görmek.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # MİMARİ
    # ═══════════════════════════════════════
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">TEKNİK MİMARİ</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div class="architecture-panel">
            <div class="architecture-row">
                <div class="architecture-label">Kullanıcı katmanı</div>
                <div class="architecture-text">Streamlit dashboard, Folium harita ve Plotly görselleştirmeleri ile karar ekranları tek yerde toplanır.</div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">İş mantığı</div>
                <div class="architecture-text">Scoring engine, scenario engine ve explainability modülleri riski hesaplar, kıyaslar ve Türkçe açıklamaya çevirir.</div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">ML hazırlığı</div>
                <div class="architecture-text">Feature engineering, eğitim ve predict katmanı heuristic yaklaşımı veri büyüdükçe supervised modele evriltecek şekilde hazırdır. Mevcut olgunluk seviyesi ürün mantığı için TRL-8 olarak konumlanır.</div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">Veri katmanı</div>
                <div class="architecture-text">AFAD, OSM, TÜİK ve kullanıcı girdileri aynı karar akışına beslenerek lokasyon ve yapı düzeyinde birlikte değerlendirilir.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="rt-card" style="padding:1rem 1.15rem;">
            <div class="summary-eyebrow">Mimari İlkesi</div>
            <div class="summary-caption">
                Ekranların tamamı belge kalitesinde okunabilirlik, veri izlenebilirliği ve operasyonel sadelik üzerine kuruludur.
                Bu sayfa ürün ailesinin stratejik çekirdeğini temsil eder.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ═══════════════════════════════════════
    # NEDEN HEURİSTİC + ML HİBRİT?
    # ═══════════════════════════════════════
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">NEDEN HEURİSTİC + ML HİBRİT?</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem;">
            <div>
                <div style="color:#10B981; font-weight:600; margin-bottom:0.5rem;">Heuristic Avantajları</div>
                <ul style="color:#94A3B8; font-size:0.85rem; line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Etiketli veri gerektirmez</li>
                    <li>Kurallar doğrudan açıklanabilir</li>
                    <li>Uzmanlar doğrulayabilir ve ayarlayabilir</li>
                    <li>Hemen çalışır, eğitim beklemez</li>
                </ul>
            </div>
            <div>
                <div style="color:#0EA5E9; font-weight:600; margin-bottom:0.5rem;">ML Avantajları</div>
                <ul style="color:#94A3B8; font-size:0.85rem; line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Veriden öğrenerek hassasiyet artışı</li>
                    <li>Non-linear ilişkileri yakalayabilir</li>
                    <li>Veri büyüdükçe performans artar</li>
                    <li>SHAP ile model açıklanabilirliği</li>
                </ul>
            </div>
        </div>
        <div style="color:#CBD5E1; font-size:0.85rem; margin-top:1rem; padding-top:0.75rem; border-top:1px solid #334155;">
            <strong style="color:#F8FAFC;">Strateji:</strong> Heuristic ile başla, veri toplandıkça ML'e geç.
            Her iki katman paralel çalışır; ML modeli heuristic'ten daha iyi performans gösterene kadar
            heuristic birincil motor olarak kalır.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # SINIRLILIKLAR
    # ═══════════════════════════════════════
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">TEKNİK SINIRLILIKLAR</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <ul style="color:#CBD5E1; font-size:0.85rem; line-height:1.8; margin:0; padding-left:1.2rem;">
            <li>MVP aşamasında <strong style="color:#F59E0B;">heuristic skorlama</strong> kullanılmaktadır</li>
            <li>Veri seti <strong style="color:#F59E0B;">demo/sentetik veriye</strong> dayanmaktadır</li>
            <li>Zemin verisi <strong style="color:#F59E0B;">kullanıcı girdisi</strong> olarak alınmaktadır</li>
            <li>Tek şehir (<strong style="color:#F59E0B;">İstanbul</strong>) için kurulmuştur</li>
            <li>AFAD otomatik entegrasyonu henüz <strong style="color:#F59E0B;">aktif değildir</strong></li>
            <li>Kesin statik proje üretmez, kolon/donatı boyutlandırmaz</li>
            <li>Resmi tahliye kararı vermez, mühendislik onayı yerine geçmez</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # GELİŞİM PLANI
    # ═══════════════════════════════════════
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">GELİŞİM PLANI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="phase-card active">
        <div style="color:#10B981; font-weight:700; font-size:0.8rem; letter-spacing:0.05em;">FAZ 1 — TAMAMLANDI</div>
        <div style="color:#F8FAFC; font-weight:600; margin:0.3rem 0;">Heuristic MVP + Baseline ML</div>
        <div style="color:#94A3B8; font-size:0.85rem;">
            Kural tabanlı skorlama, senaryo karşılaştırma, Türkçe açıklanabilir çıktı, demo veri seti,
            Streamlit dashboard, baseline ML pipeline, 39 test
        </div>
    </div>
    <div class="phase-card">
        <div style="color:#0EA5E9; font-weight:700; font-size:0.8rem; letter-spacing:0.05em;">FAZ 2 — SONRAKI</div>
        <div style="color:#F8FAFC; font-weight:600; margin:0.3rem 0;">Gerçek Veri + Supervised Model</div>
        <div style="color:#94A3B8; font-size:0.85rem;">
            AFAD/OSM otomatik entegrasyon, çoklu şehir, hasar etiketli veri ile model eğitimi,
            SHAP açıklanabilirlik, PostGIS, toplu tarama
        </div>
    </div>
    <div class="phase-card future">
        <div style="color:#64748B; font-weight:700; font-size:0.8rem; letter-spacing:0.05em;">FAZ 3 — VİZYON</div>
        <div style="color:#F8FAFC; font-weight:600; margin:0.3rem 0;">Derin Entegrasyon</div>
        <div style="color:#94A3B8; font-size:0.85rem;">
            BIM (IFC) dosya okuma, TUCBS/belediye açık veri, zemin etüdü katmanı,
            FastAPI backend, çok kullanıcılı erişim, CI/CD
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    render_disclaimer()
