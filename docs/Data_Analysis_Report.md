# Data Analysis Report - Project 2

## Dataset Overview

| Property                    | Value   |
|-----------------------------|---------|
| Total incidents             | 4,000   |
| Categories                  | 9       |
| Priority levels             | 4       |
| Train / Test                | 3,200 / 800 |
| Stratification              | By category |

## Category Distribution (approx.)

Near-uniform across 9 categories (~400-450 each).

## Priority Distribution (characteristic)

| Priority     | Approx. Share | Notes                          |
|--------------|---------------|--------------------------------|
| P1-Critical  | ~9%           | Intentionally rarer            |
| P2-High      | ~28%          |                                |
| P3-Medium    | ~40%          | Largest group                  |
| P4-Low       | ~23%          |                                |

This mirrors real ITSM environments where critical incidents are less frequent.

## Text Characteristics

- Average full_text length ~650 characters
- After cleaning, dominant terms are domain-specific (VPN, database, login, timeout, certificate, pod, etc.)
- Templates provide strong lexical anchors; noise injection tests robustness

## Implications

Because templates are category-specific, even classical methods perform reasonably. The lift from dense embeddings comes from better handling of paraphrases and cross-template generalization, which is essential for real production tickets.
