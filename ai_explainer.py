"""Live Gemini explanation helper for experiment results.

Uses Gemini's Interactions API. The generated explanation is stored in
Streamlit session state so a rerun does not erase it.
"""
import os
import streamlit as st


MODEL_NAME = "gemini-3.6-flash"


def _get_api_key():
    """Read the Gemini key without crashing when Streamlit secrets are absent."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.environ.get("GEMINI_API_KEY", "")


def render_live_experiment_explanation(
    results_df, dataset_rows, dataset_columns, target_column
):
    """Render a live Gemini explanation of the current experiment."""
    st.subheader("🤖 Live AI Results Explanation")
    st.caption(
        "AI interpretation of this experiment's metrics; not a lending decision."
    )

    api_key = _get_api_key()
    if not api_key:
        st.warning(
            "Live AI is not configured. Add GEMINI_API_KEY under "
            "Streamlit App → Settings → Secrets."
        )
        return

    if st.button(
        "✨ Generate AI Explanation",
        key="generate_live_experiment_explanation",
        type="secondary",
        use_container_width=True,
    ):
        try:
            from google import genai

            metrics_csv = results_df.to_csv(index=False)
            prompt = f"""You are a careful machine-learning tutor. Explain the following experiment results in clear, concise language for a college project presentation.

Dataset dimensions: {dataset_rows} rows × {dataset_columns} columns
Target column: {target_column}

Model metrics (CSV):
{metrics_csv}

Discuss:
1. what the metrics mean;
2. training-validation gaps and possible overfitting;
3. ROC-AUC versus accuracy and F1;
4. what can and cannot be concluded from these results; and
5. limitations.

Use only the supplied values. Do not invent causes or numbers. Do not claim that
one model is universally best. State that the findings depend on this dataset
and validation setup and are not real-world lending guarantees."""

            with st.spinner("Generating AI explanation with Gemini 3.6 Flash…"):
                client = genai.Client(api_key=api_key)
                interaction = client.interactions.create(
                    model=MODEL_NAME,
                    input=prompt,
                )

            explanation = getattr(interaction, "output_text", None)

            if not explanation:
                raise RuntimeError(
                    "Gemini returned an empty response. Check the API key, SDK "
                    "version, and model availability."
                )

            st.session_state["live_experiment_explanation"] = explanation

        except Exception as exc:
            st.error(f"Could not generate the AI explanation: {exc}")

    explanation = st.session_state.get("live_experiment_explanation")
    if explanation:
        st.markdown("### AI Explanation")
        st.markdown(explanation)
