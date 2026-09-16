import streamlit as st

from utils import load_repository_dataset, show_dataset_expander


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# LOAD DATASET
# =========================================================

df = load_repository_dataset()


# =========================================================
# HOME PAGE
# =========================================================

st.title("🏦 Loan Approval Prediction: Bagging vs Boosting")

st.subheader(
    "Ensemble Learning Based Loan Approval System"
)

st.write(
    """
    This project compares Bagging and Boosting ensemble learning
    techniques for loan approval prediction. It evaluates multiple
    machine learning models using Accuracy, F1 Score and ROC-AUC.
    """
)

st.divider()


# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.header("Project Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Models Compared",
        "5"
    )

with col2:
    st.metric(
        "Validation",
        "5-Fold CV"
    )

with col3:

    if df is not None:
        st.metric(
            "Dataset Rows",
            df.shape[0]
        )
    else:
        st.metric(
            "Dataset Rows",
            "N/A"
        )


st.write(
    """
    The project uses a Decision Tree as the baseline and compares
    Bagging, Random Forest, AdaBoost and Gradient Boosting.
    """
)


# =========================================================
# DATASET
# =========================================================

show_dataset_expander(df)


st.divider()


# =========================================================
# NAVIGATION
# =========================================================

st.header("Project Sections")

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("📊 Bagging vs Boosting")

    st.write(
        "View the project's model comparison and evaluation results."
    )

    if st.button(
        "Open Model Comparison",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Bagging_vs_Boosting.py"
        )


with col2:

    st.subheader("🧪 Run Experiment")

    st.write(
        "Upload a loan approval CSV and generate new results."
    )

    if st.button(
        "Open Experiment",
        use_container_width=True
    ):

        st.switch_page(
            "pages/2_Run_Experiment.py"
        )


with col3:

    st.subheader("🔮 Loan Prediction")

    st.write(
        "Enter applicant details and predict loan approval."
    )

    if st.button(
        "Open Prediction",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Loan_Prediction.py"
        )


st.divider()


st.caption(
    "Loan Approval Prediction: Bagging vs Boosting"
)
