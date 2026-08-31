"""
Dual-head classifier: Category + Priority.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Union

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


class DualClassifier:
    """Two independent classifiers sharing the same embedding space."""

    def __init__(
        self,
        classifier_type: str = "logistic",
        max_iter: int = 1000,
        class_weight: str = "balanced",
        n_estimators: int = 200,
        random_state: int = 42,
    ):
        self.classifier_type = classifier_type
        self.category_encoder = LabelEncoder()
        self.priority_encoder = LabelEncoder()
        self.category_model = self._build(classifier_type, max_iter, class_weight, n_estimators, random_state)
        self.priority_model = self._build(classifier_type, max_iter, class_weight, n_estimators, random_state)

    def _build(self, clf_type, max_iter, class_weight, n_estimators, random_state):
        if clf_type == "logistic":
            return LogisticRegression(
                max_iter=max_iter,
                class_weight=class_weight,
                random_state=random_state,
                n_jobs=-1,
            )
        elif clf_type == "random_forest":
            return RandomForestClassifier(
                n_estimators=n_estimators,
                class_weight=class_weight,
                random_state=random_state,
                n_jobs=-1,
            )
        raise ValueError(f"Unknown classifier_type: {clf_type}")

    def fit(
        self,
        X: np.ndarray,
        categories: List[str],
        priorities: List[str],
    ) -> "DualClassifier":
        y_cat = self.category_encoder.fit_transform(categories)
        y_pri = self.priority_encoder.fit_transform(priorities)
        self.category_model.fit(X, y_cat)
        self.priority_model.fit(X, y_pri)
        return self

    def predict(self, X: np.ndarray) -> Dict[str, List]:
        cat_pred = self.category_encoder.inverse_transform(self.category_model.predict(X))
        pri_pred = self.priority_encoder.inverse_transform(self.priority_model.predict(X))
        return {
            "category": cat_pred.tolist(),
            "priority": pri_pred.tolist(),
        }

    def predict_proba(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        return {
            "category": self.category_model.predict_proba(X),
            "priority": self.priority_model.predict_proba(X),
        }

    def predict_with_confidence(self, X: np.ndarray) -> List[Dict]:
        cat_proba = self.category_model.predict_proba(X)
        pri_proba = self.priority_model.predict_proba(X)
        cat_idx = np.argmax(cat_proba, axis=1)
        pri_idx = np.argmax(pri_proba, axis=1)

        results = []
        for i in range(len(X)):
            results.append(
                {
                    "category": self.category_encoder.classes_[cat_idx[i]],
                    "category_confidence": float(cat_proba[i, cat_idx[i]]),
                    "priority": self.priority_encoder.classes_[pri_idx[i]],
                    "priority_confidence": float(pri_proba[i, pri_idx[i]]),
                }
            )
        return results

    @property
    def category_classes_(self) -> List[str]:
        return self.category_encoder.classes_.tolist()

    @property
    def priority_classes_(self) -> List[str]:
        return self.priority_encoder.classes_.tolist()

    def save(self, category_path: Union[str, Path], priority_path: Union[str, Path]) -> None:
        Path(category_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "model": self.category_model,
                "encoder": self.category_encoder,
                "type": self.classifier_type,
            },
            category_path,
        )
        joblib.dump(
            {
                "model": self.priority_model,
                "encoder": self.priority_encoder,
                "type": self.classifier_type,
            },
            priority_path,
        )

    @classmethod
    def load(cls, category_path: Union[str, Path], priority_path: Union[str, Path]) -> "DualClassifier":
        cat_data = joblib.load(category_path)
        pri_data = joblib.load(priority_path)
        obj = cls(classifier_type=cat_data["type"])
        obj.category_model = cat_data["model"]
        obj.category_encoder = cat_data["encoder"]
        obj.priority_model = pri_data["model"]
        obj.priority_encoder = pri_data["encoder"]
        return obj
