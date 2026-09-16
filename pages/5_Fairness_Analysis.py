import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Fairness Analysis",
    page_icon="⚖️",
    layout="wide"
)


st.title("⚖️ Fairness Analysis")

st.markdown(
    """
    This section compares model performance across the
    applicant groups available in the dataset.
    """
)


st.info(
    """
    Fairness analysis is limited to the attributes available
    in this dataset. Differences between groups do not by
    themselves establish discrimination.
    """
)


# ==========================================================
# MODEL SELECTOR
# ==========================================================

model_name = st.selectbox(
    "Select Model",
    [
        "Decision Tree",
        "Bagging",
        "Random Forest",
        "AdaBoost",
        "Gradient Boosting"
    ]
)


# ==========================================================
# EDUCATION DATA
# ==========================================================

education_data = {

    "Decision Tree": [
        ["Graduate", 434, 0.6198, 0.9793, 0.9815, 0.0244, 0.0185],
        ["Not Graduate", 420, 0.6238, 0.9786, 0.9847, 0.0314, 0.0153]
    ],

    "Bagging": [
        ["Graduate", 434, 0.6267, 0.9862, 0.9926, 0.0244, 0.0074],
        ["Not Graduate", 420, 0.6286, 0.9881, 0.9962, 0.0252, 0.0038]
    ],

    "Random Forest": [
        ["Graduate", 434, 0.6198, 0.9793, 0.9815, 0.0244, 0.0185],
        ["Not Graduate", 420, 0.6310, 0.9810, 0.9923, 0.0377, 0.0077]
    ],

    "AdaBoost": [
        ["Graduate", 434, 0.6060, 0.9654, 0.9593, 0.0244, 0.0407],
        ["Not Graduate", 420, 0.6262, 0.9667, 0.9770, 0.0503, 0.0230]
    ],

    "Gradient Boosting": [
        ["Graduate", 434, 0.6244, 0.9839, 0.9889, 0.0244, 0.0111],
        ["Not Graduate", 420, 0.6262, 0.9810, 0.9885, 0.0314, 0.0115]
    ]
}


education_df = pd.DataFrame(
    education_data[model_name],
    columns=[
        "Education",
        "Samples",
        "Approval Rate",
        "Accuracy",
        "TPR",
        "FPR",
        "FNR"
    ]
)


# ==========================================================
# SELF EMPLOYMENT
# ==========================================================

employment_data = {

    "Decision Tree": [
        ["No", 426, 0.6408, 0.9812, 0.9889, 0.0323, 0.0111],
        ["Yes", 428, 0.6028, 0.9766, 0.9769, 0.0238, 0.0231]
    ],

    "Bagging": [
        ["No", 426, 0.6408, 0.9859, 0.9926, 0.0258, 0.0074],
        ["Yes", 428, 0.6145, 0.9883, 0.9962, 0.0238, 0.0038]
    ],

    "Random Forest": [
        ["No", 426, 0.6362, 0.9765, 0.9815, 0.0323, 0.0185],
        ["Yes", 428, 0.6145, 0.9836, 0.9923, 0.0298, 0.0077]
    ],

    "AdaBoost": [
        ["No", 426, 0.6315, 0.9718, 0.9742, 0.0323, 0.0258],
        ["Yes", 428, 0.6005, 0.9603, 0.9615, 0.0417, 0.0385]
    ],

    "Gradient Boosting": [
        ["No", 426, 0.6408, 0.9812, 0.9889, 0.0323, 0.0111],
        ["Yes", 428, 0.6098, 0.9836, 0.9885, 0.0238, 0.0115]
    ]
}


employment_df = pd.DataFrame(
    employment_data[model_name],
    columns=[
        "Self Employed",
        "Samples",
        "Approval Rate",
        "Accuracy",
        "TPR",
        "FPR",
        "FNR"
    ]
)


# ==========================================================
# EDUCATION
# ==========================================================

st.header("🎓 Education Group")

st.dataframe(
    education_df.style.format({
        "Approval Rate": "{:.2%}",
        "Accuracy": "{:.2%}",
        "TPR": "{:.2%}",
        "FPR": "{:.2%}",
        "FNR": "{:.2%}"
    }),
    use_container_width=True
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    education_df["Education"],
    education_df["Approval Rate"]
)

ax.set_ylabel("Approval Rate")
ax.set_title(
    f"Approval Rate by Education — {model_name}"
)

ax.set_ylim(0, 1)

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# EMPLOYMENT
# ==========================================================

st.header("💼 Self-Employment Group")

st.dataframe(
    employment_df.style.format({
        "Approval Rate": "{:.2%}",
        "Accuracy": "{:.2%}",
        "TPR": "{:.2%}",
        "FPR": "{:.2%}",
        "FNR": "{:.2%}"
    }),
    use_container_width=True
)


fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    employment_df["Self Employed"],
    employment_df["Approval Rate"]
)

ax.set_ylabel("Approval Rate")
ax.set_title(
    f"Approval Rate by Employment Status — {model_name}"
)

ax.set_ylim(0, 1)

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# INTERPRETATION
# ==========================================================

st.header("📝 Interpretation")

st.markdown(
    """
    ### Metrics

    **Approval Rate**
    - Percentage of applicants predicted as approved.

    **TPR (True Positive Rate)**
    - Percentage of actually approved applicants correctly
      predicted as approved.

    **FPR (False Positive Rate)**
    - Percentage of rejected applicants incorrectly predicted
      as approved.

    **FNR (False Negative Rate)**
    - Percentage of approved applicants incorrectly predicted
      as rejected.
    """
)

st.warning(
    """
    These comparisons are descriptive. The dataset contains
    only a limited number of potentially relevant demographic
    attributes, so this analysis should not be interpreted as
    a complete fairness assessment of real-world lending.
    """
)
