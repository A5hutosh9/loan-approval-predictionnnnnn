"""Live Gemini explanation helper for experiment results.

Configure GEMINI_API_KEY in Streamlit secrets before calling this helper.
"""
import streamlit as st


def render_live_experiment_explanation(results_df, dataset_rows, dataset_columns, target_column):
    """Render a live Gemini explanation grounded in the current experiment metrics."""
    st.subheader("🤖 Live AI Results Explanation")
    st.caption("AI interpretation of the metrics from this run; not financial advice or an approval decision.")

    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.warning("Live AI is not configured. Add GEMINI_API_KEY under Streamlit App → Settings → Secrets to enable it.")
        return

    if not st.button("✨ Generate AI Explanation", key="generate_live_experiment_explanation"):
        st.info("Run the experiment, then select Generate AI Explanation to interpret its results.")
        return

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        metrics_csv = results_df.to_csv(index=False)
        prompt = f"""You are a careful machine-learning tutor. Explain the following experiment results in clear, concise language for a college project presentation.

Dataset dimensions: {dataset_rows} rows × {dataset_columns} columns
Target column: {target_column}
Model metrics (CSV):
{metrics_csv}

Discuss: (1) what the metrics mean, (2) training-validation gaps and possible overfitting, (3) ROC-AUC versus accuracy/F1, (4) what can and cannot be concluded from these results, and (5) limitations. Refer only to supplied values; do not invent causes or numbers. Do not rank models as universally best. State that results depend on this dataset and validation setup, and are not real-world lending guarantees."""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        explanation = getattr(response, "text", None)
        if explanation:
            st.markdown(explanation)
        else:
            st.error("Gemini returned an empty response. Try again.")
    except Exception as exc:
        st.error(f"Could not generate the AI explanation: {exc}")
