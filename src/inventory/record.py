"""
RiskTwin — Yapı Envanteri Kayıt Modeli (provenans + güven + durum).

Tasarım ilkesi 10.1'in kod karşılığı: her bina özniteliği salt bir değer değil;
kaynağı, güven puanı ve durumu ile birlikte tutulur. Eksik öznitelikler
gizlenmez; "belirlenemedi" olarak işaretlenir (ilke 10.3).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class AttrStatus(str, Enum):
    """Bir özniteliğin gözlem durumu (üç-durumlu; ilke 10.3)."""
    OBSERVED = "gozlemlendi"                  # değer çıkarıldı, güvenilir
    NEEDS_FIELD = "saha_dogrulamasi_gerekli"  # aday/şüphe, doğrulama gerek
    UNDETERMINED = "belirlenemedi"            # bakıldı ama çıkarılamadı / kaynak yok


@dataclass
class AttributeRecord:
    """Tek bir öznitelik için değer + kaynak + güven + durum."""
    value: Any = None
    source: Optional[str] = None
    confidence: Optional[float] = None  # 0.0–1.0 (kalibre edilmiş hedef)
    status: AttrStatus = AttrStatus.UNDETERMINED

    @property
    def is_known(self) -> bool:
        return self.value is not None and self.status != AttrStatus.UNDETERMINED

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


# Yapı (bina-düzeyi) öznitelikleri = saha/kayıt gerektiren kritik küme.
# Konum-türevli (hazard, soil) öznitelikler her zaman doldurulabildiği için ayrıdır.
STRUCTURAL_ATTRS = ["building_age", "floor_count", "structural_system"]
SITE_ATTRS = ["hazard", "soil_class"]
EXTRA_ATTRS = ["usage_type", "is_existing_building", "retrofit_status"]
ALL_ATTRS = SITE_ATTRS + STRUCTURAL_ATTRS + EXTRA_ATTRS


@dataclass
class BuildingRecord:
    """Provenanslı bina envanteri kaydı (Adım 1 çıktısı, Adım 2 girdisi)."""
    building_id: str
    location_id: Optional[str] = None
    attributes: Dict[str, AttributeRecord] = field(default_factory=dict)
    geometry: Optional[dict] = None  # GeoJSON footprint (opsiyonel)

    # ---- erişim ----
    def get(self, name: str) -> AttributeRecord:
        return self.attributes.get(name, AttributeRecord())

    def value(self, name: str, default: Any = None) -> Any:
        rec = self.attributes.get(name)
        return rec.value if (rec is not None and rec.is_known) else default

    def set(
        self,
        name: str,
        value: Any,
        source: Optional[str] = None,
        confidence: Optional[float] = None,
        status: AttrStatus = AttrStatus.OBSERVED,
    ) -> "BuildingRecord":
        self.attributes[name] = AttributeRecord(
            value=value, source=source, confidence=confidence, status=status
        )
        return self

    def mark_undetermined(self, name: str, source: Optional[str] = None) -> "BuildingRecord":
        self.attributes[name] = AttributeRecord(
            value=None, source=source, confidence=None, status=AttrStatus.UNDETERMINED
        )
        return self

    # ---- tamlık & güven ----
    def completeness(self) -> float:
        """Kritik (yapısal) özniteliklerden bilinenlerin oranı (0–1)."""
        known = sum(1 for a in STRUCTURAL_ATTRS if self.get(a).is_known)
        return round(known / len(STRUCTURAL_ATTRS), 2)

    def mean_confidence(self) -> Optional[float]:
        vals = [
            self.get(a).confidence
            for a in ALL_ATTRS
            if self.get(a).is_known and self.get(a).confidence is not None
        ]
        return round(sum(vals) / len(vals), 2) if vals else None

    def missing_structural(self) -> List[str]:
        return [a for a in STRUCTURAL_ATTRS if not self.get(a).is_known]

    def needs_field_check(self) -> bool:
        return len(self.missing_structural()) > 0

    # ---- skor motoruna köprü ----
    def to_scoring_kwargs(self) -> Dict[str, Any]:
        """evaluate_building() çağrısı için kwargs; eksik yapısal öznitelik = None."""
        return {
            "hazard_score": self.value("hazard"),
            "soil_class": self.value("soil_class", "ZC"),
            "building_age": self.value("building_age"),        # None → site-only
            "floor_count": self.value("floor_count"),
            "structural_system": self.value("structural_system"),
            "is_existing_building": self.value("is_existing_building", True),
            "retrofit_status": self.value("retrofit_status", "yok"),
        }

    def to_row(self) -> Dict[str, Any]:
        """Düz satır: demo_building_inputs.csv üst kümesi + provenans alanları."""
        row: Dict[str, Any] = {"building_id": self.building_id, "location_id": self.location_id}
        for a in ALL_ATTRS:
            rec = self.get(a)
            row[a] = rec.value
            row[f"{a}__source"] = rec.source
            row[f"{a}__confidence"] = rec.confidence
            row[f"{a}__status"] = rec.status.value
        row["completeness"] = self.completeness()
        row["mean_confidence"] = self.mean_confidence()
        row["needs_field_check"] = self.needs_field_check()
        return row
