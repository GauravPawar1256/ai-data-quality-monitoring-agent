
from database.db_connection import get_db_connection

try:
    connection = get_db_connection()

    print("MySQL connected successfully!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS db_name")
        result = cursor.fetchone()

        print("Connected Database:", result["db_name"])

    connection.close()

except Exception as e:
    print("Database Error:", e)
