import streamlit as st
from utils import load_repository_dataset, show_dataset_expander


st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="🏦",
    layout="wide"
)


# -----------------------------
# LOAD DATASET
# -----------------------------

df = load_repository_dataset()


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("🏦 Loan Approval")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    **Machine Learning Project**

    Loan Approval Prediction:
    Bagging vs Boosting
    
st.sidebar.markdown(
    '<p style="color:#D4A017; font-size:18px; font-weight:600;">By- Ashutosh Paltasingh</p>',
    unsafe_allow_html=True


    """
)



# -----------------------------
# HOME
# -----------------------------

st.title("🏦 Loan Approval Prediction")

st.subheader("Bagging vs Boosting")

st.markdown(
    """
    This project uses machine learning ensemble techniques to predict
    whether a loan application will be **Approved** or **Rejected**.
    """
)


# -----------------------------
# PROJECT OVERVIEW
# -----------------------------

st.markdown("## 📌 Project Overview")

col1, col2, col3, col4 = st.columns(4)

if df is not None:

    with col1:
        st.metric("Dataset Rows", f"{df.shape[0]:,}")

    with col2:
        st.metric("Features", df.shape[1] - 2)

    with col3:
        st.metric("Approved", "2,656")

    with col4:
        st.metric("Rejected", "1,613")


# -----------------------------
# OBJECTIVE
# -----------------------------

st.markdown("## 🎯 Objective")

st.markdown(
    """
    - Predict loan approval using applicant information.
    - Compare **Bagging** and **Boosting** ensemble methods.
    - Evaluate models using Accuracy, F1-score and ROC-AUC.
    - Study model generalization using cross-validation.
    - Analyse feature importance.
    - Provide individual loan predictions.
    - Examine fairness across available applicant groups.
    """
)


# -----------------------------
# MODELS
# -----------------------------

st.markdown("## 🤖 Models Used")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.info("Decision Tree")

with col2:
    st.info("Bagging")

with col3:
    st.info("Random Forest")

with col4:
    st.info("AdaBoost")

with col5:
    st.info("Gradient Boosting")


# -----------------------------
# DATASET
# -----------------------------

if df is not None:
    show_dataset_expander(df, "📁 Dataset")


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

st.caption(
    "Loan Approval Prediction • Machine Learning Project"
)
