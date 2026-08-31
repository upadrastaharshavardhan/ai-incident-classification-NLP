"""FAISS / sklearn similarity index for historical incidents."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import pandas as pd

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    from sklearn.neighbors import NearestNeighbors


class SimilarityIndex:
    def __init__(self, metric: str = "cosine", top_k: int = 5):
        self.metric = metric
        self.top_k = top_k
        self.index = None
        self.metadata: Optional[pd.DataFrame] = None
        self._use_faiss = FAISS_AVAILABLE

    def build(self, embeddings: np.ndarray, metadata: pd.DataFrame) -> "SimilarityIndex":
        assert len(embeddings) == len(metadata)
        self.metadata = metadata.reset_index(drop=True)
        emb = np.ascontiguousarray(embeddings.astype(np.float32))

        if self._use_faiss:
            dim = emb.shape[1]
            self.index = faiss.IndexFlatIP(dim) if self.metric == "cosine" else faiss.IndexFlatL2(dim)
            self.index.add(emb)
        else:
            metric = "cosine" if self.metric == "cosine" else "euclidean"
            self.index = NearestNeighbors(n_neighbors=self.top_k, metric=metric)
            self.index.fit(emb)
        return self

    def search(self, query_embeddings: np.ndarray, top_k: Optional[int] = None) -> List[List[dict]]:
        k = top_k or self.top_k
        query = np.ascontiguousarray(query_embeddings.astype(np.float32))
        results = []

        if self._use_faiss:
            scores, indices = self.index.search(query, k)
            for score_row, idx_row in zip(scores, indices):
                row = []
                for score, idx in zip(score_row, idx_row):
                    if idx < 0:
                        continue
                    meta = self.metadata.iloc[idx]
                    sim = float(score) if self.metric == "cosine" else float(1.0 / (1.0 + score))
                    row.append(
                        {
                            "similarity": sim,
                            "incident_id": meta.get("incident_id", ""),
                            "category": meta.get("category", ""),
                            "priority": meta.get("priority", ""),
                            "title": str(meta.get("title", ""))[:100],
                        }
                    )
                results.append(row)
        else:
            distances, indices = self.index.kneighbors(query, n_neighbors=k)
            for dist_row, idx_row in zip(distances, indices):
                row = []
                for dist, idx in zip(dist_row, idx_row):
                    meta = self.metadata.iloc[idx]
                    sim = float(1.0 - dist) if self.metric == "cosine" else float(1.0 / (1.0 + dist))
                    row.append(
                        {
                            "similarity": sim,
                            "incident_id": meta.get("incident_id", ""),
                            "category": meta.get("category", ""),
                            "priority": meta.get("priority", ""),
                            "title": str(meta.get("title", ""))[:100],
                        }
                    )
                results.append(row)
        return results

    def save(self, index_path: Union[str, Path], metadata_path: Union[str, Path]) -> None:
        Path(index_path).parent.mkdir(parents=True, exist_ok=True)
        if self._use_faiss:
            faiss.write_index(self.index, str(index_path))
        else:
            import joblib
            joblib.dump(self.index, str(index_path) + ".sklearn")
        self.metadata.to_csv(metadata_path, index=False)

    def load(self, index_path: Union[str, Path], metadata_path: Union[str, Path]) -> "SimilarityIndex":
        self.metadata = pd.read_csv(metadata_path)
        if self._use_faiss and Path(index_path).exists():
            self.index = faiss.read_index(str(index_path))
        else:
            import joblib
            self.index = joblib.load(str(index_path) + ".sklearn")
            self._use_faiss = False
        return self
