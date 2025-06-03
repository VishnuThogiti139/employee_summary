import streamlit as st

DB_CONFIG = {
    "host": st.secrets["MYSQL_HOST"],
    "port": int(st.secrets["MYSQL_PORT"]),        # ✅ use correct key for port
    "user": st.secrets["MYSQL_USER"],
    "password": st.secrets["MYSQL_PASSWORD"],
    "database": st.secrets["MYSQL_DB"]
}

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
