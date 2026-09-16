import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="wide"
)

# =========================================================
# HOME
# =========================================================

st.title("🏦 Loan Approval Prediction")
st.subheader("Bagging vs Boosting")

st.write(
    "An ensemble learning based project for predicting loan approval "
    "and comparing Bagging and Boosting techniques."
)

st.divider()

# =========================================================
# PROJECT OVERVIEW
# =========================================================

st.header("Project Overview")

st.write(
    """
    This project investigates how ensemble learning techniques can
    improve loan approval prediction. A Decision Tree is used as a
    baseline and is compared with Bagging, Random Forest, AdaBoost,
    and Gradient Boosting.
    """
)

# =========================================================
# PROJECT INFORMATION
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Dataset",
        "4,269 Applications"
    )

with col2:
    st.metric(
        "Models",
        "5"
    )

with col3:
    st.metric(
        "Validation",
        "5-Fold CV"
    )

st.divider()

# =========================================================
# OBJECTIVES
# =========================================================

st.header("Project Objectives")

st.write(
    """
    • Build a Decision Tree baseline

    • Demonstrate overfitting and generalization

    • Apply Bagging and Random Forest

    • Apply AdaBoost and Gradient Boosting

    • Compare Accuracy, F1 Score and ROC-AUC

    • Analyze training vs validation performance

    • Examine fairness across available applicant groups

    • Build a practical loan approval prediction system
    """
)

st.divider()

# =========================================================
# NAVIGATION
# =========================================================

st.header("Project Sections")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "📊 Bagging vs Boosting",
        use_container_width=True
    ):

        st.switch_page(
            "pages/1_Bagging_vs_Boosting.py"
        )


with col2:

    if st.button(
        "🧪 Run Experiment",
        use_container_width=True
    ):

        st.switch_page(
            "pages/2_Run_Experiment.py"
        )


with col3:

    if st.button(
        "🔮 Loan Prediction",
        use_container_width=True
    ):

        st.switch_page(
            "pages/3_Loan_Prediction.py"
        )


st.divider()

st.caption(
    "Loan Approval Prediction: Bagging vs Boosting"
)
