import os

import joblib
import pandas as pd
import streamlit as st
from openai import OpenAI


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🔮",
    layout="wide"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("🔮 Loan Prediction")

st.markdown(
    """
    Enter applicant information to predict whether the loan
    application is likely to be approved.
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
# FUNCTION: GET TOP MODEL FEATURES
# ==========================================================

def get_top_features(model, top_n=5):
    """
    Try to extract the most important features from the
    trained pipeline/model.

    Returns a list of (feature, importance).
    """

    try:
        # Pipeline
        if hasattr(model, "named_steps"):

            preprocessor = model.named_steps.get("preprocessor")
            trained_model = model.named_steps.get("model")

            if (
                preprocessor is not None
                and trained_model is not None
                and hasattr(trained_model, "feature_importances_")
            ):

                feature_names = (
                    preprocessor.get_feature_names_out()
                )

                importances = (
                    trained_model.feature_importances_
                )

                feature_df = pd.DataFrame({
                    "Feature": feature_names,
                    "Importance": importances
                })

                feature_df = feature_df.sort_values(
                    "Importance",
                    ascending=False
                ).head(top_n)

                clean_features = []

                for _, row in feature_df.iterrows():

                    feature_name = str(row["Feature"])

                    feature_name = (
                        feature_name
                        .replace("num__", "")
                        .replace("cat__", "")
                        .replace("numeric__", "")
                        .replace("categorical__", "")
                    )

                    clean_features.append(
                        (
                            feature_name,
                            float(row["Importance"])
                        )
                    )

                return clean_features

        # Direct model
        if hasattr(model, "feature_importances_"):

            importances = model.feature_importances_

            return [
                (
                    f"Feature {i + 1}",
                    float(value)
                )
                for i, value in
                enumerate(importances[:top_n])
            ]

    except Exception:
        pass

    return []


# ==========================================================
# APPLICANT INPUT
# ==========================================================

st.header("👤 Applicant Information")

col1, col2, col3 = st.columns(3)


# ==========================================================
# COLUMN 1
# ==========================================================

with col1:

    no_of_dependents = st.number_input(
        "Number of Dependents",
        min_value=0,
        max_value=20,
        value=2,
        step=1
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
        value=600000,
        step=10000
    )


# ==========================================================
# COLUMN 2
# ==========================================================

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
        value=15,
        step=1
    )

    cibil_score = st.number_input(
        "CIBIL Score",
        min_value=0,
        max_value=900,
        value=760,
        step=1
    )

    residential_assets_value = st.number_input(
        "Residential Assets Value",
        min_value=0,
        value=2000000,
        step=10000
    )


# ==========================================================
# COLUMN 3
# ==========================================================

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
# PREDICT BUTTON
# ==========================================================

st.markdown("---")

predict_button = st.button(
    "🔮 Predict Loan Status",
    type="primary",
    use_container_width=True
)


# ==========================================================
# RUN PREDICTION
# ==========================================================

if predict_button:

    # ------------------------------------------------------
    # CREATE INPUT DATAFRAME
    # ------------------------------------------------------

    input_data = pd.DataFrame({

        "no_of_dependents": [
            no_of_dependents
        ],

        "education": [
            education
        ],

        "self_employed": [
            self_employed
        ],

        "income_annum": [
            income_annum
        ],

        "loan_amount": [
            loan_amount
        ],

        "loan_term": [
            loan_term
        ],

        "cibil_score": [
            cibil_score
        ],

        "residential_assets_value": [
            residential_assets_value
        ],

        "commercial_assets_value": [
            commercial_assets_value
        ],

        "luxury_assets_value": [
            luxury_assets_value
        ],

        "bank_asset_value": [
            bank_asset_value
        ]
    })


    # ------------------------------------------------------
    # MODEL PREDICTION
    # ------------------------------------------------------

    try:

        prediction = model.predict(
            input_data
        )[0]

        probabilities = model.predict_proba(
            input_data
        )[0]

        approval_probability = float(
            probabilities[1]
        )

        rejection_probability = float(
            probabilities[0]
        )

    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )

        st.stop()


    # ======================================================
    # RESULT
    # ======================================================

    if prediction == 1:

        prediction_text = "Approved"

    else:

        prediction_text = "Rejected"


    # ======================================================
    # RISK LEVEL
    # ======================================================

    if approval_probability >= 0.80:

        risk = "Low Risk"

    elif approval_probability >= 0.60:

        risk = "Medium Risk"

    else:

        risk = "High Risk"


    # ======================================================
    # DISPLAY RESULT
    # ======================================================

    st.header("📋 Prediction Result")

    result_col1, result_col2, result_col3 = st.columns(3)


    with result_col1:

        if prediction == 1:

            st.success(
                "✅ LOAN APPROVED"
            )

        else:

            st.error(
                "❌ LOAN REJECTED"
            )


    with result_col2:

        st.metric(
            "Approval Probability",
            f"{approval_probability * 100:.1f}%"
        )


    with result_col3:

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
    # MODEL FEATURE IMPORTANCE
    # ======================================================

    top_features = get_top_features(
        model,
        top_n=5
    )


    # ======================================================
    # AI EXPLANATION
    # ======================================================

    st.markdown("---")

    st.header("🤖 AI Explanation of This Prediction")

    st.caption(
        "The machine-learning model makes the prediction. "
        "OpenAI is used only to explain the result in simple language."
    )


    # ------------------------------------------------------
    # GET API KEY
    # ------------------------------------------------------

    api_key = None

    # Streamlit Cloud secret
    try:

        api_key = st.secrets.get(
            "OPENAI_API_KEY"
        )

    except Exception:

        api_key = None


    # Local environment variable fallback
    if not api_key:

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )


    # ------------------------------------------------------
    # CHECK API KEY
    # ------------------------------------------------------

    if not api_key:

        st.warning(
            """
            OpenAI API key is not configured.

            Add this to Streamlit Secrets:

            OPENAI_API_KEY = "your-new-api-key"
            """
        )

    else:

        try:

            client = OpenAI(
                api_key=api_key.strip()
            )


            # ------------------------------------------------
            # TOP FEATURE TEXT
            # ------------------------------------------------

            if top_features:

                feature_text = "\n".join(
                    [
                        f"- {name}: {importance:.4f}"
                        for name, importance
                        in top_features
                    ]
                )

            else:

                feature_text = (
                    "Feature importance was not available."
                )


            # ------------------------------------------------
            # AI PROMPT
            # ------------------------------------------------

            prompt = f"""
You are explaining a college machine-learning project.

Project:
Loan Approval Prediction: Bagging vs Boosting

The trained machine-learning model has already made the
decision. You must NOT make a new loan decision.

MODEL RESULT
------------
Prediction: {prediction_text}
Approval probability: {approval_probability * 100:.1f}%
Rejection probability: {rejection_probability * 100:.1f}%
Project risk level: {risk}

APPLICANT INFORMATION
---------------------
Number of dependents: {no_of_dependents}
Education: {education}
Self employed: {self_employed}
Annual income: ₹{income_annum:,}
Loan amount: ₹{loan_amount:,}
Loan term: {loan_term} years
CIBIL score: {cibil_score}
Residential assets: ₹{residential_assets_value:,}
Commercial assets: ₹{commercial_assets_value:,}
Luxury assets: ₹{luxury_assets_value:,}
Bank assets: ₹{bank_asset_value:,}

TOP MODEL FEATURE IMPORTANCES
-----------------------------
{feature_text}

Explain the result for a college project demonstration.

Instructions:

1. Start with one clear sentence stating what the model predicted.
2. Explain the approval probability in simple language.
3. Mention important applicant factors such as CIBIL score,
   loan amount, loan term, income, or assets where relevant.
4. If feature importance is supplied, use it as model-level
   evidence, but do not say that a feature alone caused the result.
5. Briefly explain the workflow:
   applicant inputs → preprocessing → trained model →
   prediction probability → final prediction.
6. Clearly say that this is a machine-learning project prediction,
   not a real bank lending decision.
7. Do not invent rules, policies, or banking standards.
8. Keep the explanation around 120 words.
9. Use simple English suitable for a college presentation.
"""


            # ------------------------------------------------
            # OPENAI CALL
            # ------------------------------------------------

            with st.spinner(
                "Generating AI explanation..."
            ):

                response = client.responses.create(

                    model="gpt-5.6-luna",

                    input=prompt
                )


            # ------------------------------------------------
            # DISPLAY RESPONSE
            # ------------------------------------------------

            explanation = response.output_text.strip()


            if explanation:

                st.markdown(
                    explanation
                )

            else:

                st.warning(
                    "OpenAI returned an empty explanation."
                )


            # ------------------------------------------------
            # DISCLAIMER
            # ------------------------------------------------

            st.caption(
                "AI-generated explanation for project "
                "demonstration only. It does not represent "
                "an actual banking decision."
            )


        except Exception as e:

            st.error(
                f"AI explanation could not be generated: {e}"
            )


    # ======================================================
    # HOW THE SYSTEM WORKS
    # ======================================================

    st.markdown("---")

    st.header("⚙️ How This Prediction Works")

    step1, step2, step3, step4 = st.columns(4)


    with step1:

        st.markdown(
            """
            ### 1️⃣ Input

            Applicant information is entered into
            the Streamlit application.
            """
        )


    with step2:

        st.markdown(
            """
            ### 2️⃣ Preprocessing

            Numerical and categorical information is
            prepared in the same way as during training.
            """
        )


    with step3:

        st.markdown(
            """
            ### 3️⃣ ML Prediction

            The trained ensemble model calculates
            the probability of loan approval.
            """
        )


    with step4:

        st.markdown(
            """
            ### 4️⃣ AI Explanation

            OpenAI converts the ML result into a
            short, understandable explanation.
            """
        )


    # ======================================================
    # RISK THRESHOLDS
    # ======================================================

    with st.expander(
        "ℹ️ About the Risk Level"
    ):

        st.markdown(
            """
            The project uses these demonstration thresholds:

            **80% or above → Low Risk**

            **60%–79.9% → Medium Risk**

            **Below 60% → High Risk**

            These thresholds are defined for this project.
            They are not official banking standards.
            """
        )
