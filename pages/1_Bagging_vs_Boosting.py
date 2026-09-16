import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import load_repository_dataset, show_dataset_expander


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bagging vs Boosting",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# DATASET
# =========================================================

df = load_repository_dataset()


# =========================================================
# TITLE
# =========================================================

st.title("📊 Bagging vs Boosting")

st.write(
    """
    Comparison of ensemble learning methods used for
    loan approval prediction.
    """
)


# Dataset expandable section
show_dataset_expander(df)


st.divider()


# =========================================================
# BAGGING
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.header("🌳 Bagging")

    st.write(
        """
        Bagging trains multiple models independently and combines
        their predictions to reduce variance.
        """
    )

    st.write("**Models:**")

    st.write("• Bagging")
    st.write("• Random Forest")


with col2:

    st.header("🚀 Boosting")

    st.write(
        """
        Boosting trains models sequentially, with later models
        focusing on errors made by earlier models.
        """
    )

    st.write("**Models:**")

    st.write("• AdaBoost")
    st.write("• Gradient Boosting")


st.divider()


# =========================================================
# MODEL RESULTS
# =========================================================

st.header("Model Performance Comparison")


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


display_results = results.copy()


for column in [
    "Validation Accuracy",
    "Validation F1",
    "Validation ROC-AUC"
]:

    display_results[column] = (
        display_results[column] * 100
    ).round(2).astype(str) + "%"


st.dataframe(
    display_results,
    use_container_width=True,
    hide_index=True
)


st.caption(
    "Results from the project's 5-fold stratified cross-validation."
)


st.divider()


# =========================================================
# ACCURACY
# =========================================================

st.header("Accuracy Comparison")


fig, ax = plt.subplots(
    figsize=(10, 5)
)


ax.bar(
    results["Model"],
    results["Validation Accuracy"]
)


ax.set_ylabel("Accuracy")

ax.set_ylim(
    0.90,
    1.02
)

ax.set_title(
    "Validation Accuracy"
)

ax.tick_params(
    axis="x",
    rotation=20
)

ax.grid(
    axis="y",
    alpha=0.3
)


st.pyplot(fig)

plt.close(fig)


# =========================================================
# F1
# =========================================================

st.header("F1 Score Comparison")


fig, ax = plt.subplots(
    figsize=(10, 5)
)


ax.bar(
    results["Model"],
    results["Validation F1"]
)


ax.set_ylabel("F1 Score")

ax.set_ylim(
    0.90,
    1.02
)

ax.set_title(
    "Validation F1 Score"
)

ax.tick_params(
    axis="x",
    rotation=20
)

ax.grid(
    axis="y",
    alpha=0.3
)


st.pyplot(fig)

plt.close(fig)


# =========================================================
# ROC-AUC
# =========================================================

st.header("ROC-AUC Comparison")


fig, ax = plt.subplots(
    figsize=(10, 5)
)


ax.bar(
    results["Model"],
    results["Validation ROC-AUC"]
)


ax.set_ylabel("ROC-AUC")

ax.set_ylim(
    0.90,
    1.02
)

ax.set_title(
    "Validation ROC-AUC"
)

ax.tick_params(
    axis="x",
    rotation=20
)

ax.grid(
    axis="y",
    alpha=0.3
)


st.pyplot(fig)

plt.close(fig)
