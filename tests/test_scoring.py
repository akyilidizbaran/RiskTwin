"""
RiskTwin Skorlama Motoru Testleri
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.scoring_engine import (
    evaluate_building,
    calculate_risk_score,
    get_risk_band,
    get_sub_scores,
    calculate_project_fit_score,
    get_inspection_priority,
)


class TestSubScores:
    """Alt skor hesaplama testleri."""

    def test_sub_scores_all_numeric(self):
        sub = get_sub_scores(hazard_score=70, soil_class="ZC", building_age=20, floor_count=5, structural_system="betonarme_cerceve")
        for key, value in sub.items():
            assert isinstance(value, (int, float)), f"{key} sayısal değil: {type(value)}"

    def test_sub_scores_range_0_100(self):
        sub = get_sub_scores(hazard_score=50, soil_class="ZD", building_age=40, floor_count=10, structural_system="yigma")
        for key, value in sub.items():
            assert 0 <= value <= 100, f"{key} 0-100 aralığında değil: {value}"

    def test_hazard_score_passthrough(self):
        sub = get_sub_scores(hazard_score=85)
        assert sub["hazard"] == 85

    def test_soil_class_mapping(self):
        for soil in ["ZA", "ZB", "ZC", "ZD", "ZE", "ZF"]:
            sub = get_sub_scores(soil_class=soil)
            assert 0 <= sub["soil"] <= 100

    def test_structural_system_mapping(self):
        for system in ["betonarme_perde", "celik", "betonarme_cerceve", "prefabrik", "yigma"]:
            sub = get_sub_scores(structural_system=system)
            assert 0 <= sub["system"] <= 100

    def test_age_thresholds(self):
        young = get_sub_scores(building_age=5)
        old = get_sub_scores(building_age=50)
        assert young["age"] < old["age"]

    def test_floor_thresholds(self):
        low = get_sub_scores(floor_count=2)
        high = get_sub_scores(floor_count=15)
        assert low["floors"] < high["floors"]


class TestRiskScore:
    """Risk skoru hesaplama testleri."""

    def test_risk_score_numeric(self):
        sub = get_sub_scores(hazard_score=50, soil_class="ZC")
        score = calculate_risk_score(sub)
        assert isinstance(score, float)

    def test_risk_score_range(self):
        sub = get_sub_scores(hazard_score=50, soil_class="ZC", building_age=20, floor_count=5, structural_system="betonarme_cerceve")
        score = calculate_risk_score(sub)
        assert 0 <= score <= 100

    def test_high_risk_inputs_produce_high_score(self):
        sub = get_sub_scores(hazard_score=90, soil_class="ZE", building_age=60, floor_count=12, structural_system="yigma")
        score = calculate_risk_score(sub)
        assert score >= 65

    def test_low_risk_inputs_produce_low_score(self):
        sub = get_sub_scores(hazard_score=10, soil_class="ZA", building_age=3, floor_count=2, structural_system="betonarme_perde")
        score = calculate_risk_score(sub)
        assert score < 40


class TestRiskBand:
    """Risk bandı testi."""

    def test_low_band(self):
        band = get_risk_band(25)
        assert band["label"] == "Düşük"

    def test_medium_band(self):
        band = get_risk_band(50)
        assert band["label"] == "Orta"

    def test_high_band(self):
        band = get_risk_band(80)
        assert band["label"] == "Yüksek"

    def test_boundary_39(self):
        band = get_risk_band(39)
        assert band["label"] == "Düşük"

    def test_boundary_40(self):
        band = get_risk_band(40)
        assert band["label"] == "Orta"

    def test_boundary_64(self):
        band = get_risk_band(64)
        assert band["label"] == "Orta"

    def test_boundary_65(self):
        band = get_risk_band(65)
        assert band["label"] == "Yüksek"


class TestProjectFitScore:
    """Proje uygunluk skoru testleri."""

    def test_fit_score_numeric(self):
        score = calculate_project_fit_score(50)
        assert isinstance(score, (int, float))

    def test_fit_score_range(self):
        score = calculate_project_fit_score(50)
        assert 0 <= score <= 100

    def test_retrofit_bonus(self):
        no_retrofit = calculate_project_fit_score(60, True, "yok")
        full_retrofit = calculate_project_fit_score(60, True, "tam")
        assert full_retrofit > no_retrofit


class TestInspectionPriority:
    """İnceleme önceliği testleri."""

    def test_priority_not_empty(self):
        level, text = get_inspection_priority(70)
        assert level != ""
        assert text != ""

    def test_high_risk_existing_building(self):
        level, text = get_inspection_priority(80, is_existing_building=True)
        assert level == "Yüksek"
        assert "mühendislik" in text.lower() or "inceleme" in text.lower()

    def test_high_risk_new_project(self):
        level, text = get_inspection_priority(80, is_existing_building=False)
        assert level == "Yüksek"
        assert "proje" in text.lower() or "revize" in text.lower()

    def test_low_risk(self):
        level, text = get_inspection_priority(20)
        assert level == "Düşük"


class TestEvaluateBuilding:
    """Tam değerlendirme testleri."""

    def test_evaluate_returns_all_keys(self):
        result = evaluate_building(hazard_score=70, soil_class="ZC")
        required_keys = ["sub_scores", "risk_score", "risk_band", "project_fit_score", "inspection_priority", "inspection_recommendation"]
        for key in required_keys:
            assert key in result, f"Eksik anahtar: {key}"

    def test_evaluate_default_params(self):
        result = evaluate_building()
        assert isinstance(result["risk_score"], float)
        assert result["risk_band"]["label"] in ["Düşük", "Orta", "Yüksek"]
