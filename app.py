from pathlib import Path
import pickle

import pandas as pd
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "emi_collection_model.pkl"

app = Flask(__name__)

# ---------------------------------------------------------
# Load the trained model bundle
# ---------------------------------------------------------
with MODEL_PATH.open("rb") as file:
    saved_data = pickle.load(file)

model = saved_data["model"]

# These mappings reproduce the mapping used in your
# existing Streamlit application.
# These values match the categories in the dataset used with the
# uploaded trained model.
ACCOUNT_MAP = {
    "Credit": 0,
    "Current": 1,
    "Savings": 2
}

LOAN_MAP = {
    "Car Loan": 0,
    "Home Loan": 1,
    "Personal Loan": 2
}

# Payment status categories present in the training CSV.
PAYMENT_MAP = {
    "Paid": 0,
    "Partially Paid": 1,
    "Missed": 2
}

REGION_MAP = {
    "East": 0,
    "North": 1,
    "South": 2,
    "West": 3
}

FEATURE_COLUMNS = [
    "Account_Type",
    "Loan_Type",
    "Loan_Amount",
    "Outstanding_Amount",
    "EMI_Amount",
    "Payment_Status",
    "Payment_Delay_Days",
    "Region",
    "Customer_Score"
]


def get_cibil_category(customer_score):
    """Return the same CIBIL category used in the Streamlit app."""
    if customer_score <= 500:
        return "High Risk"
    elif customer_score <= 650:
        return "Medium Risk"
    return "Low Risk"


def get_priority(risk):
    return {
        "High Risk": 1,
        "Medium Risk": 2,
        "Low Risk": 3
    }[risk]


def get_recommendations(risk):
    if risk == "High Risk":
        return [
            "Immediate customer follow-up",
            "Assign Priority 1 collection",
            "Increase monitoring frequency"
        ]

    if risk == "Medium Risk":
        return [
            "Schedule customer follow-up",
            "Assign Priority 2 collection",
            "Monitor payment behavior"
        ]

    return [
        "Routine customer follow-up",
        "Assign Priority 3 collection",
        "Continue standard monitoring"
    ]


@app.route("/")
def home():
    return render_template("index.html", title="Smart EMI Collection")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    if request.method == "POST":

        try:
            account_type = request.form["account_type"]
            loan_type = request.form["loan_type"]
            loan_amount = float(request.form["loan_amount"])
            outstanding_amount = float(request.form["outstanding_amount"])
            emi_amount = float(request.form["emi_amount"])
            payment_status = request.form["payment_status"]
            payment_delay_days = int(request.form["payment_delay_days"])
            region = request.form["region"]
            customer_score = int(request.form["customer_score"])

            # -------------------------------------------------
            # Build exactly the same 9-column model input
            # used by your Streamlit application.
            # -------------------------------------------------
            input_data = pd.DataFrame(
                [[
                    ACCOUNT_MAP[account_type],
                    LOAN_MAP[loan_type],
                    loan_amount,
                    outstanding_amount,
                    emi_amount,
                    PAYMENT_MAP[payment_status],
                    payment_delay_days,
                    REGION_MAP[region],
                    customer_score
                ]],
                columns=FEATURE_COLUMNS
            )

            # -------------------------------------------------
            # ML model prediction
            # -------------------------------------------------
            raw_prediction = int(model.predict(input_data)[0])

            # Optional probability/confidence, when supported.
            confidence = None
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_data)[0]
                confidence = round(float(max(probabilities)) * 100, 1)

            # -------------------------------------------------
            # Proper model-based deployment:
            # use the risk_map saved inside the model bundle.
            #
            # The uploaded model contains:
            # 0 -> Low Risk
            # 1 -> Medium Risk
            # 2 -> High Risk
            # -------------------------------------------------
            risk_map = saved_data.get(
                "risk_map",
                {
                    0: "Low Risk",
                    1: "Medium Risk",
                    2: "High Risk"
                }
            )

            risk = risk_map.get(
                raw_prediction,
                "Unknown Risk"
            )

            # Keep your existing CIBIL business rule visible
            # as a separate supporting indicator.
            cibil_category = get_cibil_category(customer_score)

            priority = get_priority(risk)

            return render_template(
                "result.html",
                title="Prediction Result",
                risk=risk,
                cibil_category=cibil_category,
                priority=priority,
                customer_score=customer_score,
                raw_prediction=raw_prediction,
                confidence=confidence,
                account_type=account_type,
                loan_type=loan_type,
                loan_amount=loan_amount,
                outstanding_amount=outstanding_amount,
                emi_amount=emi_amount,
                payment_status=payment_status,
                payment_delay_days=payment_delay_days,
                region=region,
                recommendations=get_recommendations(risk)
            )

        except Exception as error:
            return render_template(
                "prediction.html",
                title="Risk Prediction",
                error=f"Unable to process the prediction: {error}"
            )

    return render_template(
        "prediction.html",
        title="Risk Prediction"
    )


@app.route("/analytics")
def analytics():
    return render_template("analytics.html", title="Analytics")


@app.route("/about")
def about():
    return render_template("about.html", title="About Project")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
