"""Smoke tests for Project 2."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.generator import generate_incident_dataset
from src.data.preprocessing import TicketPreprocessor
from src.models.embeddings import EmbeddingModel
from src.models.classifier import DualClassifier
from src.models.similarity import SimilarityIndex


def test_generator():
    df = generate_incident_dataset(80, seed=1)
    assert len(df) == 80
    assert "category" in df.columns and "priority" in df.columns


def test_preprocessor():
    pre = TicketPreprocessor()
    text = "Title: Test INC-12345\nDescription: user-9999 has issue. Contact admin@co.com"
    cleaned = pre.clean(text)
    assert "INC-12345" not in cleaned
    assert "admin@co.com" not in cleaned


def test_tiny_end_to_end():
    df = generate_incident_dataset(150, seed=3)
    pre = TicketPreprocessor()
    df = pre.transform_df(df)
    embedder = EmbeddingModel(device="cpu")
    X = embedder.encode(df["cleaned_text"].tolist(), batch_size=32, show_progress=False)
    clf = DualClassifier()
    clf.fit(X[:120], df["category"].iloc[:120].tolist(), df["priority"].iloc[:120].tolist())
    preds = clf.predict(X[120:])
    assert len(preds["category"]) == 30
    sim = SimilarityIndex(top_k=3)
    sim.build(X[:120], df.iloc[:120][["incident_id", "title", "category", "priority"]])
    assert len(sim.search(X[120:121])[0]) == 3


if __name__ == "__main__":
    test_generator()
    test_preprocessor()
    test_tiny_end_to_end()
    print("All smoke tests passed.")
