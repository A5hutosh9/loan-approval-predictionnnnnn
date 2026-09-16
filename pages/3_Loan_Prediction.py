import streamlit as st
import pandas as pd
import joblib
from openai import OpenAI

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Loan Prediction")

st.markdown(
    """
    Enter applicant information to predict whether the
    loan application is likely to be approved.
    """
)

# ==========================================================
# LOAD MODEL
# ==========================================================

try:
    model = joblib.load("loan_model.pkl")
except Exception as e:
    st.error(f"Could not load loan_model.pkl: {e}")
    st.stop()

# ==========================================================
# APPLICANT INPUT
# ==========================================================

st.header("👤 Applicant Information")

col1, col2, col3 = st.columns(3)

with col1:
    no_of_dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        max_value=20,
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
        value=600000,
        step=10000
    )

with col2:
    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        value=1500000,
        step=10000
    )

    loan_term = st.number_input(
        "Loan Term (Years)",
        min_value=1,
        max_value=50,
        value=15
    )

    cibil_score = st.number_input(
        "CIBIL Score",
        min_value=0,
        max_value=900,
        value=760
    )

    residential_assets_value = st.number_input(
        "Residential Assets Value",
        min_value=0,
        value=2000000,
        step=10000
    )

with col3:
    commercial_assets_value = st.number_input(
        "Commercial Assets Value",
        min_value=0,
        value=500000,
        step=10000
    )

    luxury_assets_value = st.number_input(
        "Luxury Assets Value",
        min_value=0,
        value=300000,
        step=10000
    )

    bank_asset_value = st.number_input(
        "Bank Asset Value",
        min_value=0,
        value=400000,
        step=10000
    )

# ==========================================================
# PREDICT
# ==========================================================

st.markdown("---")

predict_button = st.button(
    "🔮 Predict Loan Status",
    type="primary",
    use_container_width=True
)

if predict_button:

    input_data = pd.DataFrame({
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

    # ------------------------------------------------------
    # ML PREDICTION
    # ------------------------------------------------------

    try:
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    # ------------------------------------------------------
    # RISK LEVEL
    # ------------------------------------------------------

    if probability >= 0.80:
        risk = "Low Risk"
    elif probability >= 0.60:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    prediction_text = (
        "Approved" if prediction == 1
        else "Rejected"
    )

    # ======================================================
    # RESULT
    # ======================================================

    st.header("📋 Prediction Result")

    result1, result2, result3 = st.columns(3)

    with result1:
        if prediction == 1:
            st.success("✅ LOAN APPROVED")
        else:
            st.error("❌ LOAN REJECTED")

    with result2:
        st.metric(
            "Approval Probability",
            f"{probability * 100:.1f}%"
        )

    with result3:
        st.metric(
            "Risk Level",
            risk
        )

    # ======================================================
    # APPLICANT DETAILS
    # ======================================================

    with st.expander("📋 View Applicant Details"):
        st.dataframe(
            input_data,
            use_container_width=True
        )

    # ======================================================
    # AI EXPLANATION
    # ======================================================

    st.markdown("---")
    st.header("🤖 AI Explanation of This Prediction")

    st.caption(
        "The ML model makes the prediction. OpenAI is used only "
        "to explain the prediction in simple language."
    )

    try:
        api_key = st.secrets["OPENAI_API_KEY"]

    except KeyError:
        st.error(
            "OPENAI_API_KEY is missing from Streamlit Secrets."
        )
        st.stop()

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
You are explaining a college machine-learning project called
"Loan Approval Prediction: Bagging vs Boosting".

The trained ML model produced this result:

Prediction: {prediction_text}
Approval probability: {probability * 100:.1f}%
Project risk level: {risk}

Applicant details:
- Number of dependents: {no_of_dependents}
- Education: {education}
- Self employed: {self_employed}
- Annual income: ₹{income_annum:,}
- Loan amount: ₹{loan_amount:,}
- Loan term: {loan_term} years
- CIBIL score: {cibil_score}
- Residential assets: ₹{residential_assets_value:,}
- Commercial assets: ₹{commercial_assets_value:,}
- Luxury assets: ₹{luxury_assets_value:,}
- Bank assets: ₹{bank_asset_value:,}

Write a short explanation for a college project demonstration.

Requirements:
1. Explain the prediction in simple English.
2. Mention important applicant factors visible in the data.
3. Explain what the probability means.
4. Explain the process:
   applicant data -> trained ML model -> probability -> prediction.
5. Do not invent model rules.
6. Do not claim that a feature definitely caused the prediction.
7. Do not describe this as an actual bank decision.
8. Keep it between 100 and 150 words.
"""

        with st.spinner("Generating AI explanation..."):

            response = client.responses.create(
                model="gpt-5.6-luna",
                input=prompt
            )

        st.markdown(response.output_text)

        st.caption(
            "AI-generated explanation for project demonstration. "
            "It does not represent an actual banking decision."
        )

    except Exception as e:
        st.error(
            f"AI explanation could not be generated: {e}"
        )

    # ======================================================
    # HOW IT WORKS
    # ======================================================

    st.markdown("---")
    st.header("⚙️ How This Prediction Works")

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown(
            """
            ### 1️⃣ Input

            Applicant information is entered into the app.
            """
        )

    with step2:
        st.markdown(
            """
            ### 2️⃣ Model

            The trained ML model processes the features.
            """
        )

    with step3:
        st.markdown(
            """
            ### 3️⃣ Probability

            The model calculates the probability of approval.
            """
        )

    with step4:
        st.markdown(
            """
            ### 4️⃣ Prediction

            The probability is converted into the final
            Approved/Rejected prediction.
            """
        )

    # ======================================================
    # RISK EXPLANATION
    # ======================================================

    with st.expander("ℹ️ About the Risk Level"):

        st.markdown(
            """
            The project uses these demonstration thresholds:

            **80% or above** → Low Risk

            **60%–79.9%** → Medium Risk

            **Below 60%** → High Risk

            These thresholds are defined for this project and
            are not official banking standards.
            """
        )
