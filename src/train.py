"""
RiskTwin Model Eğitim Pipeline'ı
Baseline modeller: Logistic Regression, Random Forest, XGBoost (opsiyonel)
Heuristic skorlardan label oluşturarak bootstrap eğitim yapar.
"""
import os
import sys
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import MODELS_DIR
from src.data_ingestion import load_hazard_data, load_building_data
from src.data_processing import clean_building_data, merge_hazard_building
from src.feature_engineering import prepare_training_data, get_feature_names

warnings.filterwarnings("ignore")


def train_models():
    """Ana eğitim fonksiyonu."""
    print("=" * 60)
    print("RiskTwin - Model Eğitim Pipeline'ı")
    print("=" * 60)

    # 1. Veri yükleme
    print("\n[1/5] Veri yükleniyor...")
    hazard_df = load_hazard_data()
    building_df = load_building_data()
    building_df = clean_building_data(building_df)
    merged_df = merge_hazard_building(hazard_df, building_df)
    print(f"  → {len(merged_df)} kayıt yüklendi")

    if len(merged_df) < 5:
        print("UYARI: Yeterli veri yok. En az 5 kayıt gerekli.")
        print("Demo veri ile devam ediliyor...")

    # 2. Feature engineering
    print("\n[2/5] Feature engineering...")
    X, y = prepare_training_data(merged_df)

    # Sadece sayısal feature'ları kullan
    base_features = get_feature_names()
    available_features = [f for f in base_features if f in X.columns]
    X_train_cols = X[available_features]

    print(f"  → {X_train_cols.shape[1]} feature, {len(y)} örnek")
    print(f"  → Sınıf dağılımı: {dict(y.value_counts().sort_index())}")

    # 3. Train/test split
    print("\n[3/5] Train/test split...")
    if len(X_train_cols) >= 6:
        X_train, X_test, y_train, y_test = train_test_split(
            X_train_cols, y, test_size=0.25, random_state=42,
            stratify=y if y.nunique() > 1 and y.value_counts().min() >= 2 else None,
        )
    else:
        # Çok az veri - tüm seti eğitim olarak kullan
        X_train, X_test = X_train_cols, X_train_cols
        y_train, y_test = y, y

    print(f"  → Train: {len(X_train)}, Test: {len(X_test)}")

    # 4. Model eğitimi
    print("\n[4/5] Model eğitimi...")
    models = {}

    # Logistic Regression
    print("  → Logistic Regression eğitiliyor...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_acc = accuracy_score(y_test, lr_pred)
    lr_f1 = f1_score(y_test, lr_pred, average="weighted", zero_division=0)
    models["logistic_regression"] = {"model": lr, "accuracy": lr_acc, "f1": lr_f1}
    print(f"    Accuracy: {lr_acc:.3f}, F1: {lr_f1:.3f}")

    # Random Forest
    print("  → Random Forest eğitiliyor...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    rf_f1 = f1_score(y_test, rf_pred, average="weighted", zero_division=0)
    models["random_forest"] = {"model": rf, "accuracy": rf_acc, "f1": rf_f1}
    print(f"    Accuracy: {rf_acc:.3f}, F1: {rf_f1:.3f}")

    # XGBoost (opsiyonel)
    try:
        from xgboost import XGBClassifier
        print("  → XGBoost eğitiliyor...")
        xgb = XGBClassifier(
            n_estimators=100, max_depth=3, random_state=42,
            use_label_encoder=False, eval_metric="mlogloss",
            verbosity=0,
        )
        xgb.fit(X_train, y_train)
        xgb_pred = xgb.predict(X_test)
        xgb_acc = accuracy_score(y_test, xgb_pred)
        xgb_f1 = f1_score(y_test, xgb_pred, average="weighted", zero_division=0)
        models["xgboost"] = {"model": xgb, "accuracy": xgb_acc, "f1": xgb_f1}
        print(f"    Accuracy: {xgb_acc:.3f}, F1: {xgb_f1:.3f}")
    except Exception:
        print("  → XGBoost kullanılamıyor (libomp eksik olabilir), atlanıyor.")

    # 5. En iyi modeli kaydet
    print("\n[5/5] Model kaydediliyor...")
    # Random Forest tercih et (feature importance için), eşit f1'de
    if "random_forest" in models and models["random_forest"]["f1"] >= max(m["f1"] for m in models.values()) - 0.001:
        best_name = "random_forest"
    else:
        best_name = max(models, key=lambda k: models[k]["f1"])
    best_model = models[best_name]["model"]

    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, "risk_model.pkl")
    metadata = {
        "model": best_model,
        "model_name": best_name,
        "feature_names": available_features,
        "accuracy": models[best_name]["accuracy"],
        "f1": models[best_name]["f1"],
        "n_classes": y.nunique(),
        "class_labels": {0: "Düşük", 1: "Orta", 2: "Yüksek"},
    }

    with open(model_path, "wb") as f:
        pickle.dump(metadata, f)

    print(f"  → En iyi model: {best_name}")
    print(f"  → Kaydedildi: {model_path}")

    # Özet
    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    for name, info in models.items():
        marker = " ← EN İYİ" if name == best_name else ""
        print(f"  {name}: acc={info['accuracy']:.3f}, f1={info['f1']:.3f}{marker}")
    print(f"\nNOT: Bu model heuristic skorlardan bootstrap edilmiştir.")
    print(f"Gerçek etiketli veri ile yeniden eğitim önerilir.")

    return models


if __name__ == "__main__":
    train_models()
