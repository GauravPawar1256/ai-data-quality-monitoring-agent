
import pandas as pd
import numpy as np


def check_missing_values(df):

    results = []

    for column in df.columns:

        missing_count = int(df[column].isnull().sum())

        if df[column].dtype == "object":
            empty_count = int(
                df[column].astype("string").str.strip().eq("").sum()
            )
        else:
            empty_count = 0

        total_missing = missing_count + empty_count

        if total_missing > 0:

            results.append({
                "Column": column,
                "Missing Values": total_missing,
                "Missing Percentage": round(
                    total_missing / len(df) * 100, 2
                ) if len(df) else 0,
                "Issue": "Missing or empty values"
            })

    return pd.DataFrame(results)


def check_duplicates(df):

    duplicate_count = int(df.duplicated().sum())

    duplicate_records = df[df.duplicated(keep=False)]

    return duplicate_count, duplicate_records


def check_inconsistent_values(df):

    results = []

    for column in df.select_dtypes(include=["object"]).columns:

        values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        normalized = values.str.lower()

        if normalized.nunique() < values.nunique():

            results.append({
                "Column": column,
                "Original Unique Values": values.nunique(),
                "Normalized Unique Values": normalized.nunique(),
                "Issue": "Possible case or whitespace inconsistency"
            })

    return pd.DataFrame(results)


def check_numeric_anomalies(df):

    results = []

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        unusual = series[
            (series < lower_limit) |
            (series > upper_limit)
        ]

        if not unusual.empty:

            results.append({
                "Column": column,
                "Unusual Values": len(unusual),
                "Lower Limit": round(float(lower_limit), 2),
                "Upper Limit": round(float(upper_limit), 2),
                "Issue": "Potential numeric outliers"
            })

    return pd.DataFrame(results)


def run_quality_checks(df):

    return {
        "missing": check_missing_values(df),
        "duplicates": check_duplicates(df),
        "inconsistent": check_inconsistent_values(df),
        "anomalies": check_numeric_anomalies(df)
    }
