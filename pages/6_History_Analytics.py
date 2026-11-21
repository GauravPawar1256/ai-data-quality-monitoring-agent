
import streamlit as st

from modules.history_manager import get_quality_history
from modules.history_dashboard import show_history_dashboard

st.title("📚 History Analytics")

st.caption(
    "Monitor previous data quality analyses stored in your database."
)

st.divider()

try:
    show_history_dashboard(get_quality_history)

except Exception as e:
    st.error(f"Unable to load history analytics: {e}")
