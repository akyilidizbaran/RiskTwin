"""
RiskTwin — Envanter (provenans) + eksik-veri skorlama testleri.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.inventory.record import AttributeRecord, BuildingRecord, AttrStatus
from src.scoring_engine import evaluate_building, get_sub_scores, calculate_risk_score


class TestAttributeRecord:
    def test_known_when_value_and_observed(self):
        a = AttributeRecord(value=6, source="3B nokta bulutu", confidence=0.78, status=AttrStatus.OBSERVED)
        assert a.is_known is True

    def test_unknown_when_undetermined(self):
        a = AttributeRecord(value=None, status=AttrStatus.UNDETERMINED)
        assert a.is_known is False

    def test_to_dict_serializes_status(self):
        a = AttributeRecord(value=6, status=AttrStatus.OBSERVED)
        assert a.to_dict()["status"] == "gozlemlendi"


class TestBuildingRecord:
    def _full_record(self):
        r = BuildingRecord(building_id="BIN001", location_id="LOC001")
        r.set("hazard", 80, source="AFAD", confidence=0.9)
        r.set("soil_class", "ZE", source="İBB mikrobölgeleme", confidence=0.8)
        r.set("building_age", 45, source="İmar Barışı", confidence=0.7)
        r.set("floor_count", 6, source="footprint+yükseklik", confidence=0.6)
        r.set("structural_system", "betonarme_cerceve", source="İmar Barışı", confidence=0.65)
        return r

    def test_completeness_full(self):
        assert self._full_record().completeness() == 1.0

    def test_completeness_partial(self):
        r = self._full_record()
        r.mark_undetermined("structural_system", source="kayıt yok")
        assert r.completeness() == round(2 / 3, 2)

    def test_completeness_site_only(self):
        r = BuildingRecord(building_id="BIN002")
        r.set("hazard", 80, source="AFAD")
        r.set("soil_class", "ZD", source="MTA")
        assert r.completeness() == 0.0
        assert r.needs_field_check() is True
        assert set(r.missing_structural()) == {"building_age", "floor_count", "structural_system"}

    def test_mean_confidence(self):
        mc = self._full_record().mean_confidence()
        assert 0.0 <= mc <= 1.0

    def test_value_falls_back_for_unknown(self):
        r = BuildingRecord(building_id="X")
        assert r.value("building_age") is None
        assert r.value("soil_class", "ZC") == "ZC"

    def test_to_scoring_kwargs_missing_is_none(self):
        r = BuildingRecord(building_id="X")
        r.set("hazard", 80)
        r.set("soil_class", "ZD")
        kw = r.to_scoring_kwargs()
        assert kw["building_age"] is None
        assert kw["floor_count"] is None
        assert kw["structural_system"] is None
        assert kw["soil_class"] == "ZD"

    def test_to_row_has_provenance_columns(self):
        row = self._full_record().to_row()
        assert row["building_age"] == 45
        assert row["building_age__source"] == "İmar Barışı"
        assert row["building_age__status"] == "gozlemlendi"
        assert "completeness" in row and "needs_field_check" in row


class TestMissingDataScoring:
    def test_full_record_status_tam(self):
        r = BuildingRecord(building_id="BIN001")
        r.set("hazard", 80); r.set("soil_class", "ZE")
        r.set("building_age", 45); r.set("floor_count", 6)
        r.set("structural_system", "yigma")
        res = evaluate_building(**r.to_scoring_kwargs())
        assert res["data_status"] == "tam"
        assert res["needs_field_check"] is False
        assert res["completeness"] == 1.0

    def test_site_only_flags_field_check(self):
        r = BuildingRecord(building_id="BIN002")
        r.set("hazard", 80); r.set("soil_class", "ZE")
        res = evaluate_building(**r.to_scoring_kwargs())
        assert res["data_status"] == "site_only"
        assert res["needs_field_check"] is True
        assert res["completeness"] == 0.0
        # site-only skor yalnız hazard+soil'den; 0-100 aralığında geçerli
        assert 0 <= res["risk_score"] <= 100

    def test_partial_status_kismi(self):
        res = evaluate_building(hazard_score=80, soil_class="ZE", building_age=45,
                                floor_count=None, structural_system=None)
        assert res["data_status"] == "kismi"
        assert res["needs_field_check"] is True

    def test_missing_not_treated_as_safe(self):
        """Eksik yapısal veri, riski yapay olarak düşürmemeli (renormalizasyon)."""
        # Yüksek tehlike + zayıf zemin: site-only skor da yüksek olmalı.
        site_only = evaluate_building(hazard_score=90, soil_class="ZE",
                                      building_age=None, floor_count=None, structural_system=None)
        # Eğer eksikler 0 sayılsaydı skor düşerdi; renormalizasyon bunu engeller.
        assert site_only["risk_score"] >= 65


class TestRenormalizationInvariance:
    def test_full_inputs_unchanged(self):
        """Tüm faktörler mevcutken renormalizasyon klasik ağırlıklı ortalamayı değiştirmez."""
        sub = get_sub_scores(hazard_score=70, soil_class="ZD", building_age=40,
                             floor_count=10, structural_system="yigma")
        manual = (70 * 0.30 + sub["soil"] * 0.25 + sub["age"] * 0.15
                  + sub["floors"] * 0.15 + sub["system"] * 0.15)
        assert calculate_risk_score(sub) == round(manual, 1)


class TestSensitivity:
    def test_tornado_sorted_by_swing(self):
        from src.sensitivity import weight_sensitivity
        sub = get_sub_scores(hazard_score=70, soil_class="ZD", building_age=40,
                             floor_count=10, structural_system="yigma")
        rows = weight_sensitivity(sub, delta=0.10)
        assert len(rows) == 5
        swings = [r["swing"] for r in rows]
        assert swings == sorted(swings, reverse=True)
