# Research Package - Project 2
## Intelligent IT Incident Classification & Priority Prediction

This archive contains the complete research paper, experimental results, methodology documentation, data analysis, and the full advanced codebase for Project 2.

---

## Contents

```
research-paper-project2/
├── README.md
├── paper/
│   ├── IT_Incident_Classification_Priority_Prediction_Research_Paper.pdf
│   └── IT_Incident_Classification_Priority_Prediction_Research_Paper.md
├── docs/
│   ├── Methodology_Detailed.md
│   ├── Experimental_Results_Summary.md
│   ├── Data_Analysis_Report.md
│   └── Research_Analysis_and_Discussion.md
├── results/
│   ├── category_metrics.csv
│   ├── priority_metrics.csv
│   └── ablation_study.csv
├── codebase/                    # Full advanced Project 2 source code
│   ├── src/
│   ├── scripts/
│   ├── notebooks/
│   ├── config/
│   └── ...
├── figures/
└── supplementary/
```

---

## Key Reported Metrics

| Task                  | Metric          | Value    |
|-----------------------|-----------------|----------|
| Category Classification | Accuracy      | **95.38%** |
| Category Classification | Macro F1      | **0.953** |
| Priority Classification | Accuracy      | **92.13%** |
| Priority Classification | Macro F1      | **0.918** |
| Retrieval             | MRR@5           | **0.887** |
| Retrieval             | Recall@5        | **0.968** |

---

## Main Research Paper

**Title**: Intelligent IT Incident Classification and Priority Prediction using Natural Language Processing

Includes full methodology, experimental setup, per-class results, ablation study, confusion analysis, latency, discussion, limitations, and reproducibility appendix.

---

## How to Reproduce

```bash
cd codebase
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python scripts/generate_data.py --n-samples 4000 --seed 42
python scripts/train.py
python scripts/evaluate.py
```

---

## Citation

> Intelligent IT Incident Classification and Priority Prediction using Natural Language Processing. Project 2 Research Documentation, August 2026.
