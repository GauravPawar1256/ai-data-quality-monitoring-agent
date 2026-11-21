
from modules.history_manager import get_quality_history

try:

    records = get_quality_history()

    if records:

        print("Quality History Retrieved Successfully!")

        for record in records:
            print(record)

    else:

        print("No history records found.")

except Exception as e:

    print("Error:", e)
