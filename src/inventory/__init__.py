"""
RiskTwin — Yapı Envanteri (Adım 1) modülü.

Açık veriden (Microsoft footprints, AFAD/MTA zemin+hazard, İmar Barışı/MEGSIS
örneklem) bina envanterini, her öznitelik için {değer, kaynak, güven, durum}
provenansıyla üretir ve mevcut skorlama motoruna (Adım 2) besler.
"""
from src.inventory.record import (
    AttributeRecord,
    BuildingRecord,
    AttrStatus,
    STRUCTURAL_ATTRS,
    SITE_ATTRS,
)

__all__ = [
    "AttributeRecord",
    "BuildingRecord",
    "AttrStatus",
    "STRUCTURAL_ATTRS",
    "SITE_ATTRS",
]
