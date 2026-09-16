import streamlit as st
import pandas as pd
import joblib


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🔮",
    layout="wide"
)


# =========================================================
# LOAD MODEL
# =========================================================

try:

    model = joblib.load(
        "loan_model.pkl"
    )

except Exception as e:

    st.error(
        "Could not load loan_model.pkl"
    )

    st.exception(e)

    st.stop()


# =========================================================
# TITLE
# =========================================================

st.title("🔮 Loan Approval Prediction")

st.write(
    "Enter applicant information to predict loan approval."
)

st.divider()


# =========================================================
# APPLICANT DETAILS
# =========================================================

st.header("Applicant Details")


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
        [
            "Graduate",
            "Not Graduate"
        ]
    )


    self_employed = st.selectbox(
        "Self Employed",
        [
            "No",
            "Yes"
        ]
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

st.divider()


if st.button(
    "🔮 Predict Loan Approval",
    type="primary"
):

    applicant = pd.DataFrame({

        "no_of_dependents":
            [no_of_dependents],

        "education":
            [education],

        "self_employed":
            [self_employed],

        "income_annum":
            [income_annum],

        "loan_amount":
            [loan_amount],

        "loan_term":
            [loan_term],

        "cibil_score":
            [cibil_score],

        "residential_assets_value":
            [residential_assets_value],

        "commercial_assets_value":
            [commercial_assets_value],

        "luxury_assets_value":
            [luxury_assets_value],

        "bank_asset_value":
            [bank_asset_value]
    })


    # =====================================================
    # PREDICTION
    # =====================================================

    try:

        prediction = model.predict(
            applicant
        )[0]


        probability = model.predict_proba(
            applicant
        )[0][1]


    except Exception as e:

        st.error(
            "Prediction failed."
        )

        st.exception(e)

        st.stop()


    # =====================================================
    # RISK LEVEL
    # =====================================================

    if probability >= 0.80:

        risk = "Low Risk"

    elif probability >= 0.60:

        risk = "Medium Risk"

    else:

        risk = "High Risk"


    st.divider()


    # =====================================================
    # RESULT
    # =====================================================

    if prediction == 1:

        st.success(
            "## ✅ LOAN APPROVED"
        )

    else:

        st.error(
            "## ❌ LOAN REJECTED"
        )


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


    st.info(
        "Risk thresholds used here are project-defined "
        "demonstration thresholds, not official banking standards."
    )
