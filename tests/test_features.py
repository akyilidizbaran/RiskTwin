"""
RiskTwin Feature Engineering Testleri
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from src.feature_engineering import encode_features, prepare_training_data, get_feature_names


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {"building_age": 30, "floor_count": 5, "structural_system": "betonarme_cerceve", "soil_class": "ZC", "is_existing_building": True, "retrofit_status": "yok", "hazard_score": 70},
        {"building_age": 10, "floor_count": 3, "structural_system": "betonarme_perde", "soil_class": "ZB", "is_existing_building": True, "retrofit_status": "tam", "hazard_score": 50},
        {"building_age": 60, "floor_count": 8, "structural_system": "yigma", "soil_class": "ZE", "is_existing_building": True, "retrofit_status": "yok", "hazard_score": 90},
    ])


class TestEncodeFeatures:
    """Feature encoding testleri."""

    def test_output_is_dataframe(self, sample_df):
        features = encode_features(sample_df)
        assert isinstance(features, pd.DataFrame)

    def test_output_has_rows(self, sample_df):
        features = encode_features(sample_df)
        assert len(features) == len(sample_df)

    def test_base_features_present(self, sample_df):
        features = encode_features(sample_df)
        base_names = get_feature_names()
        for name in base_names:
            assert name in features.columns, f"Eksik feature: {name}"

    def test_all_numeric(self, sample_df):
        features = encode_features(sample_df)
        for col in features.columns:
            assert features[col].dtype in ["float64", "int64", "int32", "float32", "uint8", "bool"], f"{col} sayısal değil: {features[col].dtype}"

    def test_normalized_range(self, sample_df):
        features = encode_features(sample_df)
        assert features["age_normalized"].between(0, 1).all()
        assert features["floors_normalized"].between(0, 1).all()
        assert features["hazard_normalized"].between(0, 1).all()

    def test_one_hot_structural_system(self, sample_df):
        features = encode_features(sample_df)
        sys_cols = [c for c in features.columns if c.startswith("sys_")]
        assert len(sys_cols) > 0

    def test_one_hot_soil_class(self, sample_df):
        features = encode_features(sample_df)
        soil_cols = [c for c in features.columns if c.startswith("soil_Z")]
        assert len(soil_cols) > 0


class TestPrepareTrainingData:
    """Training data hazırlama testleri."""

    def test_returns_tuple(self, sample_df):
        X, y = prepare_training_data(sample_df)
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)

    def test_target_length_matches(self, sample_df):
        X, y = prepare_training_data(sample_df)
        assert len(X) == len(y)

    def test_target_values_valid(self, sample_df):
        X, y = prepare_training_data(sample_df)
        assert y.isin([0, 1, 2]).all()


class TestMissingColumns:
    """Eksik kolon durumu testleri."""

    def test_empty_dataframe(self):
        df = pd.DataFrame({"building_age": [30], "floor_count": [5]})
        features = encode_features(df)
        assert len(features) == 1
        assert "building_age" in features.columns

    def test_minimal_input(self):
        df = pd.DataFrame([{"building_age": 25}])
        features = encode_features(df)
        assert isinstance(features, pd.DataFrame)
        assert len(features) == 1
