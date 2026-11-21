
import pandas as pd


# ==========================================
# LOAD CSV AND EXCEL DATASETS
# ==========================================

def load_dataset(uploaded_file):

    try:

        file_name = uploaded_file.name.lower()

        # Load CSV file
        if file_name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        # Load Excel file
        elif file_name.endswith((".xlsx", ".xls")):

            df = pd.read_excel(uploaded_file)

        else:

            raise ValueError(
                "Unsupported file format. Upload CSV or Excel."
            )

        # Check empty dataset
        if df.empty:

            raise ValueError(
                "The uploaded dataset is empty."
            )

        return df

    except Exception as e:

        raise ValueError(
            f"Dataset loading failed: {e}"
        )
