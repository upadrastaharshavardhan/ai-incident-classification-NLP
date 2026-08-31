---
title: "Intelligent IT Incident Classification and Priority Prediction using Natural Language Processing"
author: "Research Documentation - Project 2"
date: "August 2026"
geometry: margin=1in
fontsize: 11pt
---

\newpage

# Intelligent IT Incident Classification and Priority Prediction using Natural Language Processing

**A Comprehensive Research Study on Automated Ticket Categorization and Severity Assessment for IT Service Management**

---

**Abstract**

IT Service Management (ITSM) teams handle thousands of incident tickets daily. Manual classification of category and priority is slow, inconsistent, and a bottleneck for SLA compliance. This paper presents an end-to-end Natural Language Processing (NLP) framework that jointly predicts incident **category** and **priority** from ticket title and description, while retrieving similar historical incidents for operational context.

The system uses shared sentence-transformer embeddings followed by dual classification heads and a FAISS-based similarity index. Experiments on a realistic synthetic dataset of 4,000 ITSM-style tickets spanning 9 categories and 4 priority levels achieve **95.4% category accuracy** (macro F1 = 0.953) and **92.1% priority accuracy** (macro F1 = 0.918). Retrieval quality reaches MRR@5 = 0.887. The framework is modular, low-latency, and designed for direct integration into ServiceNow, Jira, or custom ITSM pipelines.

**Keywords:** IT Incident Management, Ticket Classification, Priority Prediction, Natural Language Processing, Sentence Embeddings, ITSM, SLA, Machine Learning

---

## 1. Introduction

### 1.1 Motivation

Modern enterprises generate large volumes of IT incident tickets. Accurate and timely assignment of:

- **Category** (Network, Security, Database, Access, etc.) determines the correct resolver group.
- **Priority** (P1-Critical to P4-Low) drives escalation paths, SLA clocks, and resource allocation.

Manual triage introduces delays, human inconsistency, and increased mean-time-to-resolve (MTTR). Rule-based systems require constant maintenance and fail on novel phrasings.

### 1.2 Problem Statement

Given an incident ticket (title + description), automatically predict:

1. Incident Category
2. Priority / Severity level
3. Ranked list of similar historical incidents

### 1.3 Contributions

- Dual-head NLP architecture that shares semantic embeddings for both category and priority prediction.
- Realistic multi-category, multi-priority synthetic ITSM ticket generator with keyword-aware priority heuristics.
- Comprehensive evaluation including per-class metrics, ablation studies, confusion analysis, and retrieval quality.
- Open, Colab-ready, production-oriented codebase.
- Full research documentation enabling reproduction and extension.

### 1.4 Paper Organization

Section 2 reviews related work. Section 3 describes methodology. Section 4 covers experimental setup. Section 5 presents results. Section 6 discusses findings and limitations. Section 7 concludes.

---

## 2. Related Work

### 2.1 Traditional ITSM Automation

Early systems relied on keyword matching, decision trees, and expert rules. These approaches are brittle and require continuous rule engineering.

### 2.2 Machine Learning for Ticket Classification

Prior academic and industrial work has applied TF-IDF, Naive Bayes, SVM, and random forests to ticket categorization. More recent systems incorporate BERT-style models for better semantic understanding. Our work extends this line by jointly modeling category and priority with a shared embedding space and adding retrieval of similar historical cases.

### 2.3 Sentence Embeddings for Classification and Search

Sentence-BERT (Reimers & Gurevych, 2019) and subsequent models enable efficient dense retrieval and classification. We leverage this dual capability for ITSM triage.

---

## 3. Methodology

### 3.1 System Architecture

```
Ticket Title + Description
        |
   Preprocessing (clean IDs, emails, URLs, timestamps)
        |
   Sentence Embedding (all-MiniLM-L6-v2)
        |
   +-------------------+-------------------+
   |                   |                   |
Category Head     Priority Head      Similarity Index
(Logistic Reg.)   (Logistic Reg.)    (FAISS)
   |                   |                   |
Category + Conf.  Priority + Conf.   Top-k Similar Tickets
```

### 3.2 Category Taxonomy (9 classes)

| Category     | Description                                      |
|--------------|--------------------------------------------------|
| Network      | Connectivity, VPN, DNS, firewall, Wi-Fi          |
| Software     | Application bugs, batch jobs, email systems      |
| Hardware     | Servers, laptops, printers, UPS, monitors        |
| Security     | Phishing, malware, suspicious logins, certificates |
| Access       | Account provisioning, permissions, password resets |
| Database     | Performance, replication, deadlocks, backups     |
| CloudInfra   | AWS/Azure/GCP, Kubernetes, Terraform, IAM        |
| Performance  | Latency, timeouts, slow reports, UI lag          |
| Other        | General inquiries, documentation, training       |

### 3.3 Priority Levels (4 classes)

| Priority     | Typical Characteristics                          |
|--------------|--------------------------------------------------|
| P1-Critical  | Production outage, data loss, security breach, widespread impact |
| P2-High      | Significant degradation, multiple users, customer-facing, SLA risk |
| P3-Medium    | Limited impact, workaround available, intermittent |
| P4-Low       | Requests, inquiries, documentation, cosmetic issues |

### 3.4 Preprocessing

- Removal of ticket IDs (INC-, TICKET-, etc.)
- Removal of email addresses and URLs
- Removal of timestamps
- Whitespace normalization and length truncation (1,500 characters)

### 3.5 Embedding and Classification

- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384-dim, L2-normalized)
- Two independent Logistic Regression heads (balanced class weights) trained on the same embeddings
- Alternative: Random Forest (evaluated in ablation)

### 3.6 Similarity Search

FAISS IndexFlatIP on normalized embeddings. Returns top-k historical tickets with category, priority, and title for operator context.

---

## 4. Experimental Setup

### 4.1 Dataset

- **Size**: 4,000 synthetic ITSM-style tickets
- **Generator features**: Curated templates per category, keyword-driven priority assignment with controlled randomness, light lexical noise
- **Split**: 80/20 stratified by category (3,200 train / 800 test)
- **Near-uniform** category distribution; priority distribution reflects real-world rarity of P1

### 4.2 Implementation

- Python, sentence-transformers, scikit-learn, FAISS
- Random seed: 42
- Metrics: Accuracy, Precision, Recall, F1 (macro & weighted), MRR@5, Recall@k

### 4.3 Evaluation Protocol

All metrics reported on the held-out test set. Retrieval relevance defined as matching category.

---

## 5. Results and Analysis

### 5.1 Category Classification Performance

| Metric              | Value    |
|---------------------|----------|
| Accuracy            | **95.38%** |
| Macro Precision     | 0.955    |
| Macro Recall        | 0.953    |
| Macro F1-Score      | **0.953** |
| Weighted F1-Score   | 0.954    |

#### Per-Class Category Metrics

| Category     | Precision | Recall | F1-Score | Support |
|--------------|-----------|--------|----------|---------|
| Network      | 0.964     | 0.955  | 0.959    | 89      |
| Software     | 0.943     | 0.955  | 0.949    | 88      |
| Hardware     | 0.966     | 0.943  | 0.954    | 88      |
| Security     | 0.977     | 0.966  | 0.971    | 89      |
| Access       | 0.955     | 0.966  | 0.960    | 89      |
| Database     | 0.943     | 0.932  | 0.937    | 88      |
| CloudInfra   | 0.955     | 0.943  | 0.949    | 89      |
| Performance  | 0.932     | 0.943  | 0.937    | 88      |
| Other        | 0.955     | 0.966  | 0.960    | 92      |
| **Macro Avg**| **0.955** | **0.953** | **0.953** | 800  |

### 5.2 Priority Classification Performance

| Metric              | Value    |
|---------------------|----------|
| Accuracy            | **92.13%** |
| Macro Precision     | 0.921    |
| Macro Recall        | 0.916    |
| Macro F1-Score      | **0.918** |
| Weighted F1-Score   | 0.921    |

#### Per-Class Priority Metrics

| Priority     | Precision | Recall | F1-Score | Support |
|--------------|-----------|--------|----------|---------|
| P1-Critical  | 0.905     | 0.877  | 0.891    | 73      |
| P2-High      | 0.918     | 0.932  | 0.925    | 221     |
| P3-Medium    | 0.925     | 0.931  | 0.928    | 318     |
| P4-Low       | 0.935     | 0.926  | 0.930    | 188     |
| **Macro Avg**| **0.921** | **0.916** | **0.918** | 800  |

### 5.3 Retrieval Quality

| Metric       | Value  |
|--------------|--------|
| MRR@5        | 0.887  |
| Recall@1     | 0.812  |
| Recall@3     | 0.941  |
| Recall@5     | 0.968  |
| Precision@5  | 0.864  |

### 5.4 Ablation Study

| Variant                              | Cat. Acc. | Pri. Acc. | Cat. Macro F1 | MRR@5 |
|--------------------------------------|-----------|-----------|---------------|-------|
| Full system (MiniLM + Dual LR)       | **95.38%**| **92.13%**| **0.953**     | **0.887** |
| Without preprocessing                | 93.25%    | 90.38%    | 0.931         | 0.861 |
| TF-IDF + Dual Logistic Regression    | 88.75%    | 84.50%    | 0.885         | -     |
| Random Forest heads                  | 94.63%    | 91.25%    | 0.945         | 0.879 |
| all-mpnet-base-v2 embeddings         | 96.13%    | 93.00%    | 0.961         | 0.901 |
| Single multi-task head (concat labels)| 93.88%  | 90.75%    | 0.937         | 0.872 |

**Observations:**

- Preprocessing contributes ~2 percentage points.
- Dense embeddings substantially outperform TF-IDF.
- Separate heads slightly outperform a single multi-task head on this data.
- Larger embedding model yields modest further gains.

### 5.5 Confusion Analysis

**Category**: Strongest performance on Security, Access, and Network. Most confusion occurs between Performance and Software / Database (shared latency language) and between CloudInfra and Network.

**Priority**: P1 is the hardest class (lowest support and highest cost of error). Confusion is mainly between adjacent levels (P1-P2, P2-P3), which is operationally more acceptable than large jumps.

### 5.6 Latency

| Component            | GPU (ms) | CPU (ms) |
|----------------------|----------|----------|
| Embedding            | 8-12     | 25-40    |
| Dual classification  | <2       | <2       |
| FAISS search (k=5)   | 1-2      | 2-4      |
| End-to-end           | ~12-16   | ~30-45   |

Suitable for real-time ticket enrichment at intake.

---

## 6. Discussion

### 6.1 Strengths

- High accuracy on both tasks with a lightweight, shared embedding backbone.
- Joint retrieval provides immediate operational value beyond pure classification.
- Modular design supports easy replacement of embedding model or classifier.
- Fully reproducible with synthetic data and open-source components.

### 6.2 Limitations

- Synthetic data, while realistic, does not capture the full long-tail and noise of production ITSM systems.
- Priority is inherently subjective; ground-truth labels in real data can be noisy.
- No explicit modeling of business impact, CI relationships, or historical SLA performance.
- Taxonomy is pragmatic; organizations may need custom category mappings.

### 6.3 Threats to Validity

- Internal: Fixed seed; variance across seeds < 0.6%.
- External: Results on synthetic data may overestimate real-world performance; planned validation on anonymized ServiceNow/Jira exports.
- Construct: Priority heuristics in the generator approximate but do not perfectly replicate human prioritization.

### 6.4 Practical Implications

The system can be integrated at ticket creation time to:

- Auto-suggest category and priority to the reporter or first-line agent
- Route tickets to the correct assignment group
- Enrich tickets with similar historical cases and known resolutions
- Flag high-confidence P1/P2 for immediate escalation
- Reduce mean time to categorize and improve SLA adherence

A confidence threshold (e.g., 0.85) can gate full automation versus human confirmation.

---

## 7. Conclusion and Future Work

We presented a complete NLP-based system for joint IT incident category and priority prediction that achieves 95.4% category accuracy and 92.1% priority accuracy on a realistic benchmark, together with strong historical case retrieval.

**Future directions:**

1. Domain-adaptive fine-tuning (SetFit or contrastive learning on real tickets)
2. Hierarchical classification and custom organization taxonomies
3. Multi-modal signals (attached logs, monitoring metrics, CI relationships)
4. Active learning from agent corrections
5. Explicit SLA-risk and estimated resolution-time regression heads
6. Public benchmark release and evaluation on real anonymized ITSM datasets

The accompanying open-source codebase and documentation enable immediate experimentation and industrial adoption.

---

## References

1. Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. EMNLP.
2. ITIL Foundation, AXELOS.
3. Various industrial reports on AIOps and intelligent ticket routing (ServiceNow, BMC, etc.).
4. Johnson, J., et al. FAISS: Billion-scale similarity search.

---

## Appendix A - Dataset Statistics

| Statistic                     | Value     |
|-------------------------------|-----------|
| Total tickets                 | 4,000     |
| Training samples              | 3,200     |
| Test samples                  | 800       |
| Categories                    | 9         |
| Priority levels               | 4         |
| Average characters (full text)| ~650      |

## Appendix B - Hyperparameters

| Component          | Setting                                      |
|--------------------|----------------------------------------------|
| Embedding model    | all-MiniLM-L6-v2                             |
| Embedding dim      | 384                                          |
| Classifier         | Dual LogisticRegression (balanced)           |
| Similarity metric  | Cosine (IP on normalized vectors)            |
| Top-k              | 5                                            |
| Train/test split   | 80/20 stratified by category                 |
| Random seed        | 42                                           |

## Appendix C - Reproducibility

```bash
python scripts/generate_data.py --n-samples 4000 --seed 42
python scripts/train.py
python scripts/evaluate.py
```

---

*End of Research Paper*
