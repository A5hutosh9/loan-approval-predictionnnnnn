import os
import pandas as pd
import streamlit as st


REPOSITORY_DATASET = "loan_approval_dataset.csv"


def load_repository_dataset():
    """Load the project dataset stored in the GitHub repository."""

    if not os.path.exists(REPOSITORY_DATASET):
        return None

    try:
        df = pd.read_csv(REPOSITORY_DATASET)
        df.columns = df.columns.astype(str).str.strip()
        return df

    except Exception:
        return None


def show_dataset_expander(df, title="📁 Dataset"):
    """Show dataset information inside an expandable section."""

    if df is None:
        with st.expander(title):
            st.warning(
                "The repository dataset could not be loaded."
            )
        return

    with st.expander(title):

        st.subheader("Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True,
            height=450,
            hide_index=True
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        with col4:
            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        st.subheader("Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": [
                str(dtype)
                for dtype in df.dtypes
            ],
            "Missing Values": [
                int(df[column].isnull().sum())
                for column in df.columns
            ],
            "Unique Values": [
                int(df[column].nunique())
                for column in df.columns
            ]
        })

        st.dataframe(
            column_info,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Dataset",
            data=csv_data,
            file_name="loan_approval_dataset.csv",
            mime="text/csv"
        )


def normalize_binary_target(series):
    """
    Convert a binary target column to 0/1.

    Supports common labels such as:
    Approved / Rejected
    Yes / No
    True / False
    1 / 0
    """

    cleaned = series.astype(str).str.strip()

    # Numeric-like target
    numeric = pd.to_numeric(
        cleaned,
        errors="coerce"
    )

    if numeric.notna().all():

        unique_values = sorted(
            numeric.unique().tolist()
        )

        if len(unique_values) != 2:
            return None, None

        mapping = {
            unique_values[0]: 0,
            unique_values[1]: 1
        }

        return (
            numeric.map(mapping).astype(int),
            mapping
        )

    # Common text labels
    lower = cleaned.str.lower()

    positive_words = {
        "approved",
        "approve",
        "yes",
        "true",
        "accepted",
        "accept",
        "eligible",
        "1",
        "pass",
        "passed"
    }

    negative_words = {
        "rejected",
        "reject",
        "no",
        "false",
        "declined",
        "decline",
        "not eligible",
        "0",
        "fail",
        "failed"
    }

    unique_values = lower.unique().tolist()

    if len(unique_values) != 2:
        return None, None

    positive_found = [
        value
        for value in unique_values
        if value in positive_words
    ]

    negative_found = [
        value
        for value in unique_values
        if value in negative_words
    ]

    if len(positive_found) == 1 and len(negative_found) == 1:

        mapping = {
            negative_found[0]: 0,
            positive_found[0]: 1
        }

        y = lower.map(mapping).astype(int)

        return y, mapping

    # Generic binary text fallback
    unique_values = sorted(unique_values)

    mapping = {
        unique_values[0]: 0,
        unique_values[1]: 1
    }

    y = lower.map(mapping).astype(int)

    return y, mapping
