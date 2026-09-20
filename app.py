import streamlit as st
from utils import load_repository_dataset, show_dataset_expander
from ui_theme import apply_theme, sidebar_brand, hero

st.set_page_config(page_title="Bharat Loan AI | Project Dashboard", page_icon="🏦", layout="wide")
apply_theme()
sidebar_brand()
st.sidebar.markdown("### Navigation")
st.sidebar.caption("Academic ML project • not a real bank")
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='color:#f0c45c;font-weight:700;'>By- Ashutosh Paltasingh</div>", unsafe_allow_html=True)

hero("Bharat Loan AI", "Project dashboard · Loan approval prediction with ensemble learning")
st.caption("HOME · PROJECT OVERVIEW")
df = load_repository_dataset()

st.markdown("## 🗂️ Project at a glance")
st.markdown("Explore the dataset, compare ensemble strategies, run your own experiment, or test an applicant against the saved model.")
cols = st.columns(4)
rows = df.shape[0] if df is not None else 4269
cols[0].metric("Dataset records", f"{rows:,}")
cols[1].metric("Models studied", "5")
cols[2].metric("Ensemble approaches", "2")
cols[3].metric("Explanation layer", "Gemini AI")

st.markdown("## 📚 Dataset card")
st.markdown("""
<div class="section-card">
  <div class="section-title">Loan Approval Dataset</div>
  <div class="section-subtitle">The same reference dataset underpins the saved model and the reported model-comparison results.</div>
  <ul>
    <li><b>File:</b> <code>loan_approval_dataset.csv</code></li>
    <li><b>Size:</b> 4,269 rows × 13 columns (including the identifier and target columns in the source dataset).</li>
    <li><b>Target:</b> <code>loan_status</code> — Approved or Rejected.</li>
    <li><b>Predictors:</b> CIBIL score, annual income, loan amount and term, dependents, education, self-employment, and asset values.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🧭 Explore the application")
items = st.columns(3)
with items[0]:
    st.markdown("### ⚖️ Bagging vs Boosting")
    st.write("Understand parallel versus sequential ensemble learning and review validation metrics.")
with items[1]:
    st.markdown("### 🧪 Run Experiment")
    st.write("Upload a compatible binary-classification CSV and evaluate five models with cross-validation.")
with items[2]:
    st.markdown("### 🔮 Loan Prediction")
    st.write("Enter applicant features and view the saved model’s prediction and probability estimates.")

if df is not None:
    show_dataset_expander(df, "🔎 Preview the repository dataset")

st.markdown("## 🔄 Prediction workflow")
st.markdown("""
<div class="workflow">
  <div class="workflow-step"><div class="workflow-num">1</div><div class="workflow-title">Applicant input</div><div class="workflow-text">Provide the financial and applicant features.</div></div>
  <div class="workflow-step"><div class="workflow-num">2</div><div class="workflow-title">Preprocessing</div><div class="workflow-text">The saved pipeline prepares features for the estimator.</div></div>
  <div class="workflow-step"><div class="workflow-num">3</div><div class="workflow-title">Model inference</div><div class="workflow-text">The ensemble produces a class prediction and probabilities.</div></div>
  <div class="workflow-step"><div class="workflow-num">4</div><div class="workflow-title">Explanation</div><div class="workflow-text">An optional AI layer explains the output for demonstration.</div></div>
</div>
<div class="footer-card">🇮🇳 <b>Bharat Loan AI</b> · Academic machine-learning project · Developed by Ashutosh Paltasingh · B.Tech CSE (AIML). Not a real financial institution.</div>
""", unsafe_allow_html=True)
