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
    page_title="Run Experiment",
    page_icon="🧪",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🧪 Run Bagging vs Boosting Experiment")

st.write(
    "Upload a CSV dataset and automatically train and compare "
    "Decision Tree, Bagging, Random Forest, AdaBoost and "
    "Gradient Boosting."
)

st.divider()


# =========================================================
# UPLOAD DATASET
# =========================================================

st.header("1. Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


if uploaded_file is None:

    st.info(
        "Upload a CSV file to start the experiment."
    )

    st.stop()


# =========================================================
# READ DATASET
# =========================================================

try:

    df = pd.read_csv(
        uploaded_file
    )

except Exception as e:

    st.error(
        f"Could not read CSV: {e}"
    )

    st.stop()


df.columns = df.columns.str.strip()


st.success(
    f"Dataset loaded successfully: "
    f"{df.shape[0]} rows × {df.shape[1]} columns"
)


# =========================================================
# DATASET EXPANDER
# =========================================================

with st.expander("📁 Dataset — Click to View"):

    st.write(
        f"Rows: **{df.shape[0]}**"
    )

    st.write(
        f"Columns: **{df.shape[1]}**"
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=500,
        hide_index=True
    )


st.divider()


# =========================================================
# TARGET
# =========================================================

st.header("2. Target Column")


if "loan_status" in df.columns:

    target_column = "loan_status"

    st.info(
        "loan_status automatically selected as target."
    )

else:

    target_column = st.selectbox(
        "Select target column",
        df.columns
    )


# =========================================================
# CLEAN DATA
# =========================================================

data = df.copy()

before_rows = len(data)

data = data.dropna()

removed_rows = before_rows - len(data)


if removed_rows > 0:

    st.warning(
        f"{removed_rows} rows containing missing values "
        "were removed."
    )


# =========================================================
# TARGET PROCESSING
# =========================================================

y_raw = (
    data[target_column]
    .astype(str)
    .str.strip()
)


if target_column == "loan_status":

    mapping = {
        "Approved": 1,
        "Rejected": 0,
        "APPROVED": 1,
        "REJECTED": 0,
        "approved": 1,
        "rejected": 0
    }

    y = y_raw.map(
        mapping
    )

    if y.isna().any():

        unknown = y_raw[
            y.isna()
        ].unique()

        st.error(
            f"Unknown loan_status values: {list(unknown)}"
        )

        st.stop()


else:

    unique_values = y_raw.unique()

    if len(unique_values) != 2:

        st.error(
            "The target must contain exactly two classes."
        )

        st.write(
            "Classes found:",
            list(unique_values)
        )

        st.stop()


    mapping = {
        unique_values[0]: 0,
        unique_values[1]: 1
    }

    y = y_raw.map(
        mapping
    )


y = y.astype(int)


# =========================================================
# TARGET DISTRIBUTION
# =========================================================

st.header("3. Target Distribution")

counts = y.value_counts()


if len(counts) != 2:

    st.error(
        "Binary classification is required."
    )

    st.stop()


st.dataframe(
    pd.DataFrame({
        "Class": counts.index,
        "Count": counts.values
    }),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FEATURES
# =========================================================

X = data.drop(
    columns=[target_column]
)


if "loan_id" in X.columns:

    X = X.drop(
        columns=["loan_id"]
    )


categorical_columns = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()


numerical_columns = X.select_dtypes(
    exclude=["object", "category"]
).columns.tolist()


st.header("4. Feature Information")

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
    "Numerical:",
    numerical_columns
)

st.write(
    "Categorical:",
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
# RUN
# =========================================================

st.divider()

st.header("5. Run Experiment")

run = st.button(
    "🚀 Run Experiment",
    type="primary"
)


if run:

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )


    results = []


    progress = st.progress(0)

    status = st.empty()


    # =====================================================
    # TRAIN MODELS
    # =====================================================

    for i, (name, classifier) in enumerate(
        models.items()
    ):

        status.write(
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
                scores[
                    "train_accuracy"
                ].mean(),

            "Validation Accuracy":
                scores[
                    "test_accuracy"
                ].mean(),

            "Train F1":
                scores[
                    "train_f1"
                ].mean(),

            "Validation F1":
                scores[
                    "test_f1"
                ].mean(),

            "Train ROC-AUC":
                scores[
                    "train_roc_auc"
                ].mean(),

            "Validation ROC-AUC":
                scores[
                    "test_roc_auc"
                ].mean()
        })


        progress.progress(
            int(
                ((i + 1) / len(models)) * 100
            )
        )


    status.success(
        "All models completed successfully."
    )


    results_df = pd.DataFrame(
        results
    )


    # =====================================================
    # RESULTS TABLE
    # =====================================================

    st.header("6. Results")


    display = results_df.copy()


    for column in [

        "Train Accuracy",
        "Validation Accuracy",
        "Train F1",
        "Validation F1",
        "Train ROC-AUC",
        "Validation ROC-AUC"

    ]:

        display[column] = (

            display[column] * 100

        ).round(2).astype(str) + "%"


    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # =====================================================
    # ACCURACY GRAPH
    # =====================================================

    st.header("7. Accuracy Comparison")


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


    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # F1 GRAPH
    # =====================================================

    st.header("8. F1 Score Comparison")


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


    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # ROC-AUC GRAPH
    # =====================================================

    st.header("9. ROC-AUC Comparison")


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


    st.pyplot(fig)

    plt.close(fig)


    # =====================================================
    # GENERALIZATION GAP
    # =====================================================

    st.header("10. Generalization Gap")


    gap = pd.DataFrame({

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


    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.header("11. Download Results")


    csv_data = results_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(

        "⬇️ Download Results CSV",

        data=csv_data,

        file_name="model_comparison_results.csv",

        mime="text/csv"
    )
