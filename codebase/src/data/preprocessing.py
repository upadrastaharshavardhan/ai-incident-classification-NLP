"""
Preprocessing for IT incident tickets.
"""

from __future__ import annotations

import re
from typing import List

import pandas as pd


class TicketPreprocessor:
    def __init__(
        self,
        max_text_length: int = 1500,
        remove_ticket_ids: bool = True,
        remove_emails: bool = True,
        remove_urls: bool = True,
        remove_timestamps: bool = True,
        extract_key_phrases: bool = False,
        spacy_model: str = "en_core_web_sm",
    ):
        self.max_text_length = max_text_length
        self.remove_ticket_ids = remove_ticket_ids
        self.remove_emails = remove_emails
        self.remove_urls = remove_urls
        self.remove_timestamps = remove_timestamps
        self.extract_key_phrases = extract_key_phrases
        self.spacy_model = spacy_model
        self._nlp = None

    def _load_spacy(self):
        if self._nlp is None and self.extract_key_phrases:
            try:
                import spacy
                self._nlp = spacy.load(self.spacy_model)
            except OSError:
                print(f"[WARN] spaCy model '{self.spacy_model}' not found.")
                self.extract_key_phrases = False

    def clean(self, text: str) -> str:
        if text is None or (isinstance(text, float) and pd.isna(text)):
            return ""
        text = str(text)

        if self.remove_ticket_ids:
            text = re.sub(r"\b(INC|TICKET|REQ|CHG|SR)[-_]?\d+\b", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\buser-\d+\b", "", text, flags=re.IGNORECASE)

        if self.remove_emails:
            text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "", text)

        if self.remove_urls:
            text = re.sub(r"https?://\S+|www\.\S+", "", text)

        if self.remove_timestamps:
            text = re.sub(
                r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?",
                "",
                text,
            )

        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > self.max_text_length:
            text = text[: self.max_text_length]
        return text

    def transform(self, texts: List[str]) -> List[str]:
        return [self.clean(t) for t in texts]

    def transform_df(self, df: pd.DataFrame, text_col: str = "full_text") -> pd.DataFrame:
        df = df.copy()
        df["cleaned_text"] = self.transform(df[text_col].tolist())
        return df
