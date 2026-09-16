import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Run Bagging vs Boosting Experiment",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 Loan Approval Prediction: Bagging vs Boosting")

st.write(
    "Upload a loan approval dataset and run the complete "
    "Bagging vs Boosting experiment."
)

st.divider()


# =========================================================
# 1. UPLOAD DATASET
# =========================================================

st.header("1. Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload your loan approval CSV file",
    type=["csv"]
)

if uploaded_file is None:

    st.info(
        "Please upload loan_approval_dataset.csv to start."
    )

    st.stop()


# =========================================================
# READ CSV
# =========================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(f"Could not read the CSV file: {e}")

    st.stop()


# Clean column names
df.columns = df.columns.str.strip()


st.success(
    f"Dataset loaded successfully: "
    f"{df.shape[0]} rows × {df.shape[1]} columns"
)


# =========================================================
# 2. DATASET PREVIEW
# =========================================================

st.header("2. Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# BASIC DATASET INFORMATION
# =========================================================

with st.expander("View Dataset Information"):

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
# 3. TARGET COLUMN
# =========================================================

st.header("3. Select Target Column")


# Automatically select loan_status
if "loan_status" in df.columns:

    target_column = "loan_status"

    st.info(
        "Target column automatically selected: loan_status"
    )

else:

    target_column = st.selectbox(
        "Select the target column",
        df.columns
    )


# =========================================================
# PREPARE DATA
# =========================================================

data = df.copy()


# Remove rows with missing values
before_rows = len(data)

data = data.dropna()

removed_rows = before_rows - len(data)


if removed_rows > 0:

    st.warning(
        f"{removed_rows} rows with missing values were removed."
    )


# =========================================================
# TARGET PROCESSING
# =========================================================

y_raw = data[target_column].astype(str).str.strip()


# ---------------------------------------------------------
# Loan dataset target
# ---------------------------------------------------------

if target_column == "loan_status":

    target_mapping = {
        "Approved": 1,
        "Rejected": 0,
        "APPROVED": 1,
        "REJECTED": 0,
        "approved": 1,
        "rejected": 0
    }

    y = y_raw.map(target_mapping)

    # Check for unknown target values

    if y.isna().any():

        unknown_values = y_raw[y.isna()].unique()

        st.error(
            "Unknown values found in loan_status: "
            + str(list(unknown_values))
        )

        st.stop()


# ---------------------------------------------------------
# Generic binary target
# ---------------------------------------------------------

else:

    unique_values = y_raw.unique()

    if len(unique_values) != 2:

        st.error(
            "The selected target must contain exactly "
            f"2 classes. Found {len(unique_values)} classes."
        )

        st.write(
            "Classes found:",
            list(unique_values)
        )

        st.stop()


    class_mapping = {
        unique_values[0]: 0,
        unique_values[1]: 1
    }

    y = y_raw.map(class_mapping)


# Convert target to integer
y = y.astype(int)


# =========================================================
# TARGET DISTRIBUTION
# =========================================================

st.subheader("Target Distribution")

class_counts = y.value_counts().sort_index()


target_names = []

if target_column == "loan_status":

    target_names = []

    for value in class_counts.index:

        if value == 0:
            target_names.append("Rejected")

        else:
            target_names.append("Approved")

else:

    target_names = [
        str(value)
        for value in class_counts.index
    ]


target_distribution = pd.DataFrame({
    "Class": target_names,
    "Count": class_counts.values
})


st.dataframe(
    target_distribution,
    use_container_width=True,
    hide_index=True
)


# Make sure binary
if len(class_counts) != 2:

    st.error(
        "This experiment requires a binary classification target."
    )

    st.stop()


# Make sure enough samples for 5 folds
if class_counts.min() < 5:

    st.error(
        "Each class must contain at least 5 samples "
        "for 5-fold cross-validation."
    )

    st.stop()


# =========================================================
# 4. FEATURES
# =========================================================

st.header("4. Feature Preparation")


X = data.drop(
    columns=[target_column]
)


# Remove loan_id
if "loan_id" in X.columns:

    X = X.drop(
        columns=["loan_id"]
    )


# Identify categorical columns
categorical_columns = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()


# Identify numerical columns
numerical_columns = X.select_dtypes(
    exclude=["object", "category"]
).columns.tolist()


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


st.write(
    "**Numerical columns:**",
    numerical_columns
)

st.write(
    "**Categorical columns:**",
    categorical_columns
)


# =========================================================
# PREPROCESSOR
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
# 5. MODELS
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
# 6. RUN EXPERIMENT
# =========================================================

st.divider()

st.header("5. Run Experiment")


st.write(
    "The experiment uses 5-fold Stratified Cross-Validation "
    "to compare all five models."
)


run_experiment = st.button(
    "🚀 Run Bagging vs Boosting Experiment",
    type="primary"
)


if run_experiment:

    st.divider()

    st.header("6. Training Models")

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )


    results = []


    progress_bar = st.progress(0)


    status_text = st.empty()


    total_models = len(models)


    # =====================================================
    # TRAIN EACH MODEL
    # =====================================================

    for index, (name, classifier) in enumerate(
        models.items()
    ):

        status_text.write(
            f"Training **{name}**..."
        )


        pipeline = Pipeline(
            steps=[

                (
                    "preprocessor",
                    preprocessor
                ),

                (
                    "model",
                    classifier
                )
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

            n_jobs=1
        )


        results.append({

            "Model":
                name,

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


        progress_bar.progress(
            int(
                ((index + 1) / total_models) * 100
            )
        )


    status_text.success(
        "All five models completed successfully."
    )


    # =====================================================
    # RESULTS DATAFRAME
    # =====================================================

    results_df = pd.DataFrame(
        results
    )


    # =====================================================
    # 7. PERFORMANCE TABLE
    # =====================================================

    st.header("7. Model Performance Comparison")


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


    st.caption(
        "Values represent the mean score across 5 stratified folds."
    )


    # =====================================================
    # 8. ACCURACY GRAPH
    # =====================================================

    st.header("8. Accuracy Comparison")


    x = np.arange(
        len(results_df)
    )


    width = 0.35


    fig, ax = plt.subplots(
        figsize=(10, 5)
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


    ax.set_xticks(x)


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


    st.pyplot(
        fig
    )


    plt.close(fig)


    # =====================================================
    # 9. F1 GRAPH
    # =====================================================

    st.header("9. F1 Score Comparison")


    fig, ax = plt.subplots(
        figsize=(10, 5)
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


    ax.set_xticks(x)


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


    st.pyplot(
        fig
    )


    plt.close(fig)


    # =====================================================
    # 10. ROC-AUC GRAPH
    # =====================================================

    st.header("10. ROC-AUC Comparison")


    fig, ax = plt.subplots(
        figsize=(10, 5)
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


    ax.set_xticks(x)


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


    st.pyplot(
        fig
    )


    plt.close(fig)


    # =====================================================
    # 11. GENERALIZATION GAP
    # =====================================================

    st.header("11. Generalization Gap")


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


    # =====================================================
    # 12. INTERPRETATION
    # =====================================================

    st.header("12. Experiment Summary")


    best_accuracy_index = results_df[
        "Validation Accuracy"
    ].idxmax()


    best_f1_index = results_df[
        "Validation F1"
    ].idxmax()


    best_auc_index = results_df[
        "Validation ROC-AUC"
    ].idxmax()


    best_accuracy_model = results_df.loc[
        best_accuracy_index,
        "Model"
    ]


    best_f1_model = results_df.loc[
        best_f1_index,
        "Model"
    ]


    best_auc_model = results_df.loc[
        best_auc_index,
        "Model"
    ]


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Highest Validation Accuracy",
            best_accuracy_model
        )


    with col2:

        st.metric(
            "Highest Validation F1",
            best_f1_model
        )


    with col3:

        st.metric(
            "Highest Validation ROC-AUC",
            best_auc_model
        )


    st.info(
        "The results above are calculated directly from "
        "the uploaded dataset. They are not hard-coded."
    )


    # =====================================================
    # 13. DOWNLOAD RESULTS
    # =====================================================

    st.header("13. Download Results")


    csv_data = results_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        label="⬇️ Download Model Results CSV",

        data=csv_data,

        file_name="model_comparison_results.csv",

        mime="text/csv"
    )
