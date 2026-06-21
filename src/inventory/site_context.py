"""
RiskTwin — Konuma dayalı tehlike + zemin bağlamı (Adım 1, site katmanı).

Bina yapı parametreleri eksik olsa bile, bir binanın ÜSTÜNDE durduğu konumun
tehlike (AFAD) ve zemin (MTA/İBB mikrobölgeleme) bağlamı her zaman türetilebilir
(tasarım ilkesi 10.5). Bu katman, eksik-veri durumunda "site-only" geçici skorun
temelini sağlar.

ÖNEMLİ — provenans dürüstlüğü: Bu MVP, ilçe-seviyesi YAKLAŞIK bir tehlike/zemin
modeli kullanır ve her değeri kaynağı + güven puanıyla işaretler. Sonraki adım:
AFAD TDTH servisinden koordinat-başı PGA/Ss/S1 ve İBB mikrobölgeleme GIS
dosyasından gerçek zemin sınıfı. Güven puanları bu yaklaşıklığı yansıtır.
"""
from __future__ import annotations

from typing import Dict, Tuple

# İstanbul, yüksek deprem tehlikesi bölgesinde (TDTH 2018). İlçe-seviyesi yaklaşık.
_ISTANBUL_HAZARD_SCORE = 80          # 0-100 (yüksek)
_HAZARD_SOURCE = "AFAD TDTH 2018 (İstanbul, ilçe seviyesi yaklaşık)"
_HAZARD_CONF = 0.6

# Zeytinburnu mikrobölgeleme (yaklaşık): güneye/sahile (düşük enlem) doğru alüvyal
# yumuşak zemin; kuzeye (yüksek enlem) doğru daha sıkı. Gerçek İBB GIS ile değişecek.
_SOIL_SOURCE = "İBB mikrobölgeleme (yaklaşık model — gerçek GIS ile değiştirilecek)"
_SOIL_CONF = 0.5


def get_site_context(lat: float, lon: float) -> Dict:
    """
    Koordinat için tehlike skoru ve zemin sınıfını (provenanslı) döndür.
    Returns: {hazard_score, hazard_source, hazard_conf, soil_class, soil_source, soil_conf}
    """
    if lat < 41.004:
        soil = "ZE"   # sahile yakın, zayıf/yumuşak alüvyon
    elif lat < 41.007:
        soil = "ZD"   # yumuşak
    else:
        soil = "ZC"   # daha sıkı zemin
    return {
        "hazard_score": _ISTANBUL_HAZARD_SCORE,
        "hazard_source": _HAZARD_SOURCE,
        "hazard_conf": _HAZARD_CONF,
        "soil_class": soil,
        "soil_source": _SOIL_SOURCE,
        "soil_conf": _SOIL_CONF,
    }
