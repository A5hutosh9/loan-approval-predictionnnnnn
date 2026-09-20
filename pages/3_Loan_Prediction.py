import os

import joblib
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types

from ui_theme import apply_theme, sidebar_brand, hero


GEMINI_MODELS = ("gemini-3.8-flash", "gemini-2.5-flash")


def generate_ai_explanation(api_key, prompt):
    """Use a capacity fallback so a busy Gemini model does not break the page."""
    client = genai.Client(api_key=api_key.strip())
    failures = []

    for model_name in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=220,
                ),
            )
            explanation = getattr(response, "text", None)
            if explanation and explanation.strip():
                return explanation.strip()
            failures.append(f"{model_name} returned no text")
        except Exception as error:
            failures.append(f"{model_name}: {error}")

    raise RuntimeError(" | ".join(failures))


def local_prediction_explanation(
    prediction_text,
    approval_probability,
    risk,
    cibil_score,
    income_annum,
    loan_amount,
):
    """Provide a useful academic explanation when Gemini is temporarily unavailable."""
    return f"""
**Academic prediction summary:** the trained ensemble model returned **{prediction_text}**
with an approval probability of **{approval_probability * 100:.1f}%** and a
**{risk}** classification.

This percentage represents the model's confidence from patterns in its training
data; it is not a real bank decision. The model evaluated the supplied applicant
details together, including the CIBIL score ({cibil_score}), annual income
(₹{income_annum:,}), requested loan amount (₹{loan_amount:,}), employment,
education, and declared assets. The workflow is: applicant input → preprocessing
→ trained ensemble model → probability → predicted result.
""".strip()


st.set_page_config(
    page_title="Loan Prediction | Bharat Loan AI",
    page_icon="🔮",
    layout="wide",
)

apply_theme()
sidebar_brand()

hero(
    "Loan Approval Prediction",
    "Enter applicant details and review the model result"
)

try:
    model = joblib.load("loan_model.pkl")
except Exception as e:
    st.error(f"Could not load loan_model.pkl: {e}")
    st.stop()

st.markdown("<div class='section-title'>👤 Applicant Information</div><div class='section-subtitle'>Complete the fields below. The ML model will use the same feature structure as training.</div>", unsafe_allow_html=True)

left, right = st.columns([1.55, 1], gap="large")

with left:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Personal & Financial Details</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        no_of_dependents = st.number_input("Number of Dependents", 0, 20, 2)
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    with c2:
        self_employed = st.selectbox("Self Employed", ["No", "Yes"])
        income_annum = st.number_input("Annual Income (₹)", min_value=0, value=600000, step=10000)
    with c3:
        loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=1500000, step=10000)
        loan_term = st.number_input("Loan Term (Years)", 1, 50, 15)

    st.markdown("<div class='section-title' style='margin-top:10px;'>🏠 Assets & Credit</div>", unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        cibil_score = st.number_input("CIBIL Score", 0, 900, 760)
        residential_assets_value = st.number_input("Residential Assets (₹)", min_value=0, value=2000000, step=10000)
        commercial_assets_value = st.number_input("Commercial Assets (₹)", min_value=0, value=500000, step=10000)
    with a2:
        luxury_assets_value = st.number_input("Luxury Assets (₹)", min_value=0, value=300000, step=10000)
        bank_asset_value = st.number_input("Bank Assets (₹)", min_value=0, value=400000, step=10000)

    predict = st.button("🔮 Predict Loan Status", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-card'><div class='section-title'>🏦 Bank-style Review</div><div class='section-subtitle'>Prediction results appear here after submission.</div></div>", unsafe_allow_html=True)
    st.info("Enter the applicant details and click **Predict Loan Status** to generate the model result.")

if predict:
    input_data = pd.DataFrame({
        "no_of_dependents": [no_of_dependents],
        "education": [education],
        "self_employed": [self_employed],
        "income_annum": [income_annum],
        "loan_amount": [loan_amount],
        "loan_term": [loan_term],
        "cibil_score": [cibil_score],
        "residential_assets_value": [residential_assets_value],
        "commercial_assets_value": [commercial_assets_value],
        "luxury_assets_value": [luxury_assets_value],
        "bank_asset_value": [bank_asset_value],
    })

    try:
        prediction = int(model.predict(input_data)[0])
        probs = model.predict_proba(input_data)[0]
        approval_probability = float(probs[1])
        rejection_probability = float(probs[0])
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.stop()

    prediction_text = "Approved" if prediction == 1 else "Rejected"
    risk = "Low Risk" if approval_probability >= 0.80 else "Medium Risk" if approval_probability >= 0.60 else "High Risk"

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 Prediction Result</div>", unsafe_allow_html=True)

    if prediction == 1:
        st.markdown(f"<div class='approval-card'><div class='approval-title'>✅ Loan Approved</div><div style='color:#40604f;'>The trained ML model predicts that this application is likely to be approved.</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='rejection-card'><div class='rejection-title'>❌ Loan Rejected</div><div style='color:#6b4650;'>The trained ML model predicts that this application is likely to be rejected.</div></div>", unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    r1.markdown(f"<div class='metric-card'><div class='metric-label'>Approval probability</div><div class='metric-value'>{approval_probability*100:.1f}%</div><div class='metric-note'>Model probability</div></div>", unsafe_allow_html=True)
    r2.markdown(f"<div class='metric-card'><div class='metric-label'>Risk level</div><div class='metric-value'>{risk}</div><div class='metric-note'>Project threshold</div></div>", unsafe_allow_html=True)
    r3.markdown(f"<div class='metric-card'><div class='metric-label'>Rejection probability</div><div class='metric-value'>{rejection_probability*100:.1f}%</div><div class='metric-note'>Model probability</div></div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🤖 AI Explanation", "👤 Applicant Details"])

    with tab1:
        st.markdown("<div class='ai-card'><div class='ai-label'>Gemini AI • Explanation Layer</div>", unsafe_allow_html=True)

        gemini_api_key = None
        try:
            gemini_api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            pass
        gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")

        if not gemini_api_key:
            st.warning("Add GEMINI_API_KEY to Streamlit Secrets to enable the AI explanation.")
        else:
            prompt = f"""
You are explaining a college ML project named Loan Approval Prediction: Bagging vs Boosting.
The trained ML model has already produced this result and you must not make a new decision.

Prediction: {prediction_text}
Approval probability: {approval_probability*100:.1f}%
Risk level: {risk}

Applicant:
- Dependents: {no_of_dependents}
- Education: {education}
- Self-employed: {self_employed}
- Annual income: ₹{income_annum:,}
- Loan amount: ₹{loan_amount:,}
- Loan term: {loan_term} years
- CIBIL score: {cibil_score}
- Residential assets: ₹{residential_assets_value:,}
- Commercial assets: ₹{commercial_assets_value:,}
- Luxury assets: ₹{luxury_assets_value:,}
- Bank assets: ₹{bank_asset_value:,}

Give a concise 100-130 word explanation for a college demonstration.
Explain what the probability means, mention relevant factors from the supplied data, and explain the workflow:
input -> preprocessing -> trained ML model -> probability -> prediction.
Do not invent banking rules and do not claim one feature alone caused the decision.
Clearly state that this is an academic ML prediction, not an actual bank decision.
"""
            try:
                with st.spinner("Generating AI explanation..."):
                    explanation = generate_ai_explanation(gemini_api_key, prompt)
                st.write(explanation)
            except Exception:
                st.caption(
                    "Gemini is temporarily busy, so a reliable local explanation is shown instead."
                )
                st.write(
                    local_prediction_explanation(
                        prediction_text,
                        approval_probability,
                        risk,
                        cibil_score,
                        income_annum,
                        loan_amount,
                    )
                )

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.dataframe(input_data, use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>⚙️ How It Works</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='workflow'>
      <div class='workflow-step'><div class='workflow-num'>1</div><div class='workflow-title'>Input</div><div class='workflow-text'>Applicant information is entered into the app.</div></div>
      <div class='workflow-step'><div class='workflow-num'>2</div><div class='workflow-title'>Preprocessing</div><div class='workflow-text'>The trained pipeline prepares numeric and categorical features.</div></div>
      <div class='workflow-step'><div class='workflow-num'>3</div><div class='workflow-title'>ML Prediction</div><div class='workflow-text'>The ensemble model returns approval probability.</div></div>
      <div class='workflow-step'><div class='workflow-num'>4</div><div class='workflow-title'>Gemini Explanation</div><div class='workflow-text'>Gemini turns the model result into a short explanation.</div></div>
    </div>
    <div class='footer-card'>🇮🇳 <b>Bharat Loan AI</b> is fictional branding for an academic project. It is not a real financial institution.</div>
    """, unsafe_allow_html=True)
