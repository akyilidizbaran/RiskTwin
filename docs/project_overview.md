# Proje Genel Bakış

## Problem
Türkiye, yüksek sismik aktiviteye sahip bir coğrafyada yer almaktadır. Milyonlarca yapının deprem güvenliğinin hızlı, ölçeklenebilir ve açıklanabilir biçimde ön değerlendirilmesine ihtiyaç vardır. Mevcut yöntemler uzman bağımlı, zaman alıcı ve yüksek maliyetlidir.

## Çözüm
RiskTwin, bina/parsel verisini deprem tehlikesi, temel yapı parametreleri ve coğrafi katmanlarla birleştirerek:
- Deprem risk taraması
- Proje uygunluk kıyası
- İnceleme/güçlendirme önceliği

üreten AI destekli bir karar destek dijital twini MVP'sidir.

## Hedef Kullanıcı
- Belediye risk değerlendirme birimleri
- İnşaat/yapı denetim firmaları
- Kentsel dönüşüm proje ekipleri
- Afet yönetimi karar vericileri

## Örnek Kullanım Senaryosu

### Senaryo: Belediye risk taraması
1. Kullanıcı İstanbul Avcılar ilçesindeki bir binayı seçer
2. Bina parametrelerini girer: 30 yaşında, 6 kat, betonarme çerçeve, ZE zemin
3. RiskTwin 72/100 risk skoru hesaplar (Yüksek risk bandı)
4. Açıklama: "Riski en fazla artıran faktörler: zayıf zemin sınıfı ve yüksek deprem tehlikesi"
5. Senaryo: Güçlendirme uygulanırsa risk 63'e düşer (Orta banda geçiş)
6. Öneri: "Detaylı mühendislik incelemesi öncelikli"

### Senaryo: Yeni proje değerlendirmesi
1. Geliştirici yeni bir konut projesi için Kadıköy lokasyonunu seçer
2. Proje: 8 kat, betonarme perde, ZC zemin
3. RiskTwin uygunluk skoru ve senaryo karşılaştırması sunar
4. Alternatif: Kat sayısı 5'e düşürülürse risk skoru ve uygunluk nasıl değişir?
