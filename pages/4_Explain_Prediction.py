import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Explain Prediction",
    page_icon="🔍",
    layout="wide"
)


st.title("🔍 Explain Prediction")

st.markdown(
    """
    This page explains which applicant features have the
    strongest influence on the model's prediction.
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
# INPUT
# ==========================================================

st.header("Applicant Information")


col1, col2 = st.columns(2)


with col1:

    no_of_dependents = st.number_input(
        "Number of Dependents",
        0,
        20,
        2
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
        0,
        100000000,
        600000,
        step=10000
    )

    loan_amount = st.number_input(
        "Loan Amount",
        0,
        100000000,
        1500000,
        step=10000
    )

    loan_term = st.number_input(
        "Loan Term",
        1,
        50,
        15
    )


with col2:

    cibil_score = st.number_input(
        "CIBIL Score",
        0,
        900,
        760
    )

    residential_assets_value = st.number_input(
        "Residential Assets Value",
        0,
        100000000,
        2000000,
        step=10000
    )

    commercial_assets_value = st.number_input(
        "Commercial Assets Value",
        0,
        100000000,
        500000,
        step=10000
    )

    luxury_assets_value = st.number_input(
        "Luxury Assets Value",
        0,
        100000000,
        300000,
        step=10000
    )

    bank_asset_value = st.number_input(
        "Bank Asset Value",
        0,
        100000000,
        400000,
        step=10000
    )


input_data = pd.DataFrame({

    "no_of_dependents": [no_of_dependents],

    "education": [education],

    "self_employed": [self_employed],

    "income_annum": [income_annum],

    "loan_amount": [loan_amount],

    "loan_term": [loan_term],

    "cibil_score": [cibil_score],

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


# ==========================================================
# PREDICTION
# ==========================================================

if st.button(
    "🔍 Explain This Prediction",
    type="primary",
    use_container_width=True
):

    prediction = model.predict(
        input_data
    )[0]

    probability = model.predict_proba(
        input_data
    )[0][1]


    if prediction == 1:

        st.success(
            f"Prediction: LOAN APPROVED "
            f"({probability * 100:.1f}% probability)"
        )

    else:

        st.error(
            f"Prediction: LOAN REJECTED "
            f"({(1 - probability) * 100:.1f}% rejection probability)"
        )


    # ======================================================
    # FEATURE IMPORTANCE
    # ======================================================

    st.header("📊 Model Feature Importance")


    try:

        fitted_preprocessor = model.named_steps[
            "preprocessor"
        ]

        trained_model = model.named_steps[
            "model"
        ]


        feature_names = (
            fitted_preprocessor
            .get_feature_names_out()
        )


        importances = (
            trained_model
            .feature_importances_
        )


        importance_df = pd.DataFrame({

            "Feature": feature_names,

            "Importance": importances

        }).sort_values(
            "Importance",
            ascending=False
        )


        importance_df["Feature"] = (
            importance_df["Feature"]
            .str.replace(
                "numeric__",
                "",
                regex=False
            )
            .str.replace(
                "categorical__",
                "",
                regex=False
            )
        )


        st.dataframe(
            importance_df,
            use_container_width=True
        )


        # Top features
        top_features = importance_df.head(10)


        fig, ax = plt.subplots(
            figsize=(10, 6)
        )


        ax.barh(
            top_features["Feature"][::-1],
            top_features["Importance"][::-1]
        )


        ax.set_xlabel("Importance")

        ax.set_title(
            "Top Features Used by the Model"
        )


        plt.tight_layout()

        st.pyplot(fig)


        st.info(
            "Feature importance indicates how strongly the "
            "trained model relies on a feature. It does not "
            "establish a causal relationship."
        )


    except Exception as e:

        st.warning(
            f"Feature importance could not be displayed: {e}"
        )
