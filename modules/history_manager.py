
from database.db_connection import get_db_connection


# ==========================================
# 1. SAVE QUALITY HISTORY
# ==========================================

def save_quality_history(
    dataset_name,
    total_rows,
    total_columns,
    score_results,
    missing_values,
    duplicate_rows
):

    connection = get_db_connection()

    try:

        query = """
        INSERT INTO quality_history (
            dataset_name,
            total_rows,
            total_columns,
            overall_score,
            completeness,
            uniqueness,
            validity,
            consistency,
            missing_values,
            duplicate_rows
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            dataset_name,
            total_rows,
            total_columns,
            score_results["Overall Score"],
            score_results["Completeness"],
            score_results["Uniqueness"],
            score_results["Validity"],
            score_results["Consistency"],
            missing_values,
            duplicate_rows
        )

        with connection.cursor() as cursor:
            cursor.execute(query, values)

        connection.commit()

        return True

    except Exception as e:
        connection.rollback()
        raise RuntimeError(f"History saving failed: {e}")

    finally:
        connection.close()


# ==========================================
# 2. GET QUALITY HISTORY
# ==========================================

def get_quality_history():

    connection = get_db_connection()

    try:

        query = """
        SELECT
            id,
            dataset_name,
            analysis_date,
            total_rows,
            total_columns,
            overall_score,
            completeness,
            uniqueness,
            validity,
            consistency,
            missing_values,
            duplicate_rows
        FROM quality_history
        ORDER BY analysis_date ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()

        return records

    except Exception as e:
        raise RuntimeError(
            f"Unable to retrieve history: {e}"
        )

    finally:
        connection.close()
