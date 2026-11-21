import pymysql
from dotenv import load_dotenv
import os

load_dotenv()


def get_db_connection():

    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "ai_data_quality_db"),
            port=int(os.getenv("DB_PORT", 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )

        return connection

    except pymysql.MySQLError as e:
        raise RuntimeError(f"MySQL connection failed: {e}")