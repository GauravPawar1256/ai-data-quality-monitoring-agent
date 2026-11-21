
import numpy as np


def calculate_quality_score(df):

    total_rows = len(df)
    total_cells = df.shape[0] * df.shape[1]

    # 1. Completeness
    missing = int(df.isnull().sum().sum())

    completeness = (
        ((total_cells - missing) / total_cells) * 100
        if total_cells > 0 else 100
    )

    # 2. Uniqueness
    duplicates = int(df.duplicated().sum())

    uniqueness = (
        ((total_rows - duplicates) / total_rows) * 100
        if total_rows > 0 else 100
    )

    # 3. Validity (basic numeric outlier proxy)
    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    invalid_count = 0
    numeric_count = 0

    for column in numeric_columns:

        values = df[column].dropna()

        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        invalid_count += int(
            ((values < lower) | (values > upper)).sum()
        )

        numeric_count += len(values)

    validity = (
        ((numeric_count - invalid_count) / numeric_count) * 100
        if numeric_count > 0 else 100
    )

    # 4. Consistency
    inconsistent_count = 0
    total_categorical = 0

    for column in df.select_dtypes(include=["object"]).columns:

        values = df[column].dropna().astype(str)

        inconsistent_count += (
            values.nunique() -
            values.str.strip().str.lower().nunique()
        )

        total_categorical += values.nunique()

    consistency = (
        ((total_categorical - inconsistent_count)
         / total_categorical) * 100
        if total_categorical > 0 else 100
    )

    # 5. Accuracy proxy
    # Actual accuracy requires verified reference data.
    accuracy_proxy = 100

    # Weighted overall score
    overall_score = (
        completeness * 0.30 +
        uniqueness * 0.20 +
        validity * 0.20 +
        consistency * 0.15 +
        accuracy_proxy * 0.15
    )

    overall_score = round(overall_score, 2)

    return {
        "Overall Score": overall_score,
        "Completeness": round(completeness, 2),
        "Uniqueness": round(uniqueness, 2),
        "Validity": round(validity, 2),
        "Consistency": round(consistency, 2),
        "Accuracy Proxy": accuracy_proxy
    }
