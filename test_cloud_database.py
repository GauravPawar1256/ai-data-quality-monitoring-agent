
from database.db_connection import get_db_connection

try:
    connection = get_db_connection()

    print("Cloud database connected successfully!")

    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS database_name")
        result = cursor.fetchone()
        print("Connected Database:", result["database_name"])

    connection.close()

except Exception as e:
    print("Connection error:", e)
