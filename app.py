import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Loan Approval Prediction: Bagging vs Boosting",
    page_icon="🏦",
    layout="wide"
)

# Load trained model
model = joblib.load("loan_model.pkl")

# =========================================================
# MAIN TITLE
# =========================================================

st.title("🏦 Loan Approval Prediction: Bagging vs Boosting")
st.write(
    "An ensemble learning based system for predicting loan approval "
    "and comparing Bagging and Boosting techniques."
)

st.divider()

# =========================================================
# BAGGING VS BOOSTING
# =========================================================

st.header("Bagging vs Boosting")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌳 Bagging")
    st.write("• Reduces variance")
    st.write("• Trains multiple models independently")
    st.write("• Combines predictions")
    st.write("• Models: Bagging, Random Forest")

with col2:
    st.subheader("🚀 Boosting")
    st.write("• Reduces bias")
    st.write("• Models are trained sequentially")
    st.write("• Each model focuses on previous errors")
    st.write("• Models: AdaBoost, Gradient Boosting")

st.divider()

# =========================================================
# MODEL COMPARISON
# =========================================================

st.header("Model Performance Comparison")

comparison = pd.DataFrame({
    "Model": [
        "Decision Tree",
        "Bagging",
        "Random Forest",
        "AdaBoost",
        "Gradient Boosting"
    ],
    "Validation Accuracy": [
        0.9782,
        0.9843,
        0.9796,
        0.9590,
        0.9803
    ],
    "Validation F1": [
        0.9825,
        0.9875,
        0.9837,
        0.9669,
        0.9843
    ],
    "Validation ROC-AUC": [
        0.9771,
        0.9975,
        0.9967,
        0.9948,
        0.9981
    ]
})

display_comparison = comparison.copy()

display_comparison["Validation Accuracy"] = (
    display_comparison["Validation Accuracy"] * 100
).round(2).astype(str) + "%"

display_comparison["Validation F1"] = (
    display_comparison["Validation F1"] * 100
).round(2).astype(str) + "%"

display_comparison["Validation ROC-AUC"] = (
    display_comparison["Validation ROC-AUC"] * 100
).round(2).astype(str) + "%"

st.dataframe(
    display_comparison,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Performance values are based on 5-fold stratified cross-validation."
)

st.divider()

# =========================================================
# APPLICANT PREDICTION
# =========================================================

st.header("Loan Approval Prediction")

st.subheader("Applicant Details")

col1, col2 = st.columns(2)

with col1:

    no_of_dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        max_value=10,
        value=2
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["No", "Yes"]
    )

    income_annum = st.number_input(
        "Annual Income",
        min_value=0,
        value=600000
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        value=1500000
    )

    loan_term = st.number_input(
        "Loan Term (years)",
        min_value=1,
        max_value=40,
        value=15
    )

with col2:

    cibil_score = st.number_input(
        "CIBIL Score",
        min_value=0,
        max_value=900,
        value=760
    )

    residential_assets_value = st.number_input(
        "Residential Assets Value",
        min_value=0,
        value=2000000
    )

    commercial_assets_value = st.number_input(
        "Commercial Assets Value",
        min_value=0,
        value=500000
    )

    luxury_assets_value = st.number_input(
        "Luxury Assets Value",
        min_value=0,
        value=300000
    )

    bank_asset_value = st.number_input(
        "Bank Asset Value",
        min_value=0,
        value=400000
    )

# =========================================================
# PREDICTION
# =========================================================

if st.button("Predict Loan Approval", type="primary"):

    applicant = pd.DataFrame({
        "no_of_dependents": [no_of_dependents],
        "education": [education],
        "self_employed": [self_employed],
        "income_annum": [income_annum],
        "loan_amount": [loan_amount],
        "loan_term": [loan_term],
        "cibil_score": [cibil_score],
        "residential_assets_value": [residential_assets_value],
        "commercial_assets_value": [commercial_assets_value],
        "luxury_assets_value": [luxury_assets_value],
        "bank_asset_value": [bank_asset_value]
    })

    prediction = model.predict(applicant)[0]

    probability = model.predict_proba(applicant)[0][1]

    # Risk level
    if probability >= 0.80:
        risk = "Low Risk"
    elif probability >= 0.60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    st.divider()

    # Result
    if prediction == 1:
        st.success("## LOAN APPROVED")
    else:
        st.error("## LOAN REJECTED")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Approval Probability",
            f"{probability * 100:.2f}%"
        )

    with col2:
        st.metric(
            "Risk Level",
            risk
        )
