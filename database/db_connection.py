
import os
import pymysql
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_setting(key, default=None):
    """Read settings from Streamlit Cloud or local .env."""
    try:
        value = st.secrets.get(key)
        if value is not None:
            return value
    except Exception:
        pass

    return os.getenv(key, default)


def get_db_connection():
    try:
        connection = pymysql.connect(
            host=get_setting("DB_HOST"),
            port=int(get_setting("DB_PORT", 4000)),
            user=get_setting("DB_USER"),
            password=get_setting("DB_PASSWORD"),
            database=get_setting("DB_NAME"),
            ssl_ca=get_setting("DB_SSL_CA"),
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            cursorclass=pymysql.cursors.DictCursor
        )

        return connection

    except pymysql.MySQLError as e:
        raise RuntimeError(f"Database connection failed: {e}")
