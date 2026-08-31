# Experimental Results Summary - Project 2

**Dataset**: 4,000 synthetic ITSM tickets | 80/20 stratified split | Seed 42

## Category Classification (Test n=800)

| Metric            | Value    |
|-------------------|----------|
| Accuracy          | 95.38%   |
| Macro F1          | 0.953    |
| Weighted F1       | 0.954    |

## Priority Classification (Test n=800)

| Metric            | Value    |
|-------------------|----------|
| Accuracy          | 92.13%   |
| Macro F1          | 0.918    |
| Weighted F1       | 0.921    |

## Retrieval

| Metric     | Value |
|------------|-------|
| MRR@5      | 0.887 |
| Recall@5   | 0.968 |
| Precision@5| 0.864 |

## Ablation (selected)

| Variant                    | Cat Acc | Pri Acc | Cat F1 |
|----------------------------|---------|---------|--------|
| Full system                | 95.38%  | 92.13%  | 0.953  |
| No preprocessing           | 93.25%  | 90.38%  | 0.931  |
| TF-IDF baseline            | 88.75%  | 84.50%  | 0.885  |
| Random Forest heads        | 94.63%  | 91.25%  | 0.945  |
| mpnet embeddings           | 96.13%  | 93.00%  | 0.961  |

## Latency (approx.)

End-to-end GPU: 12-16 ms | CPU: 30-45 ms
