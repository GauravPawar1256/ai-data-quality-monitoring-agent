
import streamlit as st

from modules.ai_recommendations import generate_ai_recommendations

st.title("🤖 AI Data Quality Recommendations")

st.caption(
    "Get intelligent data quality insights powered by Google Gemini."
)

st.divider()

# Check whether a dataset is uploaded
if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

# Check whether quality checks are completed
if "quality_results" not in st.session_state:
    st.info("Please run Data Quality Checks first.")
    st.stop()

results = st.session_state["quality_results"]
score_results = st.session_state["score_results"]

st.subheader("📊 Analysis Summary")

col1, col2 = st.columns(2)

col1.metric(
    "Overall Quality Score",
    f'{score_results["Overall Score"]}/100'
)

col2.metric(
    "Dataset",
    st.session_state.get("dataset_name", "Unknown")
)

st.divider()

st.subheader("Generate AI Recommendations")

if st.button(
    "Generate AI Recommendations",
    type="primary",
    use_container_width=True
):

    try:
        with st.spinner(
            "Gemini is analyzing your data quality report..."
        ):

            ai_response = generate_ai_recommendations(
                results,
                score_results
            )

            st.session_state["ai_recommendations"] = ai_response

    except Exception as e:
        st.error(f"AI recommendation error: {e}")


# Display saved recommendations
if "ai_recommendations" in st.session_state:

    st.subheader("💡 AI Analysis Report")

    st.markdown(
        st.session_state["ai_recommendations"]
    )

else:
    st.info(
        "Click the button above to generate AI recommendations."
    )
