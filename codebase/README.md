# Intelligent IT Incident Classification & Priority Prediction

**Project 2** – Advanced NLP system that classifies IT incidents and predicts priority/severity (and optionally SLA risk) from ticket title + description.

## What it does

Given an incident ticket text, the system predicts:

1. **Incident Category** (Network, Software Bug, Hardware, Security, Access/Identity, Database, Cloud/Infra, Application Performance, Other)
2. **Priority Level** (P1-Critical, P2-High, P3-Medium, P4-Low)
3. **Confidence scores** for both predictions
4. **Similar historical incidents** (for context and suggested handling)

## Key Features

- Dual-head classification (Category + Priority) on shared sentence embeddings
- Realistic synthetic ITSM-style ticket generator
- Advanced text preprocessing for ticket noise
- FAISS similarity search for historical cases
- Gradio interactive demo
- Fully configurable via YAML
- Colab-ready + modular production structure

## Project Structure

```
ai-incident-classification/
├── config/config.yaml
├── src/
│   ├── data/          # generator, preprocessing, dataset
│   ├── models/        # embeddings, dual classifier, similarity
│   ├── pipeline/      # main predictor
│   ├── utils/
│   └── api/           # Gradio UI
├── scripts/           # generate_data, train, evaluate
├── notebooks/         # Colab quickstart
├── artifacts/         # saved models & indexes
└── requirements.txt
```

## Quick Start (Colab)

```bash
!pip install -r requirements.txt
!python -m spacy download en_core_web_sm
!python scripts/generate_data.py --n-samples 4000
!python scripts/train.py
!python -m src.api.gradio_app
```

## Example Prediction

```python
from src.pipeline.predictor import IncidentPredictor

predictor = IncidentPredictor.load("artifacts")

result = predictor.predict(
    title="Cannot access VPN from home",
    description="Multiple users reporting VPN connection timeout since 09:00. Affects remote workforce. Error: Connection timed out after 30s."
)

print(result)
# {
#   "category": "Network",
#   "category_confidence": 0.94,
#   "priority": "P2-High",
#   "priority_confidence": 0.89,
#   "similar_incidents": [...]
# }
```

## Categories (default)

- Network
- Software
- Hardware
- Security
- Access
- Database
- CloudInfra
- Performance
- Other

## Priority Levels

- P1-Critical
- P2-High
- P3-Medium
- P4-Low

## License

MIT
