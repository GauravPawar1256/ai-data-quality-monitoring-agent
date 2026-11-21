
import streamlit as st

st.title("🛡️ AI Data Quality Monitoring Agent")

st.caption(
    "Intelligent dataset validation and monitoring"
)

st.divider()

st.header("📊 Dashboard")

st.info(
    "Welcome! Upload a dataset to begin monitoring its quality."
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Datasets", "0")
col2.metric("Analyses Completed", "0")
col3.metric("Average Quality Score", "0%")

st.divider()

st.subheader("Getting Started")

st.write("""
1. Upload your CSV or Excel dataset.
2. Explore data profiling and statistics.
3. Run data quality checks.
4. Generate AI recommendations.
5. Review historical analytics.
""")
