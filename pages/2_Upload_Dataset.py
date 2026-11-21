
import streamlit as st

from modules.data_loader import load_dataset
from modules.quality_score import calculate_quality_score

st.title("📁 Upload Dataset")
st.caption("Upload your CSV or Excel file for quality monitoring.")

st.divider()

uploaded_file = st.file_uploader(
    "Choose your dataset",
    type=["csv", "xlsx", "xls"],
    key="dataset_uploader"
)

if uploaded_file is not None:

    try:
        dataset_key = f"{uploaded_file.name}:{uploaded_file.size}"

        # Load only when a new file is uploaded
        if st.session_state.get("dataset_key") != dataset_key:

            df = load_dataset(uploaded_file)

            st.session_state["dataset_key"] = dataset_key
            st.session_state["df"] = df
            st.session_state["dataset_name"] = uploaded_file.name
            st.session_state["score_results"] = calculate_quality_score(df)

            # Clear results belonging to the previous dataset
            st.session_state.pop("quality_results", None)
            st.session_state.pop("ai_recommendations", None)

        st.success("Dataset uploaded successfully!")

    except Exception as e:
        st.error(f"Error loading dataset: {e}")


# Display saved dataset
if "df" in st.session_state:

    df = st.session_state["df"]

    st.subheader("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.subheader("Dataset Preview")

    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("🎯 Data Quality Score")

    score_results = st.session_state["score_results"]
    score = score_results["Overall Score"]

    st.metric("Overall Quality Score", f"{score}/100")
    st.progress(score / 100)

else:
    st.info("Please upload a CSV or Excel dataset.")
