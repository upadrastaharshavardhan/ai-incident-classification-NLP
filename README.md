# 🧠 Intelligent IT Incident Classification & Priority Prediction

### Research Project 02 · NLP · Machine Learning · IT Operations · Incident Management

<p align="center">

**Transforming unstructured IT incident descriptions into actionable classifications, priority predictions, and intelligent retrieval.**

</p>

<p align="center">

[![Project](https://img.shields.io/badge/Project-02-6C63FF?style=for-the-badge)](https://github.com/upadrastaharshavardhan/ai-incident-classification-NLP)
[![NLP](https://img.shields.io/badge/NLP-Natural%20Language%20Processing-00B894?style=for-the-badge)](https://github.com/upadrastaharshavardhan/ai-incident-classification-NLP)
[![Machine Learning](https://img.shields.io/badge/ML-Machine%20Learning-F39C12?style=for-the-badge)](https://github.com/upadrastaharshavardhan/ai-incident-classification-NLP)
[![License](https://img.shields.io/badge/License-MIT-E74C3C?style=for-the-badge)](LICENSE)

</p>

---

## 🚀 Project Overview

IT support and operations teams process thousands of incident tickets containing unstructured descriptions such as:

> *"Users are unable to access the payment portal after the latest deployment."*

Manually understanding, categorizing, prioritizing, and retrieving similar incidents is time-consuming and inconsistent.

This research project investigates an **NLP-driven intelligent incident analysis pipeline** capable of converting natural-language incident descriptions into structured operational intelligence.

### The system focuses on three core capabilities:

```text
                 ┌──────────────────────────┐
                 │   Raw IT Incident Text   │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │     NLP Processing       │
                 │ Cleaning • Features      │
                 │ Representation • Context │
                 └────────────┬─────────────┘
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │   Category   │ │   Priority   │ │  Retrieval   │
      │ Classification│ │ Prediction   │ │ Similarity   │
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                 ┌──────────────────────────┐
                 │ Actionable IT Intelligence│
                 └──────────────────────────┘
```

---

# 🎯 Research Objectives

The project investigates whether natural-language processing and machine-learning techniques can reliably support IT incident management.

### Primary objectives

* **Automatically classify** incoming incidents into meaningful categories.
* **Predict incident priority** from textual evidence and contextual signals.
* **Retrieve similar historical incidents** for faster investigation.
* Analyze model performance at both aggregate and per-class levels.
* Evaluate the contribution of individual system components through ablation experiments.
* Provide a reproducible research and experimentation pipeline.

---

# 📊 Reported Results

The current research package reports strong performance across classification and retrieval tasks.

| Task                        |   Metric |     Result |
| --------------------------- | -------: | ---------: |
| 🏷️ Category Classification | Accuracy | **95.38%** |
| 🏷️ Category Classification | Macro F1 |  **0.953** |
| 🚨 Priority Classification  | Accuracy | **92.13%** |
| 🚨 Priority Classification  | Macro F1 |  **0.918** |
| 🔎 Incident Retrieval       |    MRR@5 |  **0.887** |
| 🔎 Incident Retrieval       | Recall@5 |  **0.968** |

### What these numbers mean

**95.38% category accuracy**

The classification pipeline correctly identifies the incident category for the large majority of evaluated incidents.

**0.953 Macro F1**

The high macro-F1 score indicates that performance is not being measured only on the most common classes.

**92.13% priority accuracy**

The priority model predicts operational urgency with high overall accuracy.

**0.887 MRR@5**

Relevant historical incidents tend to appear near the top of the retrieved results.

**0.968 Recall@5**

The retrieval system successfully surfaces relevant incidents within the top five results in most evaluated cases.

> **Research note:** Reported metrics correspond to the current research package and should be interpreted together with the methodology, dataset construction, evaluation protocol, and limitations documented in the repository.

---

# 🧪 Research Pipeline

The project follows a complete experimentation lifecycle:

```text
Incident Data
     │
     ▼
Data Generation / Collection
     │
     ▼
Data Cleaning & Validation
     │
     ▼
Exploratory Data Analysis
     │
     ▼
NLP Preprocessing
     │
     ▼
Feature / Representation Engineering
     │
     ├───────────────┐
     ▼               ▼
Category Model   Priority Model
     │               │
     └───────┬───────┘
             ▼
     Similarity / Retrieval
             │
             ▼
      Model Evaluation
             │
             ▼
      Ablation Analysis
             │
             ▼
       Research Findings
```

---

# 🧠 Core Capabilities

## 1. Incident Category Classification

The system analyzes incident descriptions and predicts the most likely operational category.

Potential applications include:

* Application incidents
* Infrastructure failures
* Database issues
* Network problems
* Authentication failures
* Service availability incidents
* Configuration-related issues

The exact classes and experimental definitions are documented in the research artifacts.

---

## 2. Priority Prediction

Incident priority is predicted from the available textual and contextual information.

This can support:

* Faster triage
* Consistent prioritization
* Queue optimization
* Escalation workflows
* SLA-aware operations
* Reduced manual classification effort

---

## 3. Similar Incident Retrieval

The retrieval component searches historical incidents to identify semantically related cases.

This enables an engineer to ask:

> **"Have we seen something similar before?"**

and quickly obtain relevant historical incidents.

This can help engineers discover:

* Previous resolutions
* Related incidents
* Recurring failure patterns
* Similar affected services
* Historical operational context

---

# 🏗️ Repository Architecture

```text
ai-incident-classification-NLP/
│
├── 📄 README.md
├── 📄 LICENSE
│
├── 📁 paper/
│   ├── Research_Paper.pdf
│   └── Research_Paper.md
│
├── 📁 docs/
│   ├── Methodology_Detailed.md
│   ├── Experimental_Results_Summary.md
│   ├── Data_Analysis_Report.md
│   └── Research_Analysis_and_Discussion.md
│
├── 📁 results/
│   ├── category_metrics.csv
│   ├── priority_metrics.csv
│   └── ablation_study.csv
│
├── 📁 codebase/
│   ├── src/
│   ├── scripts/
│   ├── notebooks/
│   ├── config/
│   └── requirements.txt
│
├── 📁 figures/
│
└── 📁 supplementary/
```

---

# 📚 Research Documentation

The repository separates implementation from research evidence.

| Resource                | Purpose                                  |
| ----------------------- | ---------------------------------------- |
| 📄 Research Paper       | Complete academic research document      |
| 🧪 Methodology          | Detailed experimental methodology        |
| 📊 Experimental Results | Consolidated experiment findings         |
| 🔍 Data Analysis        | Dataset and statistical analysis         |
| 💬 Research Discussion  | Interpretation, limitations and findings |
| 📈 Metrics CSV          | Machine-readable evaluation results      |
| 🧬 Ablation Study       | Component contribution analysis          |
| 💻 Codebase             | Reproducible implementation              |

---

# 🔬 Experimental Analysis

The research package includes more than a single accuracy number.

Evaluation covers:

### Classification

* Accuracy
* Macro F1
* Per-class performance
* Confusion analysis

### Priority Prediction

* Accuracy
* Macro F1
* Class-level behavior
* Error analysis

### Retrieval

* MRR@5
* Recall@5

### Model Investigation

* Ablation study
* Component comparison
* Error analysis
* Latency considerations

This makes the project suitable for examining both **model performance** and **system behavior**.

---

# ⚙️ Reproducibility

## Requirements

Recommended environment:

```text
Python 3.x
pip
spaCy
scikit-learn
NumPy
Pandas
```

The complete dependency configuration is available inside the `codebase` directory.

---

## 🔧 Installation

Clone the repository:

```bash
git clone https://github.com/upadrastaharshavardhan/ai-incident-classification-NLP.git
```

Enter the project:

```bash
cd ai-incident-classification-NLP/codebase
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the required spaCy language model:

```bash
python -m spacy download en_core_web_sm
```

---

# ▶️ Run the Research Pipeline

### Step 1 — Generate / prepare experimental data

```bash
python scripts/generate_data.py --n-samples 4000 --seed 42
```

### Step 2 — Train the models

```bash
python scripts/train.py
```

### Step 3 — Evaluate

```bash
python scripts/evaluate.py
```

The generated outputs can then be compared against the research results documented in the repository.

---

# 🧬 Ablation Study

A major research component is the **ablation study**.

Instead of asking only:

> "How accurate is the final system?"

the study investigates:

> "Which components actually contribute to the final performance?"

Conceptually:

```text
Full System
    │
    ├── Remove Component A ──► Measure Δ Performance
    │
    ├── Remove Component B ──► Measure Δ Performance
    │
    ├── Remove Component C ──► Measure Δ Performance
    │
    └── Baseline ─────────────► Compare
```

The detailed results are available in:

```text
results/ablation_study.csv
```

---

# 📈 Results Files

### Category Metrics

```text
results/category_metrics.csv
```

Contains classification performance information.

### Priority Metrics

```text
results/priority_metrics.csv
```

Contains priority prediction evaluation results.

### Ablation Study

```text
results/ablation_study.csv
```

Contains experimental comparisons used to understand component contribution.

---

# 📄 Research Paper

### Title

**Intelligent IT Incident Classification and Priority Prediction using Natural Language Processing**

The paper includes:

* Problem formulation
* Research motivation
* Related methodology
* Dataset analysis
* NLP pipeline
* Experimental setup
* Classification experiments
* Priority prediction
* Retrieval evaluation
* Per-class results
* Confusion analysis
* Ablation study
* Latency analysis
* Discussion
* Limitations
* Reproducibility information

---

# 💡 Why This Research Matters

Modern IT environments generate enormous volumes of operational text:

```text
Tickets
Alerts
Incident descriptions
Service requests
Error messages
Support conversations
Operational notes
```

Much of this information remains unstructured.

An intelligent incident analysis system can act as a bridge:

```text
Unstructured IT Data
        ↓
     NLP / ML
        ↓
Structured Intelligence
        ↓
Faster Triage
        ↓
Better Prioritization
        ↓
Faster Investigation
```

---

# 👥 Potential Beneficiaries

### 🧑‍💻 IT Support Engineers

Reduce repetitive manual ticket classification.

### 🚨 Incident Managers

Identify high-priority incidents faster.

### 🔧 DevOps / SRE Teams

Use historical incidents to accelerate troubleshooting.

### 🏢 Enterprise IT Operations

Improve consistency across large incident volumes.

### 🔬 Researchers

Use the repository as a reproducible NLP/ITSM research package.

### 🎓 Students

Study the complete lifecycle from data preparation to evaluation.

---

# ⚠️ Limitations

Research results should not automatically be interpreted as production-ready performance.

Potential limitations include:

* Dataset characteristics may differ from real enterprise incident streams.
* Synthetic or curated data may not fully represent production noise.
* Domain-specific terminology can affect generalization.
* Priority labels may vary between organizations.
* Historical retrieval quality depends on the available incident corpus.
* Real-world deployment requires additional monitoring, governance, and validation.

These limitations are discussed in greater detail within the research documentation.

---

# 🔮 Future Research

Potential extensions include:

```text
                    Current System
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          NLP/ML      Retrieval   Evaluation
             │           │
             └─────┬─────┘
                   ▼
             Future System
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
   LLM-based    RAG-based    Agentic IT
   reasoning    incident     operations
                analysis
       │           │            │
       └───────────┼────────────┘
                   ▼
          Autonomous Incident
             Intelligence
```

Future work could investigate:

* Transformer-based architectures
* Domain-adapted language models
* LLM-assisted incident reasoning
* Retrieval-Augmented Generation
* Explainable predictions
* Multi-modal incident analysis
* Online learning
* Human-in-the-loop triage
* Agentic incident management
* Integration with ITSM platforms
* Production-scale monitoring

---

# 🔗 Project Resources

**Repository**

https://github.com/upadrastaharshavardhan/ai-incident-classification-NLP

**Research Package**

```text
paper/       → Research paper
docs/        → Research documentation
results/     → Experimental results
codebase/    → Implementation
figures/     → Research visualizations
supplementary/ → Additional material
```

---

# 📖 Citation

If you reference this work in academic or technical material:

```text
Upadrasta Harsha Vardhan.
"Intelligent IT Incident Classification and Priority Prediction
using Natural Language Processing."
Project 2 Research Documentation, August 2026.
```

---

# 📜 License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

<p align="center">

### 🧠 From Incident Text → Intelligent Classification → Priority → Retrieval

**Research Project 02**

</p>

<p align="center">

⭐ If this research is useful, consider starring the repository.

</p>
