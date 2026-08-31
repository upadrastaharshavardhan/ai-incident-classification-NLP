# Detailed Methodology - Project 2

## 1. Data Generation

The synthetic generator creates realistic ITSM tickets by:

1. Sampling a category uniformly.
2. Selecting a title/description template from a curated set (5 per category).
3. Applying light lexical noise (ticket references, user IDs).
4. Assigning priority via keyword scoring + category boosts + controlled randomness (P1 made rarer).

This yields strong semantic signals while preserving realistic priority imbalance.

## 2. Preprocessing

- Ticket ID patterns: INC-, TICKET-, REQ-, CHG-, SR-
- Email and URL removal
- Timestamp removal
- Length truncation to 1,500 characters

## 3. Shared Embedding + Dual Heads

A single sentence-transformer produces 384-dimensional L2-normalized vectors. Two independent Logistic Regression classifiers (balanced) are trained on the same vectors - one for category, one for priority. This design:

- Shares expensive embedding computation
- Allows independent class weighting and calibration
- Simplifies deployment

## 4. Similarity Index

FAISS IndexFlatIP (cosine via inner product) built on training embeddings. Returns top-k historical tickets with metadata for agent context.

## 5. Metrics

- Classification: Accuracy, macro/weighted Precision, Recall, F1
- Retrieval: MRR@5, Recall@k, Precision@k (relevance = same category)
