import os

import joblib
import pandas as pd
import streamlit as st
from google import genai


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
    Enter applicant information to predict whether the
    loan application is likely to be approved.
    """
)


# ==========================================================
# LOAD ML MODEL
# ==========================================================

try:
    model = joblib.load("loan_model.pkl")

except Exception as e:
    st.error(f"Could not load loan_model.pkl: {e}")
    st.stop()


# ==========================================================
# GET TOP FEATURE IMPORTANCE
# ==========================================================

def get_top_features(model, top_n=5):

    try:

        if hasattr(model, "named_steps"):

            preprocessor = model.named_steps.get("preprocessor")
            trained_model = model.named_steps.get("model")

            if (
                preprocessor is not None
                and trained_model is not None
                and hasattr(
                    trained_model,
                    "feature_importances_"
                )
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

                result = []

                for _, row in feature_df.iterrows():

                    feature_name = str(
                        row["Feature"]
                    )

                    feature_name = (
                        feature_name
                        .replace("numeric__", "")
                        .replace("categorical__", "")
                        .replace("num__", "")
                        .replace("cat__", "")
                    )

                    result.append(
                        (
                            feature_name,
                            float(row["Importance"])
                        )
                    )

                return result

        return []

    except Exception:
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
    # ML PREDICTION
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


    # ------------------------------------------------------
    # PREDICTION TEXT
    # ------------------------------------------------------

    if prediction == 1:
        prediction_text = "Approved"
    else:
        prediction_text = "Rejected"


    # ------------------------------------------------------
    # RISK LEVEL
    # ------------------------------------------------------

    if approval_probability >= 0.80:
        risk = "Low Risk"

    elif approval_probability >= 0.60:
        risk = "Medium Risk"

    else:
        risk = "High Risk"


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
            f"{approval_probability * 100:.1f}%"
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
    # FEATURE IMPORTANCE
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
        "Gemini is used only to explain the result."
    )


    # ------------------------------------------------------
    # GET GEMINI API KEY
    # ------------------------------------------------------

    gemini_api_key = None

    try:

        gemini_api_key = st.secrets.get(
            "GEMINI_API_KEY"
        )

    except Exception:

        gemini_api_key = None


    # Local fallback
    if not gemini_api_key:

        gemini_api_key = os.getenv(
            "GEMINI_API_KEY"
        )


    # ------------------------------------------------------
    # CHECK KEY
    # ------------------------------------------------------

    if not gemini_api_key:

        st.warning(
            """
            Gemini API key is not configured.

            Add this to Streamlit Secrets:

            GEMINI_API_KEY = "your-gemini-api-key"
            """
        )

    else:

        try:

            client = genai.Client(
                api_key=gemini_api_key.strip()
            )


            # ------------------------------------------------
            # FEATURE IMPORTANCE TEXT
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
                    "Feature importance is unavailable."
                )


            # ------------------------------------------------
            # PROMPT
            # ------------------------------------------------

            prompt = f"""
You are explaining a college machine-learning project.

Project:
Loan Approval Prediction: Bagging vs Boosting

The trained machine-learning model has already made
the prediction. Do not make a new prediction.

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

TOP MODEL FEATURE IMPORTANCE
----------------------------
{feature_text}

Write a simple explanation for a college project presentation.

Requirements:

1. Start with one sentence stating the model prediction.
2. Explain the approval probability in simple language.
3. Mention important applicant factors visible in the input.
4. Use feature importance only as model-level information.
5. Do not say that one feature definitely caused the prediction.
6. Explain this workflow:
   applicant data → preprocessing → trained ML model
   → approval probability → final prediction.
7. Do not call this an actual bank decision.
8. Do not invent banking rules.
9. Keep the explanation around 100-130 words.
10. Use simple English.
"""


            # ------------------------------------------------
            # GEMINI CALL
            # ------------------------------------------------

            with st.spinner(
                "Generating AI explanation..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt
                )


            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            explanation = (
                response.text
                if response.text
                else ""
            ).strip()


            if explanation:

                st.markdown(
                    explanation
                )

            else:

                st.warning(
                    "Gemini returned an empty explanation."
                )


            st.caption(
                "AI-generated explanation for project "
                "demonstration. It does not represent "
                "an actual banking decision."
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

            Applicant details are entered into
            the application.
            """
        )


    with step2:

        st.markdown(
            """
            ### 2️⃣ Preprocessing

            The information is prepared using
            the same preprocessing used during training.
            """
        )


    with step3:

        st.markdown(
            """
            ### 3️⃣ ML Prediction

            The trained ensemble model calculates
            the approval probability.
            """
        )


    with step4:

        st.markdown(
            """
            ### 4️⃣ AI Explanation

            Gemini converts the model result into
            a simple explanation.
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

            These are project-defined thresholds and are not
            official banking standards.
            """
        )
