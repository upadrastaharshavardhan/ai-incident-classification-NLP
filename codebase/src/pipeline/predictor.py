"""End-to-end Incident Classification & Priority Prediction pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from src.data.preprocessing import TicketPreprocessor
from src.models.embeddings import EmbeddingModel
from src.models.classifier import DualClassifier
from src.models.similarity import SimilarityIndex


class IncidentPredictor:
    def __init__(
        self,
        embedder: EmbeddingModel,
        classifier: DualClassifier,
        similarity: SimilarityIndex,
        preprocessor: TicketPreprocessor,
    ):
        self.embedder = embedder
        self.classifier = classifier
        self.similarity = similarity
        self.preprocessor = preprocessor

    def predict(
        self,
        title: str = "",
        description: str = "",
        full_text: Optional[str] = None,
        top_k_similar: int = 5,
    ) -> Dict[str, Any]:
        if full_text is None:
            full_text = f"Title: {title}\nDescription: {description}"

        cleaned = self.preprocessor.clean(full_text)
        emb = self.embedder.encode([cleaned], show_progress=False)

        pred = self.classifier.predict_with_confidence(emb)[0]
        similar = self.similarity.search(emb, top_k=top_k_similar)[0]

        return {
            "category": pred["category"],
            "category_confidence": pred["category_confidence"],
            "priority": pred["priority"],
            "priority_confidence": pred["priority_confidence"],
            "similar_incidents": similar,
            "cleaned_input_preview": cleaned[:300] + ("..." if len(cleaned) > 300 else ""),
        }

    def predict_batch(
        self,
        texts: List[str],
        top_k_similar: int = 3,
    ) -> List[Dict[str, Any]]:
        cleaned = self.preprocessor.transform(texts)
        embs = self.embedder.encode(cleaned, show_progress=True)
        preds = self.classifier.predict_with_confidence(embs)
        similars = self.similarity.search(embs, top_k=top_k_similar)

        results = []
        for pred, sim in zip(preds, similars):
            results.append(
                {
                    "category": pred["category"],
                    "category_confidence": pred["category_confidence"],
                    "priority": pred["priority"],
                    "priority_confidence": pred["priority_confidence"],
                    "similar_incidents": sim,
                }
            )
        return results

    @classmethod
    def load(
        cls,
        artifacts_dir: Union[str, Path],
        config_path: Optional[Union[str, Path]] = None,
    ) -> "IncidentPredictor":
        artifacts_dir = Path(artifacts_dir)
        if config_path is None:
            config_path = Path("config/config.yaml")
        with open(config_path) as f:
            cfg = yaml.safe_load(f)

        emb_cfg = cfg.get("embedding", {})
        pre_cfg = cfg.get("preprocessing", {})
        sim_cfg = cfg.get("similarity", {})

        embedder = EmbeddingModel(
            model_name=emb_cfg.get("model_name", "sentence-transformers/all-MiniLM-L6-v2"),
            device=emb_cfg.get("device"),
            normalize=emb_cfg.get("normalize", True),
        )

        classifier = DualClassifier.load(
            artifacts_dir / "category_classifier.joblib",
            artifacts_dir / "priority_classifier.joblib",
        )

        similarity = SimilarityIndex(
            metric=sim_cfg.get("metric", "cosine"),
            top_k=sim_cfg.get("top_k", 5),
        )
        similarity.load(artifacts_dir / "faiss.index", artifacts_dir / "metadata.csv")

        preprocessor = TicketPreprocessor(
            max_text_length=pre_cfg.get("max_text_length", 1500),
            remove_ticket_ids=pre_cfg.get("remove_ticket_ids", True),
            remove_emails=pre_cfg.get("remove_emails", True),
            remove_urls=pre_cfg.get("remove_urls", True),
            remove_timestamps=pre_cfg.get("remove_timestamps", True),
        )

        return cls(embedder, classifier, similarity, preprocessor)
