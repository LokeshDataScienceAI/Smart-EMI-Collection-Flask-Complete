# Smart EMI Collection Prioritization System — Flask Deployment

## Purpose

This project converts the existing Streamlit learning project into an attractive Flask web application.

### Development tools

- Jupyter Notebook: model development/training
- VS Code: Flask + HTML + CSS + JavaScript application
- GitHub: source-code repository
- Render: live deployment

## Important model/UI finding

The uploaded trained model expects these 9 columns:

- Account_Type
- Loan_Type
- Loan_Amount
- Outstanding_Amount
- EMI_Amount
- Payment_Status
- Payment_Delay_Days
- Region
- Customer_Score

The uploaded CSV contains these categorical values:

- Account_Type: Credit, Current, Savings
- Loan_Type: Car Loan, Home Loan, Personal Loan
- Payment_Status: Paid, Partially Paid, Missed
- Region: East, North, South, West

The Flask prediction form therefore uses those training-data categories.

The uploaded model bundle contains a saved `risk_map`:

- 0 → Low Risk
- 1 → Medium Risk
- 2 → High Risk

The Flask app uses that mapping for the primary ML result.

Your original Streamlit application also has a separate CIBIL rule:

- score <= 500 → High Risk
- score 501–650 → Medium Risk
- score > 650 → Low Risk

That CIBIL category is shown separately rather than being silently substituted for the ML model output.

## Local setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Open:

`http://127.0.0.1:5000`

## Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn app:app
```

## Project structure

```text
Smart-EMI-Collection-Flask-Complete/
│
├── app.py
├── requirements.txt
├── Procfile
├── README.md
├── project_manifest.json
│
├── model/
│   └── emi_collection_model.pkl
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── prediction.html
│   ├── result.html
│   ├── analytics.html
│   ├── about.html
│   └── error.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```
