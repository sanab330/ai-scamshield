"""
Model Training & Benchmarking Pipeline for AI ScamShield.
Trains and compares Logistic Regression, Naive Bayes, Linear SVC, and Random Forest.
Computes Accuracy, Precision, Recall, F1, ROC-AUC, FPR, FNR, and Confusion Matrices.
Saves the champion model and TF-IDF vectorizer for offline edge inference.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

def run_benchmark():
    dataset_path = "ai/data/training_dataset.csv"
    if not os.path.exists(dataset_path):
        from datasets_loader import generate_augmented_dataset
        df = generate_augmented_dataset(1800)
        df.to_csv(dataset_path, index=False)
    else:
        df = pd.read_csv(dataset_path)

    print(f"Loaded dataset from {dataset_path} with {len(df)} samples.")
    
    # Preprocessing
    X = df["text"].astype(str)
    y = df["label"].astype(int)

    # Stratified 80/20 Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Train split: {len(X_train)} | Test split: {len(X_test)}")

    # TF-IDF Feature Engineering (Unigrams + Bigrams, Sublinear TF)
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
        lowercase=True,
        token_pattern=r"(?u)\b\w+\b|https?://\S+|₹|\$|%"
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print(f"Vocabulary size: {X_train_vec.shape[1]} features.")

    # Candidate Models
    candidate_models = {
        "Logistic Regression": LogisticRegression(
            C=2.0, class_weight="balanced", max_iter=1000, random_state=42
        ),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Calibrated Linear SVC": CalibratedClassifierCV(
            LinearSVC(C=1.0, class_weight="balanced", random_state=42, dual="auto")
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=120, max_depth=25, class_weight="balanced", random_state=42
        ),
    }

    results = {}
    best_f1 = -1.0
    champion_name = None
    champion_model = None

    print("\n" + "=" * 80)
    print(f"{'Model':<26} | {'Accuracy':<8} | {'Precision':<9} | {'Recall':<8} | {'F1':<8} | {'ROC-AUC':<8} | {'FPR':<6} | {'FNR':<6}")
    print("-" * 80)

    for name, model in candidate_models.items():
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        
        # Probabilities for ROC-AUC
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test_vec)[:, 1]
        elif hasattr(model, "decision_function"):
            y_proba = model.decision_function(X_test_vec)
        else:
            y_proba = y_pred

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        roc = float(roc_auc_score(y_test, y_proba))

        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()

        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

        results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(roc, 4),
            "fpr": round(fpr, 4),
            "fnr": round(fnr, 4),
            "confusion_matrix": {
                "tn": int(tn),
                "fp": int(fp),
                "fn": int(fn),
                "tp": int(tp)
            }
        }

        print(f"{name:<26} | {acc:<8.4f} | {prec:<9.4f} | {rec:<8.4f} | {f1:<8.4f} | {roc:<8.4f} | {fpr:<6.4f} | {fnr:<6.4f}")

        # Choose champion based on high Recall + High F1 (catching scams without excessive false alarms)
        score_metric = (rec * 0.6) + (f1 * 0.4) - (fpr * 0.2)
        if score_metric > best_f1:
            best_f1 = score_metric
            champion_name = name
            champion_model = model

    print("=" * 80)
    print(f"\nChampion Model Selected: {champion_name} (Composite Score: {best_f1:.4f})")

    # Serialize Models
    os.makedirs("ai/models", exist_ok=True)
    joblib.dump(champion_model, "ai/models/scam_classifier.joblib")
    joblib.dump(vectorizer, "ai/models/tfidf_vectorizer.joblib")

    # Save Metadata & Benchmark Results
    metadata = {
        "champion_model": champion_name,
        "vocabulary_size": int(X_train_vec.shape[1]),
        "training_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "benchmarks": results
    }

    with open("ai/models/model_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("Saved champion model to ai/models/scam_classifier.joblib")
    print("Saved vectorizer to ai/models/tfidf_vectorizer.joblib")
    print("Saved benchmark metadata to ai/models/model_metadata.json")

    return metadata

if __name__ == "__main__":
    run_benchmark()
