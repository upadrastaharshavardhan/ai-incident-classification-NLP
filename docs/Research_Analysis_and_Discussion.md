# Research Analysis and Discussion - Project 2

## Why Dual Heads Work Well

Category and priority are related but not identical tasks. A shared embedding captures the semantic content of the ticket; separate linear heads allow each task to learn its own decision boundary and class weighting. This is simpler and often more effective than a single multi-task head when label spaces differ in cardinality and imbalance.

## Priority is Harder than Category

Priority prediction accuracy (92.1%) is lower than category accuracy (95.4%). Reasons:

- Priority is more subjective and context-dependent.
- Adjacent priority levels share vocabulary.
- P1 has lower support, making it statistically harder.

Operationally, confusing P2 with P3 is far less costly than confusing Network with Security; the observed error patterns are therefore acceptable.

## Practical Value of Retrieval

Even when classification confidence is moderate, the similar-ticket list often surfaces the correct historical resolution path. This makes the system useful as an assistant even before full automation confidence thresholds are met.

## Comparison with Classical Baselines

TF-IDF dual classifiers lag by 6-8 points. The gap is expected to widen on real, noisier, longer-tail production data.

## Deployment Recommendations

1. Start with high-confidence auto-suggestions (threshold 0.85-0.90).
2. Log agent overrides for continuous improvement / active learning.
3. Map predicted categories to existing assignment groups via a simple configuration table.
4. Use similar-incident retrieval to power a "Related tickets" panel in the ITSM UI.

## Limitations and Next Research Steps

- Validate on real anonymized ServiceNow / Jira datasets.
- Add explicit business-impact and CI-relationship features.
- Explore hierarchical category models and organization-specific taxonomies.
- Add regression heads for estimated resolution time and SLA-breach probability.
