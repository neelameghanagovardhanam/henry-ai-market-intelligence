# 💰 HENRY AI Market Intelligence Platform

## 🧠 Overview

The **HENRY AI Market Intelligence Platform** is an AI-powered analytics dashboard built to help financial advisors identify and target **HENRYs (High Earners, Not Rich Yet)** — individuals with strong incomes but limited wealth accumulation due to debt, cost of living pressures, or low investment participation.

The platform leverages IRS ZIP Code-level tax data to uncover **financial divergence patterns** across geographic regions and generate AI-driven marketing strategies for financial advisors.

---

## 🎯 Business Objective

### 👥 Team 9: The "HENRY Hunters"

We act as financial strategists for millennials.

### 🧩 Core Problem
We aim to identify regions where:
- 💵 Income is increasing (high earners)
- 📉 Wealth accumulation is low
- 💳 Debt levels or cost-of-living pressure is high
- 📊 Investment activity is relatively weak

### 📌 Goal
Find **"financially promising but underserved markets"** for financial advisory services.

---

## 📊 Dataset Information

### 💰 IRS Statistics of Income (ZIP Code Tax Data)

- Source: IRS SOI Tax Stats  
- Link:  
  https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi

### 📌 Dataset Characteristics:
- ZIP Code-level income data
- Tax filings and income distribution
- Historical yearly datasets (e.g., 2021, 2022)
- Includes income brackets, AGI, and tax metrics

### ⚠️ Important Notes:
- No official API is available
- No Python package exists for this dataset
- Data is provided in Excel/CSV format


## App Deployment URL

[Add your deployed Streamlit app link here]

---

## Local Setup Instructions

### Clone the repository

```bash
git clone https://github.com/neelameghanagovardhanam/henry-ai-market-intelligence
cd henry-ai-market-intelligence
```

### Install dependencies using uv

```bash
uv sync
```

### Set environment variable

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
```

### Run the app

```bash
uv run streamlit run app.py
```

---

## Technologies Used

* Python
* Streamlit
* Pandas, NumPy
* Plotly
* OpenAI API
* uv (Python package manager)
