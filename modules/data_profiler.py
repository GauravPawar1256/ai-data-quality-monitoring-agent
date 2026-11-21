
import pandas as pd


# 1. Column-wise Data Profiling
def profile_dataset(df):

    profile = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().mean().values * 100
        ).round(2),
        "Unique Values": df.nunique().values
    })

    return profile


# 2. Statistical Summary
def get_statistical_summary(df):

    summary = df.describe(
        include="all"
    ).transpose()

    return summary


# 3. Dataset Information
def get_dataset_information(df):

    information = {
        "Total Rows": df.shape[0],
        "Total Columns": df.shape[1],
        "Total Missing Values": int(
            df.isnull().sum().sum()
        ),
        "Duplicate Rows": int(
            df.duplicated().sum()
        ),
        "Memory Usage (KB)": round(
            df.memory_usage(deep=True).sum() / 1024,
            2
        )
    }

    return information
