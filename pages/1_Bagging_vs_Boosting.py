import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_repository_dataset, show_dataset_expander
from ui_theme import apply_theme, sidebar_brand, hero

st.set_page_config(page_title="Ensemble Methods | Bharat Loan AI", page_icon="⚖️", layout="wide")
apply_theme()
sidebar_brand()
hero("Ensemble Methods", "A side-by-side study of Bagging and Boosting in loan approval classification")
st.caption("PAGE 02 · MODEL COMPARISON")
st.info("**Dataset used:** `loan_approval_dataset.csv` — 4,269 loan applications and 13 columns. The target is `loan_status` (Approved/Rejected). Features describe applicants’ credit, income, loan, education, employment and assets. **Training:** Decision Tree, Bagging, Random Forest, AdaBoost and Gradient Boosting were trained and evaluated using this dataset. Results shown here are reported project validation metrics.")

st.markdown("## 🧺 Bagging | Parallel learning")
st.markdown("Bagging (Bootstrap Aggregating) trains multiple estimators independently on bootstrap samples, then combines their predictions. It is commonly used to reduce variance.")
col1, col2, col3 = st.columns(3)
col1.metric("Training strategy", "Parallel")
col2.metric("Core purpose", "Reduce variance")
col3.metric("Project example", "Bagging")

st.markdown("## 🚀 Boosting | Sequential learning")
st.markdown("Boosting builds estimators in sequence. Later estimators focus on patterns or errors left by earlier ones, combining them into a stronger model.")
col1, col2, col3 = st.columns(3)
col1.metric("Training strategy", "Sequential")
col2.metric("Core purpose", "Improve errors")
col3.metric("Project examples", "AdaBoost / Gradient Boosting")

st.markdown("## ⚖️ Conceptual comparison")
comparison = pd.DataFrame({"Feature": ["Training", "Main goal", "Relationship between estimators", "Examples"], "Bagging": ["Parallel", "Reduce variance", "Independent", "Bagging, Random Forest"], "Boosting": ["Sequential", "Improve errors", "Dependent", "AdaBoost, Gradient Boosting"]})
st.dataframe(comparison, use_container_width=True, hide_index=True)

df = load_repository_dataset()
if df is not None:
    show_dataset_expander(df, "🔎 Inspect the project dataset")

st.markdown("## 📈 Cross-validation metrics")
st.caption("Reported 5-fold validation results for the project models. These are model evaluation metrics, not bank approval guarantees.")
results = pd.DataFrame({"Model": ["Decision Tree", "Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"], "Validation Accuracy": [0.9782, 0.9843, 0.9796, 0.9590, 0.9803], "Validation F1": [0.9825, 0.9875, 0.9837, 0.9669, 0.9843], "Validation ROC-AUC": [0.9771, 0.9975, 0.9967, 0.9948, 0.9981]})
st.dataframe(results.style.format({"Validation Accuracy": "{:.4f}", "Validation F1": "{:.4f}", "Validation ROC-AUC": "{:.4f}"}), use_container_width=True)

for metric, title, ylabel in [("Validation Accuracy", "Validation accuracy by model", "Accuracy"), ("Validation F1", "Validation F1-score by model", "F1-score"), ("Validation ROC-AUC", "Validation ROC-AUC by model", "ROC-AUC")]:
    st.markdown(f"### {title}")
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(results["Model"], results[metric])
    ax.set_ylim(0.90, 1.00)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=18)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.markdown("## 🔍 Generalization gap")
st.caption("Gap values are training score minus validation score.")
gap_data = pd.DataFrame({"Model": ["Decision Tree", "Bagging", "Random Forest", "AdaBoost", "Gradient Boosting"], "Accuracy Gap": [0.0218, 0.0157, 0.0204, 0.0066, 0.0156], "F1 Gap": [0.0175, 0.0125, 0.0163, 0.0054, 0.0125], "ROC-AUC Gap": [0.0229, 0.0025, 0.0033, 0.0016, 0.0018]})
st.dataframe(gap_data.style.format({"Accuracy Gap": "{:.4f}", "F1 Gap": "{:.4f}", "ROC-AUC Gap": "{:.4f}"}), use_container_width=True)

with st.expander("🤖 AI-style explanation of these results"):
    st.markdown("""**How to read the comparison**

    - **Accuracy** is the share of predictions classified correctly.
    - **F1-score** balances precision and recall, which is useful when class counts differ.
    - **ROC-AUC** measures how well the model separates the two classes across thresholds.
    - **Generalization gap** is the training score minus the validation score; a larger positive gap can indicate overfitting.

    **Project interpretation:** Bagging combines independently trained estimators, while boosting builds estimators sequentially to focus on remaining errors. The table presents previously reported validation results for this dataset. These values describe model performance on the evaluation setup and do not guarantee outcomes for new applicants or real lending decisions.

    This explanation is rule-based page content, not a live response from an external generative-AI service.""")
st.caption("This page is part of an academic machine-learning project and does not represent a real financial institution.")
