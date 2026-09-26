"""Live Gemini explanation helper for experiment results.

Uses Gemini's Interactions API. The generated explanation is stored in
Streamlit session state so a rerun does not erase it.
"""
import os
import time

import streamlit as st


# Use several currently supported stable Flash models. If one model is
# temporarily overloaded, the next model can handle the same explanation.
GEMINI_MODELS = (
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
)


def _get_api_key():
    """Read the Gemini key without crashing when Streamlit secrets are absent."""
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.environ.get("GEMINI_API_KEY", "")


def _is_transient_error(error):
    """Return True for errors where retrying or switching models can help."""
    message = str(error).lower()
    transient_markers = (
        "503",
        "service_unavailable",
        "service unavailable",
        "unavailable",
        "overloaded",
        "500",
        "internal server error",
        "429",
        "rate_limit_exceeded",
        "too_many_requests",
        "408",
        "deadline_exceeded",
        "timeout",
    )
    return any(marker in message for marker in transient_markers)


def _generate_with_fallback(client, prompt):
    """Generate an explanation, falling back when a model is temporarily busy."""
    failures = []

    for index, model_name in enumerate(GEMINI_MODELS):
        try:
            interaction = client.interactions.create(
                model=model_name,
                input=prompt,
            )
            explanation = getattr(interaction, "output_text", None)

            if explanation and explanation.strip():
                return explanation.strip(), model_name

            failures.append(f"{model_name}: empty response")
        except Exception as error:
            failures.append(f"{model_name}: {error}")

            # The Gemini SDK already retries transient failures internally.
            # A short pause here prevents an immediate burst when moving to
            # the next model.
            if _is_transient_error(error) and index < len(GEMINI_MODELS) - 1:
                time.sleep(1.5)
                continue

            # Authentication, permission, invalid-request, or other client
            # errors should be shown rather than hidden behind a model switch.
            if not _is_transient_error(error):
                raise

    raise RuntimeError("All Gemini models were temporarily unavailable. " + " | ".join(failures))


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

            with st.spinner("Generating AI explanation…"):
                client = genai.Client(api_key=api_key)
                explanation, model_used = _generate_with_fallback(client, prompt)

            st.session_state["live_experiment_explanation"] = explanation
            st.session_state["live_experiment_model"] = model_used

        except Exception as exc:
            message = str(exc).lower()

            if "quota_exceeded" in message or "daily quota" in message:
                st.error(
                    "Gemini daily quota has been exhausted. The app is configured "
                    "correctly, but a new Gemini request cannot be completed until "
                    "the quota resets."
                )
            elif _is_transient_error(exc):
                st.error(
                    "Gemini is temporarily overloaded. The app tried multiple "
                    "supported Flash models, but they were all unavailable. "
                    "Please try again in a few moments."
                )
            else:
                st.error(f"Could not generate the AI explanation: {exc}")

    explanation = st.session_state.get("live_experiment_explanation")
    model_used = st.session_state.get("live_experiment_model")

    if explanation:
        if model_used:
            st.caption(f"Generated with {model_used}.")
        st.markdown("### AI Explanation")
        st.markdown(explanation)
