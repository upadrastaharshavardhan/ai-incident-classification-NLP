"""Dataset utilities for incident data."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


class IncidentDataset:
    def __init__(
        self,
        df: pd.DataFrame,
        text_col: str = "cleaned_text",
        category_col: str = "category",
        priority_col: str = "priority",
    ):
        self.df = df
        self.text_col = text_col
        self.category_col = category_col
        self.priority_col = priority_col

    @classmethod
    def from_csv(cls, path: str | Path, **kwargs) -> "IncidentDataset":
        return cls(pd.read_csv(path), **kwargs)

    def train_test_split(
        self,
        test_size: float = 0.2,
        random_state: int = 42,
        stratify_col: str = "category",
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        strat = self.df[stratify_col] if stratify_col in self.df.columns else None
        train_df, test_df = train_test_split(
            self.df,
            test_size=test_size,
            random_state=random_state,
            stratify=strat,
        )
        return train_df.reset_index(drop=True), test_df.reset_index(drop=True)

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(path, index=False)

    def __len__(self) -> int:
        return len(self.df)
