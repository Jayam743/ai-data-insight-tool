# AI-Powered Data Insight Tool

A lightweight web app that turns a CSV file into:
- verified statistics + charts (computed in Python)
- a plain-English AI summary of the results

The goal is to help non-technical users understand their data quickly, without needing to know data science tools.

---

## Features

### Data Analysis (Deterministic)
- CSV upload
- Column type detection (numeric / categorical / datetime)
- Missing value report
- Descriptive statistics for numeric columns
- Automatic visualizations:
  - histograms for numeric columns
  - bar charts for categorical columns

### AI Explanation Layer
- Generates a natural-language summary based on computed stats (not raw data guessing)
- Reliability/validation checks for key claims (e.g., percent change)
- Displays limitations and warnings (small datasets, heavy missingness, etc.)

---

## Tech Stack
- Python 3.11+
- Streamlit (UI)
- Pandas / NumPy (analysis)
- Matplotlib (charts)
- OpenAI API (explanations)

---

## Setup

### 1) Create and activate a virtual environment
```bash
python -m venv .venv
