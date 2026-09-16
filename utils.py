import streamlit as st
import pandas as pd
import numpy as np


REPOSITORY_DATASET = "loan_approval_dataset.csv"


def load_repository_dataset():
    try:
        df = pd.read_csv(REPOSITORY_DATASET)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None


def show_dataset_expander(df, title="📁 Dataset"):
    if df is None:
        return

    with st.expander(title):
        st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
        st.dataframe(df, use_container_width=True)

        st.write("### Dataset Information")
        info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(info, use_container_width=True)


def normalize_binary_target(series):
    """
    Convert common binary target labels into 0 and 1.
    """

    # Numeric target
    if pd.api.types.is_numeric_dtype(series):
        unique = series.dropna().unique()

        if len(unique) != 2:
            raise ValueError("Target column must contain exactly 2 classes.")

        mapping = {
            unique[0]: 0,
            unique[1]: 1
        }

        return series.map(mapping), mapping

    # Text target
    values = series.astype(str).str.strip().str.lower()

    unique = values.dropna().unique()

    if len(unique) != 2:
        raise ValueError("Target column must contain exactly 2 classes.")

    positive_words = {
        "approved",
        "approve",
        "yes",
        "y",
        "true",
        "accepted",
        "accept",
        "1",
        "pass",
        "passed",
        "success",
        "successful"
    }

    negative_words = {
        "rejected",
        "reject",
        "no",
        "n",
        "false",
        "declined",
        "decline",
        "0",
        "fail",
        "failed"
    }

    mapping = {}

    for value in unique:
        if value in positive_words:
            mapping[value] = 1
        elif value in negative_words:
            mapping[value] = 0

    # If automatic mapping wasn't possible
    if len(mapping) != 2:
        mapping = {
            unique[0]: 0,
            unique[1]: 1
        }

    return values.map(mapping), mapping
