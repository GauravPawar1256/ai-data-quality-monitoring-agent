
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.data_loader import load_dataset
from modules.quality_checks import run_quality_checks
from modules.quality_score import calculate_quality_score
from modules.ai_recommendations import generate_ai_recommendations
from modules.history_manager import save_quality_history
from modules.history_dashboard import show_history_dashboard
from modules.history_manager import get_quality_history



# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Data Quality Monitoring Agent",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CUSTOM PROFESSIONAL FRONTEND DESIGN
# ==========================================


st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #EEF2FF 0%, #F0FDFA 50%, #FFF7ED 100%);
    color: #1E293B;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Headings */
h1 {
    color: #4338CA !important;
    font-weight: 850 !important;
}

h2 {
    color: #6D28D9 !important;
    font-weight: 750 !important;
}

h3 {
    color: #0F766E !important;
    font-weight: 700 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #E0E7FF);
    border: 1px solid #C7D2FE;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(79, 70, 229, 0.12);
}

[data-testid="stMetric"]:nth-child(2) {
    background: linear-gradient(135deg, #FFFFFF, #CCFBF1);
}

[data-testid="stMetricValue"] {
    color: #4F46E5;
    font-weight: 850;
}

[data-testid="stMetricLabel"] {
    color: #334155;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #7C3AED, #2563EB, #0891B2);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #5B21B6, #1D4ED8, #0E7490);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(79, 70, 229, 0.25);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #FFFFFF, #F3E8FF);
    border: 2px dashed #A78BFA;
    border-radius: 16px;
    padding: 18px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #C7D2FE;
    border-radius: 14px;
    overflow: hidden;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #475569;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    color: #7C3AED !important;
    border-bottom-color: #7C3AED !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #312E81, #5B21B6, #0F766E);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Alerts and progress */
[data-testid="stAlert"] {
    border-radius: 12px;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #7C3AED, #06B6D4);
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(90deg, #059669, #0D9488);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

/* Dividers */
hr {
    border-color: #C4B5FD;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. APPLICATION HEADER
# ==========================================

# st.title("🛡️ Data Quality Monitor")


st.markdown("""
<div style="
    background: linear-gradient(#EEF2FF, #A78BFA);
    padding: 28px;
    border-radius: 20px;
    margin: 25px;
    text-align:center;
    box-shadow: 0 8px 24px rgba(0, 7, 22, 20);
">
    <h1 style="color:white !important; margin:auto;">
        🛡️ AI Data Quality Monitor
    </h1>
    <p style="color:#E0F2FE; text-align:center; font-size:17px; 
    margin:10px 0 0 0;">
        Intelligent Data Validation | AI Recommendations |
        Quality Analytics | Historical Monitoring
    </p>
</div>
""", unsafe_allow_html=True)



st.divider()


# ==========================================
# 3. DATASET UPLOAD
# ==========================================

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel dataset",
    type=["csv", "xlsx", "xls"]
)


if uploaded_file is not None:

    try:

        # ==========================================
        # 4. LOAD DATASET
        # ==========================================

        df = load_dataset(uploaded_file)

        dataset_key = (
            f"{uploaded_file.name}:{uploaded_file.size}"
        )

        # Reset old results for a new dataset
        if st.session_state.get("dataset_key") != dataset_key:

            st.session_state["dataset_key"] = dataset_key

            st.session_state.pop(
                "quality_results", None
            )

            st.session_state.pop(
                "ai_recommendations", None
            )

        st.success("Dataset uploaded successfully!")

        # ==========================================
        # 5. DATASET PREVIEW
        # ==========================================

        st.subheader("📁 Dataset Preview")

        st.dataframe(
            df.head(10),
            width="stretch"
        )

        # ==========================================
        # 6. DATASET OVERVIEW
        # ==========================================

        st.subheader("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Rows", df.shape[0])

        col2.metric("Total Columns", df.shape[1])

        col3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

        col4.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )

        st.divider()

        # ==========================================
        # 7. DATA QUALITY SCORE
        # ==========================================

        st.subheader("🎯 Data Quality Score")

        score_results = calculate_quality_score(df)

        score = score_results["Overall Score"]

        col1, col2 = st.columns([1, 2])

        with col1:

            st.metric(
                "Overall Quality Score",
                f"{score}/100"
            )

            st.progress(score / 100)

            if score >= 90:
                st.success("Excellent Data Quality")

            elif score >= 75:
                st.info("Good Data Quality")

            elif score >= 50:
                st.warning("Moderate Data Quality")

            else:
                st.error("Poor Data Quality")

        with col2:

            st.write("Quality Dimension Analysis")

            score_df = pd.DataFrame({
                "Dimension": [
                    "Completeness",
                    "Uniqueness",
                    "Validity",
                    "Consistency",
                    "Accuracy Proxy"
                ],

                "Score": [
                    score_results["Completeness"],
                    score_results["Uniqueness"],
                    score_results["Validity"],
                    score_results["Consistency"],
                    score_results["Accuracy Proxy"]
                ]
            })

            st.bar_chart(
                score_df.set_index("Dimension")
            )

        st.divider()

        # ==========================================
        # 8. INTERACTIVE DATA PROFILING
        # ==========================================

        st.header("📊 Interactive Data Profiling")

        tab1, tab2, tab3 = st.tabs([
            "Missing Values",
            "Numeric Analysis",
            "Categorical Analysis"
        ])

        # TAB 1: MISSING VALUES

        with tab1:

            st.subheader("Missing Values by Column")

            missing_data = df.isnull().sum()

            missing_data = missing_data[
                missing_data > 0
            ]

            if not missing_data.empty:

                st.bar_chart(missing_data)

                st.dataframe(
                    missing_data.rename("Missing Count"),
                    width="stretch"
                )

            else:

                st.success("No missing values found!")

        # TAB 2: NUMERIC ANALYSIS

        with tab2:

            st.subheader("Numeric Column Distribution")

            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_columns:

                selected_numeric = st.selectbox(
                    "Select a numeric column",
                    numeric_columns
                )

                values = df[selected_numeric].dropna()

                if not values.empty:

                    fig, ax = plt.subplots(figsize=(9, 4))

                    ax.hist(
                        values,
                        bins=20,
                        edgecolor="black"
                    )

                    ax.set_title(
                        f"Distribution of {selected_numeric}"
                    )

                    ax.set_xlabel(selected_numeric)
                    ax.set_ylabel("Frequency")

                    st.pyplot(fig)

                    plt.close(fig)

                    st.subheader("Statistical Summary")

                    st.write(
                        df[selected_numeric].describe()
                    )

                else:

                    st.info("No numeric values available.")

            else:

                st.info("No numeric columns available.")

        # TAB 3: CATEGORICAL ANALYSIS

        with tab3:

            st.subheader("Categorical Column Analysis")

            categorical_columns = df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns.tolist()

            if categorical_columns:

                selected_category = st.selectbox(
                    "Select a categorical column",
                    categorical_columns
                )

                category_counts = (
                    df[selected_category]
                    .value_counts()
                    .head(10)
                )

                if not category_counts.empty:

                    st.subheader(
                        "Top 10 Most Frequent Values"
                    )

                    st.bar_chart(category_counts)

                    st.dataframe(
                        category_counts.rename("Count"),
                        width="stretch"
                    )

                else:

                    st.info("No category values available.")

            else:

                st.info("No categorical columns available.")

        st.divider()

        # ==========================================
        # 9. DATA QUALITY CHECKS
        # ==========================================

        st.header("🔍 Data Quality Analysis")

        if st.button(
            "Run Data Quality Checks",
            type="primary",
            width="stretch"
        ):

            with st.spinner("Analyzing your dataset..."):

                # Run quality checks
                results = run_quality_checks(df)

                # Save results in Streamlit session
                st.session_state["quality_results"] = results

                # Clear previous AI recommendations
                st.session_state.pop(
                    "ai_recommendations", None
                )

                # ==========================================
                # 10. SAVE HISTORY IN MYSQL
                # ==========================================

                try:

                    duplicate_count, _ = results["duplicates"]

                    save_quality_history(
                        dataset_name=uploaded_file.name,
                        total_rows=df.shape[0],
                        total_columns=df.shape[1],
                        score_results=score_results,
                        missing_values=int(
                            df.isnull().sum().sum()
                        ),
                        duplicate_rows=int(duplicate_count)
                    )

                    st.success(
                        "Analysis history saved successfully in MySQL!"
                    )

                except Exception as e:

                    st.error(
                        f"History saving error: {e}"
                    )

        # ==========================================
        # 11. DISPLAY QUALITY RESULTS
        # ==========================================

        if "quality_results" in st.session_state:

            results = st.session_state["quality_results"]

            st.success("Data quality analysis completed!")

            # MISSING VALUES

            st.subheader("1. Missing Value Detection")

            if results["missing"].empty:

                st.success("No missing values found.")

            else:

                st.dataframe(
                    results["missing"],
                    width="stretch"
                )

            # DUPLICATES

            st.subheader("2. Duplicate Record Detection")

            duplicate_count, duplicate_records = (
                results["duplicates"]
            )

            if duplicate_count > 0:

                st.warning(
                    f"{duplicate_count} duplicate rows detected."
                )

                st.dataframe(
                    duplicate_records,
                    width="stretch"
                )

            else:

                st.success("No duplicate records found.")

            # INCONSISTENCIES

            st.subheader("3. Inconsistent Value Detection")

            if results["inconsistent"].empty:

                st.success(
                    "No possible inconsistencies found."
                )

            else:

                st.dataframe(
                    results["inconsistent"],
                    width="stretch"
                )

            # NUMERIC ANOMALIES

            st.subheader("4. Numeric Anomaly Detection")

            if results["anomalies"].empty:

                st.success(
                    "No potential outliers detected."
                )

            else:

                st.dataframe(
                    results["anomalies"],
                    width="stretch"
                )

            # ==========================================
            # 12. AI DATA QUALITY RECOMMENDATIONS
            # ==========================================

            st.divider()

            st.header("🤖 AI Data Quality Recommendations")

            st.write(
                "Get intelligent recommendations "
                "powered by Google Gemini."
            )

            if st.button(
                "Generate AI Recommendations",
                type="primary",
                width="stretch"
            ):

                try:

                    with st.spinner(
                        "Gemini is analyzing your data quality report..."
                    ):

                        ai_response = generate_ai_recommendations(
                            results,
                            score_results
                        )

                    st.session_state["ai_recommendations"] = (
                        ai_response
                    )

                except Exception as e:

                    st.error(
                        f"AI recommendation error: {e}"
                    )

            # DISPLAY AI RESPONSE

            if "ai_recommendations" in st.session_state:

                st.subheader("💡 AI Analysis Report")

                st.markdown(
                    st.session_state["ai_recommendations"]
                )

    except Exception as e:

        st.error(f"Error: {e}")

else:
    st.info("Please upload a dataset to start monitoring.")

# ==========================================
# HISTORICAL MONITORING DASHBOARD
# ==========================================

st.divider()

show_history_dashboard(get_quality_history)
