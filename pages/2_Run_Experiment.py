import hashlib
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_curve
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

from ai_explainer import render_live_experiment_explanation
from utils import normalize_binary_target


st.set_page_config(page_title="Run Experiment", page_icon="🧪", layout="wide")
st.title("🧪 Run Experiment")
st.caption(
    "Upload a binary-classification CSV, run the models once, and then generate "
    "an AI explanation without rerunning the experiment."
)

uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"],
    key="experiment_csv",
)

# Keep a copy of the upload in session state. This makes the experiment independent
# of the file-uploader widget during later Streamlit reruns (for example, when the
# AI button is clicked).
if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    st.session_state["experiment_file_bytes"] = file_bytes
    st.session_state["experiment_file_name"] = file_name
    st.session_state["experiment_file_hash"] = file_hash
else:
    file_bytes = st.session_state.get("experiment_file_bytes")
    file_name = st.session_state.get("experiment_file_name")
    file_hash = st.session_state.get("experiment_file_hash")

if not file_bytes:
    st.info("Upload a CSV file to start a new experiment.")
    st.markdown(
        "**Supported targets:** Approved/Rejected, Yes/No, 1/0, or True/False. "
        "Choose a binary target column after uploading."
    )
    st.stop()

try:
    df = pd.read_csv(io.BytesIO(file_bytes))
    df.columns = df.columns.astype(str).str.strip()
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

with st.expander("📁 Uploaded Dataset", expanded=False):
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
    st.dataframe(df, use_container_width=True)

target_column = st.selectbox("Choose the target column:", df.columns)

signature = (file_hash, target_column)
if st.session_state.get("experiment_signature") != signature:
    st.session_state["experiment_signature"] = signature
    st.session_state.pop("experiment_results", None)
    st.session_state.pop("experiment_roc", None)
    st.session_state.pop("experiment_dataset_info", None)
    st.session_state.pop("live_experiment_explanation", None)

try:
    y_raw, target_mapping = normalize_binary_target(df[target_column])
except Exception as exc:
    st.error(str(exc))
    st.stop()

valid = y_raw.notna()
df = df.loc[valid].copy()
y = y_raw.loc[valid].astype(int)
X = df.drop(columns=[target_column])

id_columns = [
    c
    for c in X.columns
    if c.lower().replace("_", "").replace(" ", "")
    in {"id", "loanid", "applicationid", "customerid", "applicantid"}
]
if id_columns:
    X = X.drop(columns=id_columns)
    st.info(f"Automatically removed ID column(s): {', '.join(id_columns)}")

empty_columns = [c for c in X.columns if X[c].isna().all()]
if empty_columns:
    X = X.drop(columns=empty_columns)
    st.warning(f"Removed completely empty columns: {', '.join(empty_columns)}")

numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
categorical_features = X.select_dtypes(exclude=["number"]).columns.tolist()

st.header("🔍 Detected Features")
left, right = st.columns(2)
left.write("**Numerical**")
left.write(numeric_features or "None")
right.write("**Categorical**")
right.write(categorical_features or "None")

counts = y.value_counts().sort_index()
st.header("📊 Target Distribution")
a, b = st.columns(2)
a.metric("Class 0", int(counts.get(0, 0)))
b.metric("Class 1", int(counts.get(1, 0)))

if not numeric_features and not categorical_features:
    st.error("No usable feature columns remain after removing the target and ID/empty columns.")
    st.stop()

transformers = []
if numeric_features:
    transformers.append(
        (
            "numeric",
            Pipeline([("imputer", SimpleImputer(strategy="median"))]),
            numeric_features,
        )
    )

if categorical_features:
    transformers.append(
        (
            "categorical",
            Pipeline(
                [
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            categorical_features,
        )
    )

preprocessor = ColumnTransformer(transformers=transformers)

models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Bagging": BaggingClassifier(
        estimator=DecisionTreeClassifier(random_state=42),
        n_estimators=100,
        bootstrap=True,
        random_state=42,
        n_jobs=1,
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_features="sqrt",
        random_state=42,
        n_jobs=1,
    ),
    "AdaBoost": AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1, random_state=42),
        n_estimators=100,
        learning_rate=0.5,
        random_state=42,
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42,
    ),
}

results_df = st.session_state.get("experiment_results")

# Do not expose a second run button once a completed result exists. This makes the
# post-run state unambiguous: the page can rerun for AI generation without starting
# another experiment.
if results_df is None:
    if st.button("🚀 Run Experiment", type="primary", use_container_width=True):
        if len(X) < 20:
            st.error("Dataset is too small for a meaningful experiment (minimum 20 rows).")
            st.stop()

        class_counts = y.value_counts()
        if len(class_counts) != 2 or int(class_counts.min()) < 2:
            st.error(
                "The target must contain exactly two classes, with at least two samples in each class."
            )
            st.stop()

        cv = StratifiedKFold(
            n_splits=min(5, int(class_counts.min())),
            shuffle=True,
            random_state=42,
        )

        results = []
        roc_data = {}
        progress = st.progress(0)

        for idx, (name, model) in enumerate(models.items()):
            pipe = Pipeline(
                [
                    ("preprocessor", preprocessor),
                    ("model", model),
                ]
            )

            scores = cross_validate(
                pipe,
                X,
                y,
                cv=cv,
                scoring=["accuracy", "f1", "roc_auc"],
                return_train_score=True,
                n_jobs=1,
            )

            train_acc = scores["train_accuracy"].mean()
            val_acc = scores["test_accuracy"].mean()
            train_f1 = scores["train_f1"].mean()
            val_f1 = scores["test_f1"].mean()
            train_auc = scores["train_roc_auc"].mean()
            val_auc = scores["test_roc_auc"].mean()

            results.append(
                {
                    "Model": name,
                    "Train Accuracy": train_acc,
                    "Validation Accuracy": val_acc,
                    "Train F1": train_f1,
                    "Validation F1": val_f1,
                    "Train ROC-AUC": train_auc,
                    "Validation ROC-AUC": val_auc,
                    "Accuracy Gap": train_acc - val_acc,
                    "F1 Gap": train_f1 - val_f1,
                    "ROC-AUC Gap": train_auc - val_auc,
                }
            )

            probabilities = cross_val_predict(
                pipe,
                X,
                y,
                cv=cv,
                method="predict_proba",
                n_jobs=1,
            )[:, 1]

            fpr, tpr, _ = roc_curve(y, probabilities)
            roc_data[name] = (fpr, tpr, val_auc)
            progress.progress((idx + 1) / len(models))

        st.session_state["experiment_results"] = pd.DataFrame(results)
        st.session_state["experiment_roc"] = roc_data
        st.session_state["experiment_dataset_info"] = (
            len(df),
            df.shape[1],
            target_column,
        )
        st.session_state.pop("live_experiment_explanation", None)
        st.rerun()

    st.info("Select **Run Experiment** to calculate model results.")
    st.stop()

# Everything below this line is rendered from session state. A click on the AI
# button causes only a normal Streamlit rerun and does not execute the model loop.
rows, columns, target_name = st.session_state["experiment_dataset_info"]

st.success(
    "Experiment completed. Results are saved for this session; generating the AI "
    "explanation will not rerun the models."
)

render_live_experiment_explanation(
    results_df,
    rows,
    columns,
    target_name,
)

st.header("📋 Model Results")
st.dataframe(
    results_df.style.format(
        {
            c: "{:.4f}"
            for c in results_df.columns
            if c != "Model"
        }
    ),
    use_container_width=True,
)

x = np.arange(len(results_df))
width = 0.35

for metric, heading in [
    ("Accuracy", "📊 Accuracy Comparison"),
    ("F1", "📊 F1-Score Comparison"),
    ("ROC-AUC", "📊 ROC-AUC Comparison"),
]:
    st.header(heading)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(
        x - width / 2,
        results_df[f"Train {metric}"],
        width,
        label="Training",
    )
    ax.bar(
        x + width / 2,
        results_df[f"Validation {metric}"],
        width,
        label="Validation",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(results_df["Model"], rotation=20)
    ax.set_ylabel(metric)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.header("🔎 Generalization Gap")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(results_df["Model"], results_df["Accuracy Gap"])
ax.set_ylabel("Training − Validation Accuracy")
ax.set_title("Accuracy Generalization Gap")
plt.xticks(rotation=20)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.header("📈 ROC Curves")
fig, ax = plt.subplots(figsize=(9, 7))
for name, (fpr, tpr, auc_value) in st.session_state["experiment_roc"].items():
    ax.plot(fpr, tpr, label=f"{name} (AUC={auc_value:.3f})")

ax.plot([0, 1], [0, 1], linestyle="--")
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("Cross-Validated ROC Curves")
ax.legend()
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.header("⬇️ Download Results")
st.download_button(
    "Download Experiment Results",
    data=results_df.to_csv(index=False).encode("utf-8"),
    file_name="loan_experiment_results.csv",
    mime="text/csv",
)
