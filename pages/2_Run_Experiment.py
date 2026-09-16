import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import (
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
    roc_curve,
    auc,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from utils import (
    load_repository_dataset,
    show_dataset_expander,
    normalize_binary_target
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Run Experiment",
    page_icon="🧪",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("🧪 Run Bagging vs Boosting Experiment")

st.write(
    """
    Upload a compatible loan approval CSV dataset and run the
    complete ensemble learning experiment.
    """
)


st.info(
    """
    This page calculates new results from the uploaded CSV.
    The results are not hard-coded.
    """
)


# =========================================================
# REPOSITORY DATASET
# =========================================================

st.divider()


# =========================================================
# UPLOAD DATASET
# =========================================================

st.header("1. Upload Dataset")


uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)


if uploaded_file is None:

    st.warning(
        "Upload a CSV file to run the experiment."
    )

    st.stop()


# =========================================================
# READ DATASET
# =========================================================

try:

    df = pd.read_csv(
        uploaded_file
    )

except Exception as error:

    st.error(
        f"Could not read the CSV file: {error}"
    )

    st.stop()


df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


st.success(
    f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns"
)


# =========================================================
# UPLOADED DATASET EXPANDER
# =========================================================

with st.expander("📁 Uploaded Dataset"):

    st.dataframe(
        df,
        use_container_width=True,
        height=450,
        hide_index=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:
        st.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )


# =========================================================
# TARGET SELECTION
# =========================================================

st.header("2. Target Selection")


# Try to automatically identify a likely target
target_candidates = [

    column
    for column in df.columns

    if any(
        keyword in column.lower()
        for keyword in [
            "loan_status",
            "loan_status",
            "approval",
            "approved",
            "status",
            "target"
        ]
    )
]


if target_candidates:

    default_target = target_candidates[0]

    target_index = list(
        df.columns
    ).index(
        default_target
    )

else:

    target_index = 0


target_column = st.selectbox(
    "Select the target column",
    df.columns,
    index=target_index
)


# =========================================================
# TARGET PREPARATION
# =========================================================

target_series = df[target_column]


# Remove rows with missing target
valid_target_rows = (
    target_series.notna()
)

data = df.loc[
    valid_target_rows
].copy()


target_series = data[
    target_column
]


y, target_mapping = normalize_binary_target(
    target_series
)


if y is None:

    st.error(
        """
        The selected target could not be converted into a
        binary classification problem.

        The target must contain exactly two classes, for example:
        Approved / Rejected
        Yes / No
        1 / 0
        """
    )

    st.write(
        "Values found in the target:"
    )

    st.write(
        target_series.unique()
    )

    st.stop()


# =========================================================
# TARGET DISTRIBUTION
# =========================================================

st.subheader("Target Distribution")


class_counts = y.value_counts().sort_index()


distribution = pd.DataFrame({
    "Class": [
        "Class 0",
        "Class 1"
    ],

    "Count": [
        class_counts.get(0, 0),
        class_counts.get(1, 0)
    ]
})


if target_mapping is not None:

    mapping_text = ", ".join(
        [
            f"{key} → {value}"
            for key, value in target_mapping.items()
        ]
    )

    st.caption(
        f"Target mapping: {mapping_text}"
    )


st.dataframe(
    distribution,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CHECK CLASS COUNTS
# =========================================================

if len(class_counts) != 2:

    st.error(
        "The target must contain exactly two classes."
    )

    st.stop()


minimum_class_count = class_counts.min()


if minimum_class_count < 2:

    st.error(
        "At least two samples are required in each class."
    )

    st.stop()


# =========================================================
# FEATURES
# =========================================================

st.header("3. Feature Preparation")


X = data.drop(
    columns=[target_column]
)


# Remove common ID columns
id_columns = [

    column

    for column in X.columns

    if column.lower() in [
        "id",
        "loan_id",
        "customer_id",
        "application_id",
        "applicant_id"
    ]
]


if id_columns:

    X = X.drop(
        columns=id_columns
    )


# Detect categorical columns
categorical_columns = (
    X.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    )
    .columns
    .tolist()
)


# Detect numerical columns
numerical_columns = (
    X.select_dtypes(
        include=np.number
    )
    .columns
    .tolist()
)


if len(X.columns) == 0:

    st.error(
        "No usable feature columns remain after removing the target."
    )

    st.stop()


if len(numerical_columns) == 0 and len(categorical_columns) == 0:

    st.error(
        "No numerical or categorical features were detected."
    )

    st.stop()


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Numerical Features",
        len(numerical_columns)
    )


with col2:

    st.metric(
        "Categorical Features",
        len(categorical_columns)
    )


with st.expander("View Detected Features"):

    st.write(
        "**Numerical:**",
        numerical_columns
    )

    st.write(
        "**Categorical:**",
        categorical_columns
    )


# =========================================================
# PREPROCESSOR
# =========================================================

transformers = []


if numerical_columns:

    numerical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            )
        ]
    )

    transformers.append(
        (
            "num",
            numerical_pipeline,
            numerical_columns
        )
    )


if categorical_columns:

    categorical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    transformers.append(
        (
            "cat",
            categorical_pipeline,
            categorical_columns
        )
    )


preprocessor = ColumnTransformer(
    transformers=transformers
)


# =========================================================
# MODELS
# =========================================================

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
            max_samples=1.0,
            bootstrap=True,
            random_state=42,
            n_jobs=-1
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            max_features="sqrt",
            random_state=42,
            n_jobs=-1
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


# =========================================================
# CROSS VALIDATION
# =========================================================

number_of_folds = min(
    5,
    int(minimum_class_count)
)


if number_of_folds < 2:

    st.error(
        "Not enough samples for cross-validation."
    )

    st.stop()


cv = StratifiedKFold(
    n_splits=number_of_folds,
    shuffle=True,
    random_state=42
)


st.info(
    f"Using {number_of_folds}-fold stratified cross-validation."
)


# =========================================================
# RUN EXPERIMENT
# =========================================================

st.header("4. Run Experiment")


run_experiment = st.button(
    "🚀 Run Bagging vs Boosting Experiment",
    type="primary"
)


if not run_experiment:

    st.stop()


# =========================================================
# TRAIN MODELS
# =========================================================

results = []

roc_data = {}

progress = st.progress(0)

status = st.empty()


for index, (
    model_name,
    model
) in enumerate(models.items()):

    status.write(
        f"Training **{model_name}**..."
    )


    pipeline = Pipeline(
        steps=[

            (
                "preprocessor",
                preprocessor
            ),

            (
                "model",
                model
            )
        ]
    )


    # -----------------------------------------------------
    # CROSS VALIDATION METRICS
    # -----------------------------------------------------

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


    results.append({

        "Model":
            model_name,

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


    # -----------------------------------------------------
    # ROC CURVE
    # -----------------------------------------------------

    probabilities = cross_val_predict(

        pipeline,

        X,

        y,

        cv=cv,

        method="predict_proba",

        n_jobs=1
    )[:, 1]


    false_positive_rate, true_positive_rate, _ = (
        roc_curve(
            y,
            probabilities
        )
    )


    roc_auc_value = auc(
        false_positive_rate,
        true_positive_rate
    )


    roc_data[model_name] = (
        false_positive_rate,
        true_positive_rate,
        roc_auc_value
    )


    progress.progress(
        int(
            ((index + 1) / len(models)) * 100
        )
    )


status.success(
    "All models completed successfully."
)


# =========================================================
# RESULTS DATAFRAME
# =========================================================

results_df = pd.DataFrame(
    results
)


# =========================================================
# MODEL PERFORMANCE TABLE
# =========================================================

st.divider()

st.header("5. Model Performance")


display_df = results_df.copy()


for column in [

    "Train Accuracy",
    "Validation Accuracy",
    "Train F1",
    "Validation F1",
    "Train ROC-AUC",
    "Validation ROC-AUC"

]:

    display_df[column] = (
        display_df[column] * 100
    ).round(2).astype(str) + "%"


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


st.caption(
    "Values are mean scores across the cross-validation folds."
)


# =========================================================
# ACCURACY GRAPH
# =========================================================

st.header("6. Accuracy Comparison")


x = np.arange(
    len(results_df)
)

width = 0.35


fig, ax = plt.subplots(
    figsize=(11, 5)
)


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


ax.set_xticks(
    x
)


ax.set_xticklabels(
    results_df["Model"],
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
# F1 GRAPH
# =========================================================

st.header("7. F1 Score Comparison")


fig, ax = plt.subplots(
    figsize=(11, 5)
)


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


ax.set_xticks(
    x
)


ax.set_xticklabels(
    results_df["Model"],
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
# ROC-AUC GRAPH
# =========================================================

st.header("8. ROC-AUC Comparison")


fig, ax = plt.subplots(
    figsize=(11, 5)
)


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


ax.set_xticks(
    x
)


ax.set_xticklabels(
    results_df["Model"],
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

st.header("9. Generalization Gap")


gap_df = pd.DataFrame({

    "Model":
        results_df["Model"],

    "Accuracy Gap":
        results_df["Train Accuracy"]
        -
        results_df["Validation Accuracy"],

    "F1 Gap":
        results_df["Train F1"]
        -
        results_df["Validation F1"],

    "ROC-AUC Gap":
        results_df["Train ROC-AUC"]
        -
        results_df["Validation ROC-AUC"]
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


# =========================================================
# ROC CURVES
# =========================================================

st.header("10. ROC Curves")


fig, ax = plt.subplots(
    figsize=(10, 6)
)


for model_name, (
    fpr,
    tpr,
    roc_auc_value
) in roc_data.items():

    ax.plot(
        fpr,
        tpr,
        label=f"{model_name} (AUC = {roc_auc_value:.4f})"
    )


ax.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)


ax.set_xlabel(
    "False Positive Rate"
)


ax.set_ylabel(
    "True Positive Rate"
)


ax.set_title(
    "ROC Curves"
)


ax.legend()


ax.grid(
    alpha=0.3
)


st.pyplot(fig)

plt.close(fig)


# =========================================================
# BEST RESULTS
# =========================================================

st.header("11. Experiment Summary")


accuracy_index = results_df[
    "Validation Accuracy"
].idxmax()


f1_index = results_df[
    "Validation F1"
].idxmax()


auc_index = results_df[
    "Validation ROC-AUC"
].idxmax()


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Highest Validation Accuracy",
        results_df.loc[
            accuracy_index,
            "Model"
        ],
        f"{results_df.loc[accuracy_index, 'Validation Accuracy'] * 100:.2f}%"
    )


with col2:

    st.metric(
        "Highest Validation F1",
        results_df.loc[
            f1_index,
            "Model"
        ],
        f"{results_df.loc[f1_index, 'Validation F1'] * 100:.2f}%"
    )


with col3:

    st.metric(
        "Highest Validation ROC-AUC",
        results_df.loc[
            auc_index,
            "Model"
        ],
        f"{results_df.loc[auc_index, 'Validation ROC-AUC'] * 100:.2f}%"
    )


# =========================================================
# DOWNLOAD
# =========================================================

st.divider()

st.header("12. Download Results")


csv_results = results_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    "⬇️ Download Experiment Results",
    data=csv_results,
    file_name="model_comparison_results.csv",
    mime="text/csv"
)
