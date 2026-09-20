import streamlit as st
from utils import load_repository_dataset, show_dataset_expander
from ui_theme import apply_theme, sidebar_brand, hero

# Streamlit page configuration must be the first Streamlit command.
st.set_page_config(
    page_title="Bharat Loan AI | Loan Approval Prediction",
    page_icon="🏦",
    layout="wide",
)

# Apply the theme and branding only once.
apply_theme()
sidebar_brand()

st.sidebar.markdown("### Navigation")
st.sidebar.caption("Academic ML project • not a real bank")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='color:#f0c45c;font-weight:700;'>By- Ashutosh Paltasingh</div>",
    unsafe_allow_html=True,
)

# Render one hero banner only.
hero(
    "Loan Approval Prediction",
    "Using ensemble learning to analyse loan applications"
)

df = load_repository_dataset()

st.markdown(
    "<div class='section-title'>🏛️ Project Overview</div>"
    "<div class='section-subtitle'>A banking-style interface for your existing machine-learning project.</div>",
    unsafe_allow_html=True,
)

cols = st.columns(4)
rows = df.shape[0] if df is not None else 4269
cols[0].markdown(
    f"<div class='metric-card'><div class='metric-label'>Dataset records</div><div class='metric-value'>{rows:,}</div><div class='metric-note'>Loan applications</div></div>",
    unsafe_allow_html=True,
)
cols[1].markdown(
    "<div class='metric-card'><div class='metric-label'>Models</div><div class='metric-value'>5</div><div class='metric-note'>Tree + ensemble models</div></div>",
    unsafe_allow_html=True,
)
cols[2].markdown(
    "<div class='metric-card'><div class='metric-label'>Ensemble families</div><div class='metric-value'>2</div><div class='metric-note'>Bagging &amp; Boosting</div></div>",
    unsafe_allow_html=True,
)
cols[3].markdown(
    "<div class='metric-card'><div class='metric-label'>AI layer</div><div class='metric-value'>Gemini</div><div class='metric-note'>Prediction explanation</div></div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="section-card">
        <div class="section-title">🎯 What this application does</div>
        <div class="section-subtitle">
            The interface wraps your existing Colab model into an interactive banking-style application.
        </div>
        <ul>
            <li>Compare Decision Tree, Bagging, Random Forest, AdaBoost and Gradient Boosting.</li>
            <li>Run new experiments on uploaded loan datasets.</li>
            <li>Generate individual loan predictions from the trained model.</li>
            <li>Show model-level feature importance and fairness analysis.</li>
            <li>Use Gemini to explain a prediction in simple language.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

if df is not None:
    show_dataset_expander(df, "📁 Repository Dataset")

st.markdown(
    """
    <div class="workflow">
      <div class="workflow-step"><div class="workflow-num">1</div><div class="workflow-title">Applicant Input</div><div class="workflow-text">Enter personal, financial and asset information.</div></div>
      <div class="workflow-step"><div class="workflow-num">2</div><div class="workflow-title">ML Processing</div><div class="workflow-text">The trained ensemble pipeline processes the inputs.</div></div>
      <div class="workflow-step"><div class="workflow-num">3</div><div class="workflow-title">Prediction</div><div class="workflow-text">The system returns approval probability and risk level.</div></div>
      <div class="workflow-step"><div class="workflow-num">4</div><div class="workflow-title">AI Explanation</div><div class="workflow-text">Gemini explains the model result in simple terms.</div></div>
    </div>
    <div class="footer-card">🇮🇳 <b>Bharat Loan AI</b> • Academic machine-learning project • Developed by Ashutosh Paltasingh • B.Tech CSE (AIML)</div>
    """,
    unsafe_allow_html=True,
)
