#!/usr/bin/env python
"""Train the dual classification + similarity pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

from src.data.generator import generate_incident_dataset
from src.data.preprocessing import TicketPreprocessor
from src.data.dataset import IncidentDataset
from src.models.embeddings import EmbeddingModel
from src.models.classifier import DualClassifier
from src.models.similarity import SimilarityIndex
from src.utils.helpers import load_config, ensure_dirs, set_seed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--data", default=None)
    args = parser.parse_args()

    cfg = load_config(args.config)
    set_seed(cfg["data"]["random_seed"])
    ensure_dirs(cfg["paths"]["data_dir"], cfg["paths"]["artifacts_dir"])

    # Data
    data_path = Path(args.data or cfg["paths"]["raw_data"])
    if data_path.exists():
        print(f"Loading {data_path}")
        df = pd.read_csv(data_path)
    else:
        print("Generating synthetic incidents...")
        df = generate_incident_dataset(
            n_samples=cfg["data"]["n_samples"],
            seed=cfg["data"]["random_seed"],
            categories=cfg.get("categories"),
        )
        df.to_csv(data_path, index=False)

    # Preprocess
    pre_cfg = cfg["preprocessing"]
    preprocessor = TicketPreprocessor(
        max_text_length=pre_cfg["max_text_length"],
        remove_ticket_ids=pre_cfg["remove_ticket_ids"],
        remove_emails=pre_cfg["remove_emails"],
        remove_urls=pre_cfg["remove_urls"],
        remove_timestamps=pre_cfg["remove_timestamps"],
    )
    df = preprocessor.transform_df(df)

    dataset = IncidentDataset(df)
    train_df, test_df = dataset.train_test_split(
        test_size=cfg["data"]["test_size"],
        random_state=cfg["data"]["random_seed"],
    )
    print(f"Train: {len(train_df)} | Test: {len(test_df)}")

    # Embeddings
    emb_cfg = cfg["embedding"]
    embedder = EmbeddingModel(
        model_name=emb_cfg["model_name"],
        device=emb_cfg.get("device"),
        normalize=emb_cfg.get("normalize", True),
    )
    print("Encoding...")
    X_train = embedder.encode(train_df["cleaned_text"].tolist(), batch_size=emb_cfg.get("batch_size", 64))
    X_test = embedder.encode(test_df["cleaned_text"].tolist(), batch_size=emb_cfg.get("batch_size", 64))

    # Dual classifier
    clf_cfg = cfg["classifier"]
    classifier = DualClassifier(
        classifier_type=clf_cfg["type"],
        max_iter=clf_cfg.get("max_iter", 1000),
        class_weight=clf_cfg.get("class_weight", "balanced"),
        n_estimators=clf_cfg.get("n_estimators", 200),
        random_state=clf_cfg.get("random_state", 42),
    )
    print("Training dual classifier (category + priority)...")
    classifier.fit(
        X_train,
        train_df["category"].tolist(),
        train_df["priority"].tolist(),
    )

    # Evaluate
    preds = classifier.predict(X_test)
    print("\n=== Category Classification ===")
    print("Accuracy:", accuracy_score(test_df["category"], preds["category"]))
    print(classification_report(test_df["category"], preds["category"], digits=3))

    print("\n=== Priority Classification ===")
    print("Accuracy:", accuracy_score(test_df["priority"], preds["priority"]))
    print(classification_report(test_df["priority"], preds["priority"], digits=3))

    # Confusion matrices
    for name, y_true, y_pred, classes in [
        ("category", test_df["category"], preds["category"], classifier.category_classes_),
        ("priority", test_df["priority"], preds["priority"], classifier.priority_classes_),
    ]:
        cm = confusion_matrix(y_true, y_pred, labels=classes)
        plt.figure(figsize=(9, 7))
        sns.heatmap(cm, annot=True, fmt="d", xticklabels=classes, yticklabels=classes, cmap="Blues")
        plt.title(f"Confusion Matrix – {name.title()}")
        plt.ylabel("True")
        plt.xlabel("Predicted")
        plt.tight_layout()
        path = Path(cfg["paths"]["artifacts_dir"]) / f"cm_{name}.png"
        plt.savefig(path, dpi=120)
        print(f"Saved {path}")
        plt.close()

    # Save classifiers
    classifier.save(
        cfg["paths"]["category_classifier"],
        cfg["paths"]["priority_classifier"],
    )

    # Similarity index
    sim_cfg = cfg["similarity"]
    similarity = SimilarityIndex(metric=sim_cfg["metric"], top_k=sim_cfg["top_k"])
    meta_cols = ["incident_id", "title", "category", "priority"]
    similarity.build(X_train, train_df[meta_cols])
    similarity.save(
        Path(cfg["paths"]["artifacts_dir"]) / "faiss.index",
        Path(cfg["paths"]["artifacts_dir"]) / "metadata.csv",
    )

    print("\n✅ Training complete. Artifacts saved to", cfg["paths"]["artifacts_dir"])


if __name__ == "__main__":
    main()
