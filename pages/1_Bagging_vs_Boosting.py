import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import load_repository_dataset, show_dataset_expander


st.set_page_config(
    page_title="Bagging vs Boosting",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Bagging vs Boosting")

st.markdown(
    """
    Comparison of ensemble learning techniques used in the
    Loan Approval Prediction project.
    """
)


# ==========================================================
# BAGGING
# ==========================================================

st.header("🟦 Bagging")

st.markdown(
    """
    **Bagging (Bootstrap Aggregating)** trains multiple models
    independently on different bootstrap samples of the dataset.

    The final prediction is obtained by combining the predictions
    of the individual models.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Training Strategy", "Parallel")

with col2:
    st.metric("Main Idea", "Reduce Variance")

with col3:
    st.metric("Project Model", "Bagging")


# ==========================================================
# BOOSTING
# ==========================================================

st.header("🟩 Boosting")

st.markdown(
    """
    **Boosting** builds models sequentially.

    Each new model focuses more on the errors made by previous
    models, gradually improving the overall prediction.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Training Strategy", "Sequential")

with col2:
    st.metric("Main Idea", "Reduce Errors")

with col3:
    st.metric("Project Models", "AdaBoost / GB")


# ==========================================================
# DIFFERENCE
# ==========================================================

st.header("⚖️ Key Difference")

comparison = pd.DataFrame({
    "Feature": [
        "Training",
        "Main Goal",
        "Model Relationship",
        "Examples"
    ],

    "Bagging": [
        "Parallel",
        "Reduce variance",
        "Independent",
        "Bagging, Random Forest"
    ],

    "Boosting": [
        "Sequential",
        "Improve errors",
        "Dependent",
        "AdaBoost, Gradient Boosting"
    ]
})

st.table(comparison)


# ==========================================================
# DATASET
# ==========================================================

df = load_repository_dataset()

if df is not None:
    show_dataset_expander(df, "📁 Dataset")


# ==========================================================
# CROSS VALIDATION RESULTS
# ==========================================================

st.header("📈 5-Fold Cross-Validation Results")

results = pd.DataFrame({
    "Model": [
        "Decision Tree",
        "Bagging",
        "Random Forest",
        "AdaBoost",
        "Gradient Boosting"
    ],

    "Validation Accuracy": [
        0.9782,
        0.9843,
        0.9796,
        0.9590,
        0.9803
    ],

    "Validation F1": [
        0.9825,
        0.9875,
        0.9837,
        0.9669,
        0.9843
    ],

    "Validation ROC-AUC": [
        0.9771,
        0.9975,
        0.9967,
        0.9948,
        0.9981
    ]
})

st.dataframe(
    results.style.format({
        "Validation Accuracy": "{:.4f}",
        "Validation F1": "{:.4f}",
        "Validation ROC-AUC": "{:.4f}"
    }),
    use_container_width=True
)


# ==========================================================
# ACCURACY CHART
# ==========================================================

st.header("📊 Validation Accuracy")

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    results["Model"],
    results["Validation Accuracy"]
)

ax.set_ylim(0.90, 1.00)
ax.set_ylabel("Accuracy")
ax.set_xlabel("Model")
ax.set_title("Validation Accuracy Comparison")

plt.xticks(rotation=20)
plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# F1 CHART
# ==========================================================

st.header("📊 Validation F1-Score")

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    results["Model"],
    results["Validation F1"]
)

ax.set_ylim(0.90, 1.00)
ax.set_ylabel("F1 Score")
ax.set_xlabel("Model")
ax.set_title("Validation F1 Comparison")

plt.xticks(rotation=20)
plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# ROC-AUC CHART
# ==========================================================

st.header("📊 Validation ROC-AUC")

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(
    results["Model"],
    results["Validation ROC-AUC"]
)

ax.set_ylim(0.90, 1.00)
ax.set_ylabel("ROC-AUC")
ax.set_xlabel("Model")
ax.set_title("Validation ROC-AUC Comparison")

plt.xticks(rotation=20)
plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# GENERALIZATION GAP
# ==========================================================

st.header("🔎 Generalization Gap")

gap_data = pd.DataFrame({
    "Model": [
        "Decision Tree",
        "Bagging",
        "Random Forest",
        "AdaBoost",
        "Gradient Boosting"
    ],

    "Accuracy Gap": [
        0.0218,
        0.0157,
        0.0204,
        0.0066,
        0.0156
    ],

    "F1 Gap": [
        0.0175,
        0.0125,
        0.0163,
        0.0054,
        0.0125
    ],

    "ROC-AUC Gap": [
        0.0229,
        0.0025,
        0.0033,
        0.0016,
        0.0018
    ]
})

st.dataframe(
    gap_data.style.format({
        "Accuracy Gap": "{:.4f}",
        "F1 Gap": "{:.4f}",
        "ROC-AUC Gap": "{:.4f}"
    }),
    use_container_width=True
)


st.info(
    "The gap is calculated as Training Score − Validation Score."
)
