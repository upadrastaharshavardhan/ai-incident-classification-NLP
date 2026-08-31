#!/usr/bin/env python
"""Evaluate trained IncidentPredictor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

from src.pipeline.predictor import IncidentPredictor
from src.utils.helpers import load_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--data", default=None)
    args = parser.parse_args()

    cfg = load_config(args.config)
    predictor = IncidentPredictor.load(args.artifacts, args.config)

    data_path = args.data or cfg["paths"]["raw_data"]
    df = pd.read_csv(data_path)
    if len(df) > 600:
        df = df.sample(600, random_state=42)

    results = predictor.predict_batch(df["full_text"].tolist(), top_k_similar=1)
    cat_preds = [r["category"] for r in results]
    pri_preds = [r["priority"] for r in results]

    print("Category Accuracy:", accuracy_score(df["category"], cat_preds))
    print(classification_report(df["category"], cat_preds, digits=3))
    print("\nPriority Accuracy:", accuracy_score(df["priority"], pri_preds))
    print(classification_report(df["priority"], pri_preds, digits=3))


if __name__ == "__main__":
    main()
