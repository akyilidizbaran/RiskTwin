"""
RiskTwin - Hakkında / Yol Haritası Sayfası
Final Report ile uyumlu: Proje amacı, literatür, özgünlük, mimari, sınırlar ve gelişim planı.
"""
import os
import base64
import streamlit as st
from components.metric_cards import render_disclaimer, render_summary_grid, render_phase_card


def render_about():
    st.markdown("""
    <div class="page-hero">
        <div class="page-kicker">Strategy & Context</div>
        <h1 class="page-title">Hakkında</h1>
        <p class="page-summary">
            Proje vizyonu, literatür bağlamı, özgünlük, mimari kararlar ve gelişim planı.
        </p>
        <div class="page-tags">
            <span class="page-tag">Karar desteği</span>
            <span class="page-tag">Açıklanabilir risk</span>
            <span class="page-tag">Digital Twin</span>
            <span class="page-tag">Yol haritası</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_summary_grid([
        {"eyebrow": "Bağlam Etiketi", "chip": "SİSMİK_GÜVENLİK", "chip_variant": "blue", "caption": ""},
        {"eyebrow": "Karar Katmanı", "chip": "KURUMSAL_KARAR", "chip_variant": "green", "caption": ""},
        {"eyebrow": "Teknik Yöntem", "chip": "DT_TABANLI", "chip_variant": "amber", "caption": ""},
        {"eyebrow": "Olgunluk Seviyesi", "value": "TRL-8", "value_size": "var(--rt-text-lg)", "caption": "Heuristic-first ürün çekirdeği"},
    ])

    # ═══════════════════════════════════════
    # PROJE AMACI
    # ═══════════════════════════════════════
    st.markdown('<div class="section-header">PROJE AMACI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8;">
            <strong style="color:var(--rt-text);">RiskTwin</strong>'in çıkış noktası yalnızca yeni bir deprem modeli geliştirmek değildir.
            Çıkış noktamız, Türkiye gibi yüksek sismik tehlike altında yaşayan bir ülkede,
            <strong style="color:var(--rt-blue);">deprem öncesi risk önceliklendirmesini daha rasyonel, daha açıklanabilir
            ve daha uygulanabilir hale getirmektir</strong>.
        </p>
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8;">
            RiskTwin'in temel problemi şudur: Deprem olmadan önce hangi bina veya bina gruplarının daha kırılgan,
            daha öncelikli ve daha dikkat gerektiren yapılar olduğunu; olay sonrası hasar kanıtı, açıklanabilir modelleme
            ve Digital Twin veri yapısı ile birlikte <strong style="color:var(--rt-amber);">anlamlı bir karar desteğine dönüştürmek</strong>.
        </p>
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8;">
            RiskTwin'in en doğru akademik kimliği:
            <strong style="color:var(--rt-text);">Explainable, event-aware, Digital Twin tabanlı deprem risk karar destek sistemi.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # LİTERATÜR BAĞLAMI
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">LİTERATÜR BAĞLAMI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8; margin-bottom:var(--rt-space-md);">
            Literatürde deprem problemine yaklaşım üç ana çizgide şekillenmektedir. RiskTwin, bu üç çizginin
            güçlü yönlerini aynı sistemde birleştirmeyi hedefler.
        </p>
        <div class="architecture-panel">
            <div class="architecture-row">
                <div class="architecture-label">Kocaeli DT-COP</div>
                <div class="architecture-text">
                    <strong style="color:var(--rt-text);">Mimari omurga referansı.</strong>
                    Digital Twin + Common Operating Picture mantığında deprem tehlikesi ve afet yönetimini birleştiren yapı.
                    Türkiye bağlamında DT yaklaşımının uygulanabilirliğini gösterir. Ancak explainable pre-risk skor ve
                    kullanıcıya dönük önceliklendirme semantiği eksiktir.
                </div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">DaDO / İtalya</div>
                <div class="architecture-text">
                    <strong style="color:var(--rt-text);">Veri mimarisi referansı.</strong>
                    Bina düzeyi observed damage arşivi ve event-aware veri mantığı kurar.
                    Farklı depremler arasında ortak veri disiplini sağlar. Ancak explainable ürün katmanı
                    ve belediye tabanlı güncel karar desteği odağı yoktur.
                </div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">Christchurch</div>
                <div class="architecture-text">
                    <strong style="color:var(--rt-text);">Modelleme ve çıktı mantığı referansı.</strong>
                    Bina özellikleri + shaking + observed consequence birleşimiyle kayıp tahmini yapar.
                    Consequence odaklı çıktı uzayı kurar. Ancak Digital Twin, provenance-rich bina kaydı
                    ve event-aware evidence modeli eksiktir.
                </div>
            </div>
        </div>
        <div class="rt-card__footer" style="color:var(--rt-text);">
            <strong>Sentez:</strong> Kocaeli bize mimari omurgayı, DaDO bize veri yapısını, Christchurch ise çıktı mantığını öğretmektedir.
            RiskTwin'in özgünlüğü, bu üç yönü aynı sistemde birleştirmesinde yatmaktadır.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # ÖZGÜNLÜK
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">PROJE ÖZGÜNLÜĞÜ</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8; margin-bottom:var(--rt-space-md);">
            RiskTwin'in farkı, literatürde bulunmayan yepyeni bir fizik ya da algoritma icat etmesinde değildir.
            Fark, <strong style="color:var(--rt-blue);">literatürde tek tek kanıtlanmış ama birbirinden kopuk duran katmanları birleştirmesindedir</strong>.
        </p>
        <ol style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:2;">
            <li><strong>Belediye bina envanterini</strong> merkez alması</li>
            <li><strong>Hazard bağlamını</strong> çekirdek karar katmanı yapması</li>
            <li><strong>Damage evidence</strong>'ı riskin kendisi değil, olay-bazlı kanıt katmanı olarak ele alması</li>
            <li><strong>Explainability</strong>'yi çekirdek bileşen olarak konumlaması</li>
            <li><strong>Digital Twin</strong>'i görselleştirme değil, veri omurgası olarak kullanması</li>
            <li>Kullanıcıya <strong>inceleme önceliği + dayanıklılık skoru + uyarı semantiği</strong> sunması</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # HEDEF KULLANICI
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
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
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">KULLANIM SENARYOLARI</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div class="rt-scenario-item">
            <div class="rt-scenario-item__title">Senaryo 1: Belediye Toplu Risk Taraması</div>
            <div class="rt-scenario-item__text">
                Bir ilçede öncelikli inceleme gerektiren binaları hızla belirlemek.
                RiskTwin ile tüm binaları hazard bağlamı ve yapı parametreleri bazında tarayarak yüksek risk grubundakileri listeleyin.
            </div>
        </div>
        <div class="rt-scenario-item">
            <div class="rt-scenario-item__title">Senaryo 2: Yeni Proje Ön Değerlendirme</div>
            <div class="rt-scenario-item__text">
                Yeni bir konut projesi için lokasyon ve yapı parametrelerini girerek proje uygunluğunu kontrol etmek.
                Alternatif kat sayısı ve sistem senaryolarını karşılaştırmak.
            </div>
        </div>
        <div class="rt-scenario-item">
            <div class="rt-scenario-item__title">Senaryo 3: Güçlendirme Önceliklendirme</div>
            <div class="rt-scenario-item__text">
                Mevcut yapı stoku içinde güçlendirme bütçesinin en etkili şekilde kullanılacağı binaları belirlemek.
                Güçlendirme senaryosunun risk düşürme potansiyelini görmek.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # TEKNİK MİMARİ
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">TEKNİK MİMARİ</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <p style="color:var(--rt-text); font-size:0.95rem; line-height:1.8; margin-bottom:var(--rt-space-md);">
            RiskTwin'in önerdiği yapı dört bileşenli bir karar destek omurgasıdır.
        </p>
        <div class="architecture-panel">
            <div class="architecture-row">
                <div class="architecture-label">Hazard bağlamı ayağı</div>
                <div class="architecture-text">AFAD ve ilgili kamu deprem tehlike yüzeyleri, fay yakınlığı ve fay etkinliği bilgileri, jeolojik ve zeminsel tehlike bağlamı. Bina konumuna bağlı hazard profilini üretir.</div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">Bina / learning ayağı</div>
                <div class="architecture-text">Belediye bina envanteri, geçmiş deprem performansı, gözlenen hasar davranışı, normalize dayanıklılık hedefleri. Bina verileri ile geçmiş davranış öğrenilir.</div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">Digital Twin ayağı</div>
                <div class="architecture-text">Tekil bina kaydı içinde envanter, hazard bağlamı, damage evidence, provenance, uncertainty, explainability ve warning/inspection priority birlikte tutulur.</div>
            </div>
            <div class="architecture-row">
                <div class="architecture-label">Kullanıcı çıktısı</div>
                <div class="architecture-text">Dayanıklılık skoru, inceleme önceliği, risk bandı / uyarı seviyesi ve açıklama metni. Otomatik yıkım kararı değil, ağır kararların önceliklendirme altyapısı.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # NEDEN HEURİSTİC + ML HİBRİT?
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">NEDEN HEURİSTİC + ML HİBRİT?</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div class="rt-grid-2" style="gap:var(--rt-space-lg);">
            <div>
                <div class="rt-feature-highlight">Heuristic Avantajları</div>
                <ul style="color:var(--rt-muted); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Etiketli veri gerektirmez</li>
                    <li>Kurallar doğrudan açıklanabilir</li>
                    <li>Uzmanlar doğrulayabilir ve ayarlayabilir</li>
                    <li>Hemen çalışır, eğitim beklemez</li>
                </ul>
            </div>
            <div>
                <div class="rt-accent-text--blue" style="font-weight:600; margin-bottom:var(--rt-space-sm);">ML Avantajları</div>
                <ul style="color:var(--rt-muted); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Veriden öğrenerek hassasiyet artışı</li>
                    <li>Non-linear ilişkileri yakalayabilir</li>
                    <li>Veri büyüdükçe performans artar</li>
                    <li>SHAP ile model açıklanabilirliği</li>
                </ul>
            </div>
        </div>
        <div class="rt-card__footer" style="color:var(--rt-text);">
            <strong style="color:var(--rt-text);">Strateji:</strong> Heuristic ile başla, veri toplandıkça ML'e geç.
            Her iki katman paralel çalışır; ML modeli heuristic'ten daha iyi performans gösterene kadar
            heuristic birincil motor olarak kalır.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # NE İDDİA EDİYORUZ / ETMİYORUZ
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">TEZ VE SINIRLAR</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="rt-card">
        <div class="rt-grid-2" style="gap:var(--rt-space-lg);">
            <div>
                <div class="rt-accent-text--emerald" style="font-weight:600; margin-bottom:var(--rt-space-sm);">Ne İddia Ediyoruz?</div>
                <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Explainable pre-risk / dayanıklılık önceliklendirmesi</li>
                    <li>Event-aware bina kaydı</li>
                    <li>Kullanıcıya dönük uyarı ve inceleme önceliği</li>
                    <li>Hazard bağlamı ile maliyet ve öncelik kararlarını daha rasyonel hale getirme</li>
                    <li>Eksik veri koşullarında dahi provenance-rich karar desteği üretme</li>
                </ul>
            </div>
            <div>
                <div class="rt-accent-text--amber" style="font-weight:600; margin-bottom:var(--rt-space-sm);">Ne İddia Etmiyoruz?</div>
                <ul style="color:var(--rt-text); font-size:var(--rt-text-base); line-height:1.8; margin:0; padding-left:1.2rem;">
                    <li>Tam doğrulanmış otomatik yıkım kararı</li>
                    <li>Eksiksiz gold-label tabanlı nihai model</li>
                    <li>Tüm eksik verilerin hatasız doldurulduğu bir sistem</li>
                    <li>Tüm bina stoğu için kurumsal doğrulukta geometri bind</li>
                    <li>Mühendislik onayı yerine geçen resmi karar</li>
                </ul>
            </div>
        </div>
        <div class="rt-card__footer" style="color:var(--rt-text);">
            Bu sınır projeyi zayıflatmaz. Aksine, akademik olarak daha savunulabilir hale getirir.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════
    # GELİŞİM PLANI
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">GELİŞİM PLANI</div>', unsafe_allow_html=True)

    render_phase_card(
        "FAZ 1 — TAMAMLANDI",
        "Heuristic MVP + Baseline ML",
        "Kural tabanlı skorlama, hazard bağlamı, event-aware bina kaydı, senaryo karşılaştırma, Türkçe açıklanabilir çıktı, demo veri seti, Streamlit dashboard, baseline ML pipeline",
        variant="active",
    )
    render_phase_card(
        "FAZ 2 — SONRAKI",
        "Gerçek Veri + Supervised Model",
        "AFAD/OSM otomatik entegrasyon, çoklu şehir, hasar etiketli veri ile supervised model eğitimi, SHAP açıklanabilirlik, PostGIS, provenance-rich kayıt, toplu tarama",
        variant="default",
    )
    render_phase_card(
        "FAZ 3 — VİZYON",
        "Derin Entegrasyon",
        "BIM (IFC) dosya okuma, TUCBS/belediye açık veri, zemin etüdü katmanı, FastAPI backend, çok kullanıcılı erişim, CI/CD",
        variant="future",
    )

    # ═══════════════════════════════════════
    # MOBİL ERİŞİM — QR KOD
    # ═══════════════════════════════════════
    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">MOBİL ERİŞİM</div>', unsafe_allow_html=True)

    _qr_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "qr_site.svg")
    try:
        with open(_qr_path, "r") as _f:
            _qr_b64 = base64.b64encode(_f.read().encode()).decode()
        st.markdown(f"""
        <div class="rt-card" style="text-align:center; padding:var(--rt-space-xl);">
            <div style="margin-bottom:var(--rt-space-md);">
                <img src="data:image/svg+xml;base64,{_qr_b64}" alt="RiskTwin QR" style="width:180px; height:180px;" />
            </div>
            <div style="font-size:1.1rem; font-weight:700; color:var(--rt-text); margin-bottom:var(--rt-space-xs);">
                RiskTwin'i Telefonunuzdan Deneyin
            </div>
            <div style="font-size:0.85rem; color:var(--rt-muted); margin-bottom:var(--rt-space-sm);">
                QR kodu tarayarak mobil cihazınızdan uygulamaya erişin.
            </div>
            <div style="font-size:0.75rem; color:var(--rt-subtle); font-family:var(--rt-mono);">
                aerolithsystems-risktwin.streamlit.app
            </div>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.markdown('<div class="rt-spacer-lg"></div>', unsafe_allow_html=True)
    render_disclaimer()
