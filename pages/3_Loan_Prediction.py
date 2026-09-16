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


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🔮 Loan Prediction")

st.markdown(
    """
    Enter the applicant's information to predict whether the
    loan application is likely to be approved.
    """
)


# ==========================================================
# LOAD ML MODEL
# ==========================================================

try:

    model = joblib.load("loan_model.pkl")

except Exception as e:

    st.error(
        f"Could not load loan_model.pkl: {e}"
    )

    st.stop()


# ==========================================================
# APPLICANT INFORMATION
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
# PREDICTION BUTTON
# ==========================================================

st.markdown("---")

predict_button = st.button(
    "🔮 Predict Loan Status",
    type="primary",
    use_container_width=True
)


# ==========================================================
# PREDICTION
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
    # RUN MODEL
    # ------------------------------------------------------

    try:

        prediction = model.predict(
            input_data
        )[0]

        probability = model.predict_proba(
            input_data
        )[0][1]


    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )

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


    # ======================================================
    # RESULT
    # ======================================================

    st.header("📋 Prediction Result")


    result_col1, result_col2, result_col3 = st.columns(3)


    # ------------------------------------------------------
    # RESULT
    # ------------------------------------------------------

    with result_col1:

        if prediction == 1:

            st.success(
                "✅ LOAN APPROVED"
            )

        else:

            st.error(
                "❌ LOAN REJECTED"
            )


    # ------------------------------------------------------
    # PROBABILITY
    # ------------------------------------------------------

    with result_col2:

        st.metric(
            "Approval Probability",
            f"{probability * 100:.1f}%"
        )


    # ------------------------------------------------------
    # RISK
    # ------------------------------------------------------

    with result_col3:

        st.metric(
            "Risk Level",
            risk
        )


    # ======================================================
    # APPLICANT DETAILS
    # ======================================================

    with st.expander(
        "📋 View Applicant Details"
    ):

        st.dataframe(
            input_data,
            use_container_width=True
        )


    # ======================================================
    # MODEL EXPLANATION
    # ======================================================

    st.markdown("---")

    st.header("🤖 AI Explanation of This Prediction")

    st.markdown(
        """
        The AI explanation describes how the trained machine
        learning model arrived at this prediction using the
        applicant's input values and model probability.
        """
    )


    # ======================================================
    # OPENAI API
    # ======================================================

    try:

        # Read API key from Streamlit Secrets
        api_key = st.secrets["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"]

        client = OpenAI(
            api_key=api_key
        )


        # --------------------------------------------------
        # PREDICTION TEXT
        # --------------------------------------------------

        prediction_text = (
            "Approved"
            if prediction == 1
            else "Rejected"
        )


        # --------------------------------------------------
        # AI PROMPT
        # --------------------------------------------------

        prompt = f"""
You are explaining a college machine-learning project.

The project is:
"Loan Approval Prediction: Bagging vs Boosting"

A trained machine-learning model has already made the
following prediction.

Prediction: {prediction_text}

Approval probability:
{probability * 100:.1f}%

Project risk level:
{risk}

Applicant information:

Number of dependents:
{no_of_dependents}

Education:
{education}

Self employed:
{self_employed}

Annual income:
₹{income_annum:,}

Loan amount:
₹{loan_amount:,}

Loan term:
{loan_term} years

CIBIL score:
{cibil_score}

Residential assets:
₹{residential_assets_value:,}

Commercial assets:
₹{commercial_assets_value:,}

Luxury assets:
₹{luxury_assets_value:,}

Bank assets:
₹{bank_asset_value:,}


Explain the result in simple language for a college
presentation.

Requirements:

1. Start with one short sentence explaining the prediction.
2. Mention the most important applicant factors visible
   from the supplied information.
3. Explain why the probability is high or low in simple terms.
4. Briefly explain the process:
   applicant data → trained ML model → probability → prediction.
5. Do NOT invent model rules or claim that a specific feature
   caused the decision unless the supplied information supports it.
6. Do NOT say that this is an actual bank decision.
7. Keep the explanation between 100 and 150 words.
8. Use simple student-friendly English.
"""


        # --------------------------------------------------
        # CALL OPENAI
        # --------------------------------------------------

        with st.spinner(
            "Generating AI explanation..."
        ):

            response = client.responses.create(

                model="gpt-5.6-luna",

                input=prompt
            )


        # --------------------------------------------------
        # DISPLAY AI RESPONSE
        # --------------------------------------------------

        explanation = response.output_text


        st.markdown(
            explanation
        )


        # --------------------------------------------------
        # DISCLAIMER
        # --------------------------------------------------

        st.caption(
            "AI-generated explanation of the ML prediction. "
            "It is for project demonstration and does not "
            "represent an actual banking decision."
        )


    # ======================================================
    # API ERROR
    # ======================================================

    except KeyError:

        st.warning(
            """
            OpenAI API key is not configured.

            Add your API key to Streamlit Secrets as:

            OPENAI_API_KEY = "your-api-key"
            """
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

            Applicant information is entered into the
            Streamlit application.
            """
        )


    with step2:

        st.markdown(
            """
            ### 2️⃣ ML Model

            The trained loan approval model processes
            the applicant features.
            """
        )


    with step3:

        st.markdown(
            """
            ### 3️⃣ Probability

            The model produces an approval probability.
            """
        )


    with step4:

        st.markdown(
            """
            ### 4️⃣ Result

            The application is classified as Approved
            or Rejected.
            """
        )


    # ======================================================
    # PROJECT RISK THRESHOLD
    # ======================================================

    with st.expander(
        "ℹ️ About the Risk Level"
    ):

        st.markdown(
            """
            The project uses these demonstration thresholds:

            - **80% or above:** Low Risk
            - **60%–79.9%:** Medium Risk
            - **Below 60%:** High Risk

            These are project-defined thresholds and are not
            official banking standards.
            """
        )
