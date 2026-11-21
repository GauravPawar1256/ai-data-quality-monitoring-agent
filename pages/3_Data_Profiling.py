
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Data Profiling")
st.caption("Explore missing values, numerical distributions and categorical data.")

st.divider()

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

st.subheader("Dataset Information")

col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Total Missing Values", int(df.isnull().sum().sum()))

st.divider()

tab1, tab2, tab3 = st.tabs([
    "Missing Values",
    "Numeric Analysis",
    "Categorical Analysis"
])

# 1. Missing Values
with tab1:
    st.subheader("Missing Values by Column")

    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0]

    if not missing_data.empty:
        st.bar_chart(missing_data)
        st.dataframe(
            missing_data.rename("Missing Count"),
            use_container_width=True
        )
    else:
        st.success("No missing values found!")

# 2. Numeric Analysis
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

            ax.set_title(f"Distribution of {selected_numeric}")
            ax.set_xlabel(selected_numeric)
            ax.set_ylabel("Frequency")

            st.pyplot(fig)
            plt.close(fig)

            st.subheader("Statistical Summary")
            st.write(df[selected_numeric].describe())
        else:
            st.info("No numeric values available.")
    else:
        st.info("No numeric columns available.")

# 3. Categorical Analysis
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
            st.subheader("Top 10 Most Frequent Values")

            st.bar_chart(category_counts)

            st.dataframe(
                category_counts.rename("Count"),
                use_container_width=True
            )
        else:
            st.info("No category values available.")
    else:
        st.info("No categorical columns available.")
