
import os
import pymysql
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# DATABASE SETTINGS
# ==========================================

def get_setting(key, default=None):
    """Read settings from Streamlit Cloud or local .env."""

    try:
        value = st.secrets.get(key)

        if value is not None:
            return value

    except Exception:
        pass

    return os.getenv(key, default)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    try:

        host = get_setting("DB_HOST")
        port = int(get_setting("DB_PORT", 4000))
        user = get_setting("DB_USER")
        password = get_setting("DB_PASSWORD")
        database = get_setting("DB_NAME")
        ca_path = get_setting("DB_SSL_CA")

        # Validate database settings
        required = {
            "DB_HOST": host,
            "DB_USER": user,
            "DB_PASSWORD": password,
            "DB_NAME": database
        }

        missing = [
            key for key, value in required.items()
            if not value
        ]

        if missing:
            raise ValueError(
                f"Missing database settings: {', '.join(missing)}"
            )

        # Validate SSL certificate
        if not ca_path:
            raise ValueError("DB_SSL_CA is missing.")

        ca_path = os.path.abspath(
            os.path.expanduser(str(ca_path))
        )

        if not os.path.isfile(ca_path):
            raise FileNotFoundError(
                f"SSL certificate not found: {ca_path}"
            )

        # Connect to database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl_ca=ca_path,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=15
        )

        return connection

    except Exception as e:
        raise RuntimeError(
            f"Database connection failed: {e}"
        ) from e
