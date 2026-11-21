
import streamlit as st
import pandas as pd


def show_history_dashboard(get_quality_history):

    st.header("📈 Historical Data Quality Monitoring")

    try:
        records = get_quality_history()

        if not records:
            st.info(
                "No historical records found. "
                "Run data quality checks to create history."
            )
            return

        # ==========================================
        # 1. CONVERT DATABASE RECORDS TO DATAFRAME
        # ==========================================

        columns = [
            "id",
            "dataset_name",
            "analysis_date",
            "total_rows",
            "total_columns",
            "overall_score",
            "completeness",
            "uniqueness",
            "validity",
            "consistency",
            "missing_values",
            "duplicate_rows"
        ]

        if isinstance(records[0], dict):
            history_df = pd.DataFrame(records)
        else:
            history_df = pd.DataFrame(
                records,
                columns=columns
            )

        # Convert date
        history_df["analysis_date"] = pd.to_datetime(
            history_df["analysis_date"],
            errors="coerce"
        )

        # Remove invalid dates
        history_df = history_df.dropna(
            subset=["analysis_date"]
        )

        if history_df.empty:
            st.warning("No valid historical dates found.")
            return

        # Convert scores
        numeric_columns = [
            "overall_score",
            "completeness",
            "uniqueness",
            "validity",
            "consistency"
        ]

        for column in numeric_columns:
            history_df[column] = pd.to_numeric(
                history_df[column],
                errors="coerce"
            )

        history_df = history_df.sort_values(
            "analysis_date"
        ).reset_index(drop=True)

        # ==========================================
        # 2. DASHBOARD METRICS
        # ==========================================

        total_analyses = len(history_df)

        average_score = history_df["overall_score"].mean()

        latest_score = history_df.iloc[-1]["overall_score"]

        total_datasets = history_df["dataset_name"].nunique()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Analyses", total_analyses)

        col2.metric(
            "Average Quality Score",
            f"{average_score:.2f}/100"
            if pd.notna(average_score) else "N/A"
        )

        col3.metric(
            "Latest Quality Score",
            f"{latest_score:.2f}/100"
            if pd.notna(latest_score) else "N/A"
        )

        col4.metric("Datasets Analyzed", total_datasets)

        st.divider()

        # ==========================================
        # 3. QUALITY SCORE TREND
        # ==========================================

        st.subheader("📊 Quality Score Trend")

        chart_df = history_df[
            ["analysis_date", "overall_score"]
        ].dropna().copy()

        if not chart_df.empty:
            chart_df = chart_df.set_index("analysis_date")

            st.line_chart(
                chart_df,
                y="overall_score",
                height=350
            )
        else:
            st.info("No valid quality scores available for the chart.")

        st.divider()

        # ==========================================
        # 4. QUALITY DIMENSION ANALYSIS
        # ==========================================

        st.subheader("📊 Latest Quality Dimensions")

        latest = history_df.iloc[-1]

        dimension_df = pd.DataFrame({
            "Dimension": [
                "Completeness",
                "Uniqueness",
                "Validity",
                "Consistency"
            ],
            "Score": [
                latest["completeness"],
                latest["uniqueness"],
                latest["validity"],
                latest["consistency"]
            ]
        })

        dimension_df = dimension_df.dropna(
            subset=["Score"]
        )

        if not dimension_df.empty:
            st.bar_chart(
                dimension_df.set_index("Dimension")
            )
        else:
            st.info("No quality dimension scores available.")

        st.divider()

        # ==========================================
        # 5. HISTORY TABLE
        # ==========================================

        st.subheader("📋 Analysis History")

        display_df = history_df.rename(columns={
            "id": "ID",
            "dataset_name": "Dataset Name",
            "analysis_date": "Analysis Date",
            "total_rows": "Total Rows",
            "total_columns": "Total Columns",
            "overall_score": "Overall Score",
            "completeness": "Completeness",
            "uniqueness": "Uniqueness",
            "validity": "Validity",
            "consistency": "Consistency",
            "missing_values": "Missing Values",
            "duplicate_rows": "Duplicate Rows"
        })

        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True
        )

        # ==========================================
        # 6. DOWNLOAD HISTORY
        # ==========================================

        csv_data = display_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download History as CSV",
            data=csv_data,
            file_name="data_quality_history.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(
            f"Historical dashboard error: {e}"
        )

        st.exception(e)
