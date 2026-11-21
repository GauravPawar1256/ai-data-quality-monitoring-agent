
from modules.history_manager import save_quality_history

sample_scores = {
    "Overall Score": 95.5,
    "Completeness": 98.0,
    "Uniqueness": 95.0,
    "Validity": 94.0,
    "Consistency": 96.0
}

try:
    result = save_quality_history(
        dataset_name="sample_students.csv",
        total_rows=100,
        total_columns=5,
        score_results=sample_scores,
        missing_values=2,
        duplicate_rows=1
    )

    if result:
        print("Quality history saved successfully!")

except Exception as e:
    print("Error:", e)
