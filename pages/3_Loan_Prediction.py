import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🔮",
    layout="wide"
)


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

    st.error(
        f"Could not load loan_model.pkl: {e}"
    )

    st.stop()


# ==========================================================
# INPUTS
# ==========================================================

st.header("Applicant Information")


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
        ],

    })


    try:

        prediction = model.predict(
            input_data
        )[0]

        probability = model.predict_proba(
            input_data
        )[0][1]


        # Risk level
        if probability >= 0.80:

            risk = "Low Risk"

        elif probability >= 0.60:

            risk = "Medium Risk"

        else:

            risk = "High Risk"


        # ==================================================
        # RESULT
        # ==================================================

        st.header("📋 Prediction Result")


        col1, col2, col3 = st.columns(3)


        with col1:

            if prediction == 1:
                st.success("✅ LOAN APPROVED")
            else:
                st.error("❌ LOAN REJECTED")


        with col2:

            st.metric(
                "Approval Probability",
                f"{probability * 100:.1f}%"
            )


        with col3:

            st.metric(
                "Risk Level",
                risk
            )


        # ==================================================
        # INPUT SUMMARY
        # ==================================================

        with st.expander("📋 View Applicant Details"):

            st.dataframe(
                input_data,
                use_container_width=True
            )


        st.info(
            "Risk thresholds shown here are project-defined "
            "demonstration thresholds, not official banking standards."
        )


    except Exception as e:

        st.error(
            f"Prediction failed: {e}"
        )
