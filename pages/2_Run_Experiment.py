import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate,
    cross_val_predict
)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    BaggingClassifier,
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier
)

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    roc_curve
)

from utils import normalize_binary_target


st.set_page_config(
    page_title="Run Experiment",
    page_icon="🧪",
    layout="wide"
)


st.title("🧪 Run Experiment")

st.markdown(
    """
    Upload your own loan approval dataset and compare
    Bagging and Boosting models automatically.
    """
)


# ==========================================================
# UPLOAD DATASET
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)


if uploaded_file is None:

    st.info(
        "Upload a CSV file to start a new experiment."
    )

    st.markdown(
        """
        ### Supported Dataset Structure

        Your dataset should contain:

        - One binary target column
        - Numerical and/or categorical features
        - Common target labels such as:
          - Approved / Rejected
          - Yes / No
          - 1 / 0
          - True / False
        """
    )

    st.stop()


# ==========================================================
# READ DATA
# ==========================================================

try:

    df = pd.read_csv(uploaded_file)

    df.columns = df.columns.str.strip()

except Exception as e:

    st.error(f"Could not read the CSV file: {e}")

    st.stop()


# ==========================================================
# DATASET EXPANDER
# ==========================================================

with st.expander("📁 Uploaded Dataset"):

    st.write(
        f"**Rows:** {df.shape[0]} | "
        f"**Columns:** {df.shape[1]}"
    )

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================================================
# TARGET SELECTION
# ==========================================================

st.header("🎯 Select Target Column")

target_column = st.selectbox(
    "Choose the column containing loan approval status:",
    df.columns
)


# ==========================================================
# PREPARE TARGET
# ==========================================================

try:

    y, target_mapping = normalize_binary_target(
        df[target_column]
    )

except Exception as e:

    st.error(str(e))

    st.stop()


# Remove missing target rows
valid_rows = y.notna()

df = df.loc[valid_rows].copy()
y = y.loc[valid_rows].astype(int)


# ==========================================================
# FEATURES
# ==========================================================

X = df.drop(columns=[target_column])


# Drop likely ID columns
id_columns = []

for col in X.columns:

    name = col.lower().replace("_", "").replace(" ", "")

    if name in [
        "id",
        "loanid",
        "applicationid",
        "customerid",
        "applicantid"
    ]:

        id_columns.append(col)


if id_columns:

    X = X.drop(columns=id_columns)

    st.info(
        f"Automatically removed ID column(s): "
        f"{', '.join(id_columns)}"
    )


# ==========================================================
# REMOVE COMPLETELY EMPTY COLUMNS
# ==========================================================

empty_columns = [
    col for col in X.columns
    if X[col].isna().all()
]

if empty_columns:

    X = X.drop(columns=empty_columns)

    st.warning(
        f"Removed completely empty columns: "
        f"{', '.join(empty_columns)}"
    )


# ==========================================================
# DETECT FEATURES
# ==========================================================

numeric_features = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_features = X.select_dtypes(
    exclude=["number"]
).columns.tolist()


st.header("🔍 Detected Features")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Numerical Features")

    if numeric_features:
        st.write(numeric_features)
    else:
        st.write("None")


with col2:

    st.subheader("Categorical Features")

    if categorical_features:
        st.write(categorical_features)
    else:
        st.write("None")


# ==========================================================
# CLASS DISTRIBUTION
# ==========================================================

st.header("📊 Target Distribution")

target_counts = y.value_counts().sort_index()

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Class 0",
        int(target_counts.get(0, 0))
    )

with col2:

    st.metric(
        "Class 1",
        int(target_counts.get(1, 0))
    )


# ==========================================================
# PREPROCESSING
# ==========================================================

numeric_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    )
])


categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="most_frequent")
    ),

    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])


transformers = []


if numeric_features:

    transformers.append(
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        )
    )


if categorical_features:

    transformers.append(
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    )


preprocessor = ColumnTransformer(
    transformers=transformers
)


# ==========================================================
# MODELS
# ==========================================================

models = {

    "Decision Tree":
        DecisionTreeClassifier(
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42
        ),

    "Bagging":
        BaggingClassifier(
            estimator=DecisionTreeClassifier(
                max_depth=None,
                min_samples_split=2,
                random_state=42
            ),
            n_estimators=100,
            bootstrap=True,
            random_state=42,
            n_jobs=1
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features="sqrt",
            random_state=42,
            n_jobs=1
        ),

    "AdaBoost":
        AdaBoostClassifier(
            estimator=DecisionTreeClassifier(
                max_depth=1,
                random_state=42
            ),
            n_estimators=100,
            learning_rate=0.5,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
}


# ==========================================================
# RUN BUTTON
# ==========================================================

st.markdown("---")

run_experiment = st.button(
    "🚀 Run Experiment",
    type="primary",
    use_container_width=True
)


if not run_experiment:

    st.stop()


# ==========================================================
# CHECK DATA
# ==========================================================

if len(X) < 20:

    st.error(
        "Dataset is too small for a meaningful experiment."
    )

    st.stop()


class_counts = y.value_counts()

if len(class_counts) != 2:

    st.error(
        "The target column must contain exactly two classes."
    )

    st.stop()


min_class_count = int(class_counts.min())

if min_class_count < 2:

    st.error(
        "Each class must contain at least 2 samples."
    )

    st.stop()


n_splits = min(
    5,
    min_class_count
)


# ==========================================================
# CROSS VALIDATION
# ==========================================================

cv = StratifiedKFold(
    n_splits=n_splits,
    shuffle=True,
    random_state=42
)


results = []

roc_data = {}


progress = st.progress(0)

model_items = list(models.items())


for index, (model_name, model) in enumerate(model_items):

    pipeline = Pipeline([
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ])


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
        n_jobs=1
    )


    train_accuracy = scores[
        "train_accuracy"
    ].mean()

    validation_accuracy = scores[
        "test_accuracy"
    ].mean()


    train_f1 = scores[
        "train_f1"
    ].mean()

    validation_f1 = scores[
        "test_f1"
    ].mean()


    train_auc = scores[
        "train_roc_auc"
    ].mean()

    validation_auc = scores[
        "test_roc_auc"
    ].mean()


    results.append({

        "Model": model_name,

        "Train Accuracy":
            train_accuracy,

        "Validation Accuracy":
            validation_accuracy,

        "Train F1":
            train_f1,

        "Validation F1":
            validation_f1,

        "Train ROC-AUC":
            train_auc,

        "Validation ROC-AUC":
            validation_auc,

        "Accuracy Gap":
            train_accuracy - validation_accuracy,

        "F1 Gap":
            train_f1 - validation_f1,

        "ROC-AUC Gap":
            train_auc - validation_auc
    })


    # ROC predictions
    probabilities = cross_val_predict(
        pipeline,
        X,
        y,
        cv=cv,
        method="predict_proba",
        n_jobs=1
    )[:, 1]


    fpr, tpr, _ = roc_curve(
        y,
        probabilities
    )


    roc_data[model_name] = (
        fpr,
        tpr,
        validation_auc
    )


    progress.progress(
        (index + 1) / len(model_items)
    )


# ==========================================================
# RESULTS DATAFRAME
# ==========================================================

results_df = pd.DataFrame(results)


st.success(
    "Experiment completed successfully."
)


# ==========================================================
# RESULTS TABLE
# ==========================================================

st.header("📋 Model Results")

st.dataframe(
    results_df.style.format(
        {
            "Train Accuracy": "{:.4f}",
            "Validation Accuracy": "{:.4f}",
            "Train F1": "{:.4f}",
            "Validation F1": "{:.4f}",
            "Train ROC-AUC": "{:.4f}",
            "Validation ROC-AUC": "{:.4f}",
            "Accuracy Gap": "{:.4f}",
            "F1 Gap": "{:.4f}",
            "ROC-AUC Gap": "{:.4f}"
        }
    ),
    use_container_width=True
)


# ==========================================================
# ACCURACY
# ==========================================================

st.header("📊 Accuracy Comparison")

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
ax.set_title("Training vs Validation Accuracy")
ax.legend()

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# F1
# ==========================================================

st.header("📊 F1-Score Comparison")

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
ax.set_title("Training vs Validation F1")
ax.legend()

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# ROC-AUC
# ==========================================================

st.header("📊 ROC-AUC Comparison")

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
ax.set_title("Training vs Validation ROC-AUC")
ax.legend()

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# GENERALIZATION GAP
# ==========================================================

st.header("🔎 Generalization Gap")

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    results_df["Model"],
    results_df["Accuracy Gap"]
)

ax.set_ylabel("Training − Validation Accuracy")
ax.set_title("Accuracy Generalization Gap")

plt.xticks(rotation=20)

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# ROC CURVES
# ==========================================================

st.header("📈 ROC Curves")

fig, ax = plt.subplots(figsize=(9, 7))

for model_name, (
    fpr,
    tpr,
    auc
) in roc_data.items():

    ax.plot(
        fpr,
        tpr,
        label=f"{model_name} (AUC={auc:.3f})"
    )


ax.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")

ax.set_title("Cross-Validated ROC Curves")

ax.legend()

plt.tight_layout()

st.pyplot(fig)


# ==========================================================
# DOWNLOAD RESULTS
# ==========================================================

st.header("⬇️ Download Results")

csv = results_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    "Download Experiment Results",
    data=csv,
    file_name="loan_experiment_results.csv",
    mime="text/csv"
)
