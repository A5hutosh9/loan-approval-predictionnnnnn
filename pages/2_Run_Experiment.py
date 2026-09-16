import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_validate
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

import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Run Bagging vs Boosting Experiment",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Run Bagging vs Boosting Experiment")

st.write(
    "Upload a loan approval CSV dataset and run the complete "
    "ensemble learning experiment."
)

st.divider()


# =========================================================
# UPLOAD DATASET
# =========================================================

st.header("1. Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is None:

    st.info(
        "Upload a CSV file to start the experiment."
    )

    st.stop()


# =========================================================
# READ DATA
# =========================================================

try:
    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(f"Unable to read the CSV file: {e}")
    st.stop()


# Remove spaces from column names
df.columns = df.columns.str.strip()


st.success(
    f"Dataset loaded successfully: {df.shape[0]} rows × {df.shape[1]} columns"
)


# =========================================================
# DATASET PREVIEW
# =========================================================

st.header("2. Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)


# =========================================================
# TARGET COLUMN
# =========================================================

st.header("3. Select Target Column")

target_column = st.selectbox(
    "Select the column you want to predict",
    df.columns
)


# =========================================================
# REMOVE MISSING VALUES
# =========================================================

data = df.copy()

data = data.dropna()

if len(data) < len(df):

    st.warning(
        f"{len(df) - len(data)} rows containing missing values "
        "were removed."
    )


# =========================================================
# TARGET PROCESSING
# =========================================================

y_raw = data[target_column]


# Convert common loan status labels
if y_raw.dtype == "object":

    unique_values = y_raw.astype(str).str.strip().unique()

    mapping = {
        "Approved": 1,
        "Rejected": 0,
        "approved": 1,
        "rejected": 0,
        "Yes": 1,
        "No": 0,
        "yes": 1,
        "no": 0
    }

    if all(value in mapping for value in unique_values):

        y = y_raw.astype(str).str.strip().map(mapping)

    else:

        # Generic binary encoding
        if len(unique_values) != 2:

            st.error(
                "Target column must contain exactly two classes."
            )

            st.stop()

        class_mapping = {
            unique_values[0]: 0,
            unique_values[1]: 1
        }

        y = y_raw.astype(str).str.strip().map(class_mapping)

else:

    y = y_raw


# Remove rows where target couldn't be converted
valid_rows = y.notna()

data = data.loc[valid_rows].copy()
y = y.loc[valid_rows].astype(int)


# =========================================================
# FEATURES
# =========================================================

X = data.drop(columns=[target_column])


# Remove loan_id if present
if "loan_id" in X.columns:

    X = X.drop(columns=["loan_id"])


# =========================================================
# IDENTIFY COLUMNS
# =========================================================

categorical_columns = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    exclude=["object", "category"]
).columns.tolist()


st.write("**Numerical features:**", len(numerical_columns))
st.write("**Categorical features:**", len(categorical_columns))


# =========================================================
# PREPROCESSING
# =========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            "passthrough",
            numerical_columns
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_columns
        )
    ]
)


# =========================================================
# MODELS
# =========================================================

models = {

    "Decision Tree": DecisionTreeClassifier(
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42
    ),

    "Bagging": BaggingClassifier(
        estimator=DecisionTreeClassifier(
            max_depth=None,
            min_samples_split=2,
            random_state=42
        ),
        n_estimators=100,
        max_samples=1.0,
        bootstrap=True,
        random_state=42,
        n_jobs=-1
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "AdaBoost": AdaBoostClassifier(
        estimator=DecisionTreeClassifier(
            max_depth=1,
            random_state=42
        ),
        n_estimators=100,
        learning_rate=0.5,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
}


# =========================================================
# RUN EXPERIMENT BUTTON
# =========================================================

st.divider()

run_experiment = st.button(
    "🚀 Run Bagging vs Boosting Experiment",
    type="primary"
)


if run_experiment:

    st.header("4. Training Models")

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    results = []

    progress = st.progress(0)

    total_models = len(models)

    for index, (name, classifier) in enumerate(models.items()):

        st.write(f"Training **{name}**...")

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", classifier)
            ]
        )

        scores = cross_validate(
            pipeline,
            X,
            y,
            cv=cv,
            scoring=[
                "accuracy",
                "f1",
                "roc_auc"
            ],
            return_train_score=True,
            n_jobs=-1
        )

        results.append({

            "Model": name,

            "Train Accuracy":
                scores["train_accuracy"].mean(),

            "Validation Accuracy":
                scores["test_accuracy"].mean(),

            "Train F1":
                scores["train_f1"].mean(),

            "Validation F1":
                scores["test_f1"].mean(),

            "Train ROC-AUC":
                scores["train_roc_auc"].mean(),

            "Validation ROC-AUC":
                scores["test_roc_auc"].mean()
        })

        progress.progress(
            int((index + 1) / total_models * 100)
        )


    # =====================================================
    # RESULTS
    # =====================================================

    results_df = pd.DataFrame(results)

    st.success("All models trained successfully.")


    # =====================================================
    # RESULTS TABLE
    # =====================================================

    st.header("5. Model Performance")

    display_df = results_df.copy()

    percentage_columns = [
        "Train Accuracy",
        "Validation Accuracy",
        "Train F1",
        "Validation F1",
        "Train ROC-AUC",
        "Validation ROC-AUC"
    ]

    for column in percentage_columns:

        display_df[column] = (
            display_df[column] * 100
        ).round(2).astype(str) + "%"


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # ACCURACY GRAPH
    # =====================================================

    st.header("6. Accuracy Comparison")

    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(results_df))

    width = 0.35

    ax.bar(
        x - width / 2,
        results_df["Train Accuracy"],
        width,
        label="Training"
    )

    ax.bar(
        x + width / 2,
        results_df["Validation Accuracy"],
        width,
        label="Validation"
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        results_df["Model"],
        rotation=20
    )

    ax.set_ylabel("Accuracy")

    ax.set_ylim(0, 1.05)

    ax.set_title(
        "Training vs Validation Accuracy"
    )

    ax.legend()

    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # F1 GRAPH
    # =====================================================

    st.header("7. F1 Score Comparison")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        x - width / 2,
        results_df["Train F1"],
        width,
        label="Training"
    )

    ax.bar(
        x + width / 2,
        results_df["Validation F1"],
        width,
        label="Validation"
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        results_df["Model"],
        rotation=20
    )

    ax.set_ylabel("F1 Score")

    ax.set_ylim(0, 1.05)

    ax.set_title(
        "Training vs Validation F1 Score"
    )

    ax.legend()

    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # ROC-AUC GRAPH
    # =====================================================

    st.header("8. ROC-AUC Comparison")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        x - width / 2,
        results_df["Train ROC-AUC"],
        width,
        label="Training"
    )

    ax.bar(
        x + width / 2,
        results_df["Validation ROC-AUC"],
        width,
        label="Validation"
    )

    ax.set_xticks(x)

    ax.set_xticklabels(
        results_df["Model"],
        rotation=20
    )

    ax.set_ylabel("ROC-AUC")

    ax.set_ylim(0, 1.05)

    ax.set_title(
        "Training vs Validation ROC-AUC"
    )

    ax.legend()

    ax.grid(axis="y", alpha=0.3)

    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # GENERALIZATION GAP
    # =====================================================

    st.header("9. Generalization Gap")

    gap_df = pd.DataFrame({

        "Model": results_df["Model"],

        "Accuracy Gap":
            results_df["Train Accuracy"]
            - results_df["Validation Accuracy"],

        "F1 Gap":
            results_df["Train F1"]
            - results_df["Validation F1"],

        "ROC-AUC Gap":
            results_df["Train ROC-AUC"]
            - results_df["Validation ROC-AUC"]
    })

    gap_display = gap_df.copy()

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


    # =====================================================
    # DOWNLOAD RESULTS
    # =====================================================

    st.header("10. Download Results")

    csv = results_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Experiment Results",
        data=csv,
        file_name="model_comparison_results.csv",
        mime="text/csv"
    )
