"""
RiskTwin Tahmin Modülü
Eğitilmiş model varsa onu kullanır, yoksa heuristic scoring'e fallback eder.
"""
import os
import pickle
import warnings
from typing import Dict, Optional

import pandas as pd

from src.config import MODELS_DIR
from src.scoring_engine import evaluate_building
from src.feature_engineering import encode_features, get_feature_names


MODEL_PATH = os.path.join(MODELS_DIR, "risk_model.pkl")

# Model cache
_cached_model = None


def _load_model() -> Optional[Dict]:
    """Eğitilmiş modeli yükle (cache ile)."""
    global _cached_model
    if _cached_model is not None:
        return _cached_model

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        with open(MODEL_PATH, "rb") as f:
            _cached_model = pickle.load(f)
        return _cached_model
    except Exception as e:
        warnings.warn(f"Model yükleme hatası: {e}")
        return None


def predict_risk_class(
    hazard_score: float = 70,
    soil_class: str = "ZC",
    building_age: int = 25,
    floor_count: int = 5,
    structural_system: str = "betonarme_cerceve",
    is_existing_building: bool = True,
    retrofit_status: str = "yok",
    use_model: bool = True,
) -> Dict:
    """
    Risk sınıfı tahmini yap.
    Model varsa ML tahmini, yoksa heuristic kullanır.
    """
    # Önce heuristic değerlendirmeyi her durumda yap
    heuristic_result = evaluate_building(
        hazard_score=hazard_score,
        soil_class=soil_class,
        building_age=building_age,
        floor_count=floor_count,
        structural_system=structural_system,
        is_existing_building=is_existing_building,
        retrofit_status=retrofit_status,
    )

    result = {**heuristic_result, "prediction_method": "heuristic"}

    # ML model dene
    if use_model:
        model_data = _load_model()
        if model_data is not None:
            try:
                model = model_data["model"]
                feature_names = model_data["feature_names"]
                class_labels = model_data.get("class_labels", {0: "Düşük", 1: "Orta", 2: "Yüksek"})

                # Feature DataFrame hazırla
                input_df = pd.DataFrame([{
                    "building_age": building_age,
                    "floor_count": floor_count,
                    "hazard_score": hazard_score,
                    "soil_class": soil_class,
                    "structural_system": structural_system,
                    "is_existing_building": is_existing_building,
                    "retrofit_status": retrofit_status,
                }])

                features = encode_features(input_df)
                X = features[[c for c in feature_names if c in features.columns]]

                # Eksik feature'ları doldur
                for col in feature_names:
                    if col not in X.columns:
                        X[col] = 0
                X = X[feature_names]

                prediction = model.predict(X)[0]
                result["ml_risk_class"] = int(prediction)
                result["ml_risk_label"] = class_labels.get(int(prediction), "Bilinmiyor")
                result["prediction_method"] = "ml"
                result["model_name"] = model_data.get("model_name", "unknown")
            except Exception as e:
                warnings.warn(f"ML tahmin hatası, heuristic kullanılıyor: {e}")
                result["prediction_method"] = "heuristic (ml fallback)"

    return result


if __name__ == "__main__":
    # Test
    result = predict_risk_class(
        hazard_score=80, soil_class="ZD", building_age=40,
        floor_count=8, structural_system="yigma",
    )
    print(f"Method: {result['prediction_method']}")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Band: {result['risk_band']['label']}")
    if "ml_risk_label" in result:
        print(f"ML Class: {result['ml_risk_label']}")
