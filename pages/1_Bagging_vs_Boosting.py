import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    BaggingClassifier,
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import roc_curve, auc


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bagging vs Boosting",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 Bagging vs Boosting")

st.write(
    "Comparison of ensemble learning techniques for "
    "loan approval prediction."
)

st.divider()


# =========================================================
# BAGGING VS BOOSTING
# =========================================================

st.header("Bagging vs Boosting")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🌳 Bagging")

    st.write("• Reduces variance")
    st.write("• Models train independently")
    st.write("• Uses bootstrap samples")
    st.write("• Predictions are combined")
    st.write("• Bagging")
    st.write("• Random Forest")


with col2:

    st.subheader("🚀 Boosting")

    st.write("• Reduces bias")
    st.write("• Models train sequentially")
    st.write("• Later models focus on previous errors")
    st.write("• AdaBoost")
    st.write("• Gradient Boosting")


st.divider()


# =========================================================
# DATASET EXPANDER
# =========================================================

with st.expander("📁 Dataset — Click to View"):

    try:

        dataset = pd.read_csv(
            "loan_approval_dataset.csv"
        )

        dataset.columns = dataset.columns.str.strip()

        st.write(
            f"Dataset size: **{dataset.shape[0]} rows × "
            f"{dataset.shape[1]} columns**"
        )

        st.dataframe(
            dataset,
            use_container_width=True,
            height=500,
            hide_index=True
        )

    except FileNotFoundError:

        st.warning(
            "loan_approval_dataset.csv was not found "
            "in the repository."
        )


st.divider()


# =========================================================
# PROJECT RESULTS
# =========================================================

st.header("5-Fold Cross-Validation Results")

results = pd.DataFrame({

    "Model": [
        "Decision Tree",
        "Bagging",
        "Random Forest",
        "AdaBoost",
        "Gradient Boosting"
    ],

    "Train Accuracy": [
        1.0000,
        1.0000,
        1.0000,
        0.9656,
        0.9960
    ],

    "Validation Accuracy": [
        0.9782,
        0.9843,
        0.9796,
        0.9590,
        0.9803
    ],

    "Train F1": [
        1.0000,
        1.0000,
        1.0000,
        0.9722,
        0.9968
    ],

    "Validation F1": [
        0.9825,
        0.9875,
        0.9837,
        0.9669,
        0.9843
    ],

    "Train ROC-AUC": [
        1.0000,
        1.0000,
        1.0000,
        0.9964,
        0.9998
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
    "Train Accuracy",
    "Validation Accuracy",
    "Train F1",
    "Validation F1",
    "Train ROC-AUC",
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
    "Values are mean results from 5-fold stratified cross-validation."
)


st.divider()


# =========================================================
# ACCURACY
# =========================================================

st.header("Accuracy Comparison")

fig, ax = plt.subplots(
    figsize=(10, 5)
)

x = np.arange(
    len(results)
)

width = 0.35

ax.bar(
    x - width / 2,
    results["Train Accuracy"],
    width,
    label="Training"
)

ax.bar(
    x + width / 2,
    results["Validation Accuracy"],
    width,
    label="Validation"
)

ax.set_xticks(x)

ax.set_xticklabels(
    results["Model"],
    rotation=20
)

ax.set_ylabel(
    "Accuracy"
)

ax.set_ylim(
    0,
    1.05
)

ax.set_title(
    "Training vs Validation Accuracy"
)

ax.legend()

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
    x - width / 2,
    results["Train F1"],
    width,
    label="Training"
)

ax.bar(
    x + width / 2,
    results["Validation F1"],
    width,
    label="Validation"
)

ax.set_xticks(x)

ax.set_xticklabels(
    results["Model"],
    rotation=20
)

ax.set_ylabel(
    "F1 Score"
)

ax.set_ylim(
    0,
    1.05
)

ax.set_title(
    "Training vs Validation F1 Score"
)

ax.legend()

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
    x - width / 2,
    results["Train ROC-AUC"],
    width,
    label="Training"
)

ax.bar(
    x + width / 2,
    results["Validation ROC-AUC"],
    width,
    label="Validation"
)

ax.set_xticks(x)

ax.set_xticklabels(
    results["Model"],
    rotation=20
)

ax.set_ylabel(
    "ROC-AUC"
)

ax.set_ylim(
    0,
    1.05
)

ax.set_title(
    "Training vs Validation ROC-AUC"
)

ax.legend()

ax.grid(
    axis="y",
    alpha=0.3
)

st.pyplot(fig)

plt.close(fig)


# =========================================================
# GENERALIZATION GAP
# =========================================================

st.header("Generalization Gap")

gap = pd.DataFrame({

    "Model":
        results["Model"],

    "Accuracy Gap":
        results["Train Accuracy"]
        -
        results["Validation Accuracy"],

    "F1 Gap":
        results["Train F1"]
        -
        results["Validation F1"],

    "ROC-AUC Gap":
        results["Train ROC-AUC"]
        -
        results["Validation ROC-AUC"]
})


gap_display = gap.copy()

for column in [
    "Accuracy Gap",
    "F1 Gap",
    "ROC-AUC Gap"
]:

    gap_display[column] = (
        gap_display[column] * 100
    ).round(2).astype(str) + "%"


st.dataframe(
    gap_display,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# SUMMARY
# =========================================================

st.header("Project Results Summary")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Highest Validation Accuracy",
        "Bagging — 98.43%"
    )

with col2:

    st.metric(
        "Highest Validation F1",
        "Bagging — 98.75%"
    )

with col3:

    st.metric(
        "Highest Validation ROC-AUC",
        "Gradient Boosting — 99.81%"
    )
