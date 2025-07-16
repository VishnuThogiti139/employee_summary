import mysql.connector
from config import DB_CONFIG
from contextlib import contextmanager

@contextmanager
def get_connection():
    # """
    # A context manager for handling MySQL database connections.
    # """
    conn = None
    try:
        # Establishing the connection
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn  # Yield the connection to the calling code
    except mysql.connector.Error as err:
        # Handling any database connection errors
        raise Exception(f"Error connecting to the database: {err}")
    finally:
        # Close the connection when the block is exited, if it's valid
        if conn and conn.is_connected():
            conn.close()
