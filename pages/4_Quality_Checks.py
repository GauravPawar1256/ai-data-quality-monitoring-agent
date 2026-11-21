
import streamlit as st

from modules.quality_checks import run_quality_checks
from modules.history_manager import save_quality_history

st.title("🔍 Data Quality Checks")
st.caption("Detect missing values, duplicates, inconsistencies and numeric anomalies.")

st.divider()

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

if st.button("Run Data Quality Checks", type="primary", use_container_width=True):

    with st.spinner("Analyzing your dataset..."):

        try:
            results = run_quality_checks(df)

            st.session_state["quality_results"] = results

            # Clear old AI recommendations
            st.session_state.pop("ai_recommendations", None)

            # Save analysis history
            try:
                duplicate_count, _ = results["duplicates"]

                save_quality_history(
                    dataset_name=st.session_state.get(
                        "dataset_name", "Unknown Dataset"
                    ),
                    total_rows=df.shape[0],
                    total_columns=df.shape[1],
                    score_results=st.session_state["score_results"],
                    missing_values=int(df.isnull().sum().sum()),
                    duplicate_rows=int(duplicate_count)
                )

                st.success("Analysis history saved successfully!")

            except Exception as e:
                st.warning(f"History saving error: {e}")

        except Exception as e:
            st.error(f"Quality check error: {e}")


# Display saved results
if "quality_results" in st.session_state:

    results = st.session_state["quality_results"]

    st.success("Data quality analysis completed!")

    # 1. Missing Values
    st.subheader("1. Missing Value Detection")

    if results["missing"].empty:
        st.success("No missing values found.")
    else:
        st.dataframe(
            results["missing"],
            use_container_width=True
        )

    # 2. Duplicate Records
    st.subheader("2. Duplicate Record Detection")

    duplicate_count, duplicate_records = results["duplicates"]

    if duplicate_count > 0:
        st.warning(f"{duplicate_count} duplicate rows detected.")

        st.dataframe(
            duplicate_records,
            use_container_width=True
        )
    else:
        st.success("No duplicate records found.")

    # 3. Inconsistent Values
    st.subheader("3. Inconsistent Value Detection")

    if results["inconsistent"].empty:
        st.success("No possible inconsistencies found.")
    else:
        st.dataframe(
            results["inconsistent"],
            use_container_width=True
        )

    # 4. Numeric Anomalies
    st.subheader("4. Numeric Anomaly Detection")

    if results["anomalies"].empty:
        st.success("No potential outliers detected.")
    else:
        st.dataframe(
            results["anomalies"],
            use_container_width=True
        )

else:
    st.info("Click 'Run Data Quality Checks' to analyze your dataset.")
