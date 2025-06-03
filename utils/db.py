from config import DB_CONFIG
import mysql.connector

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        import streamlit as st
        st.error(f"MySQL connection failed: {err}")
        raise
