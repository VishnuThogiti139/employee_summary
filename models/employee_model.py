from utils.db import get_connection
import mysql.connector
from config import DB_CONFIG

def insert_employee_dynamic(form_data):
    with get_connection() as conn:
        cursor = conn.cursor()

    # Step 1: Get all table columns
        table_map = {}
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = [col[0] for col in cursor.fetchall()]
            table_map[table] = columns

    # Step 2: Insert into `employees` first and get emp_id
        base_table = "employees"
        base_columns = [col for col in table_map[base_table] if col != "id"]
        base_values = [form_data.get(col) for col in base_columns]
        cursor.execute(
            f"INSERT INTO {base_table} ({', '.join(base_columns)}) VALUES ({', '.join(['%s'] * len(base_columns))})",
            base_values
        )
        emp_id = cursor.lastrowid

    # Step 3: Insert into all other tables using employee_id
        for table, columns in table_map.items():
            if table == base_table:
                continue
            cols_to_insert = [col for col in columns if col != "employee_id" and col in form_data]
            if not cols_to_insert:
                continue

            values = [form_data[col] for col in cols_to_insert]
            query = f"INSERT INTO {table} (employee_id, {', '.join(cols_to_insert)}) VALUES (%s, {', '.join(['%s'] * len(cols_to_insert))})"
            cursor.execute(query, [emp_id] + values)

        conn.commit()
        cursor.close()
        conn.close()



def search_employees_by_sql(sql_query):
    try:
        # Use context manager to manage the database connection
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:  # Use cursor inside the context manager
                cursor.execute(sql_query)  # Execute the provided SQL query
                results = cursor.fetchall()  # Fetch all matching rows
                return results  # Return the list of employee records
    except mysql.connector.Error as err:
        # Handle any database errors
        raise Exception(f"Error executing query: {err}")

def get_full_employee_profile(emp_id):
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                # Step 1: Find all tables that contain 'employee_id' column
                cursor.execute("""
                    SELECT TABLE_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE COLUMN_NAME = 'employee_id' AND TABLE_SCHEMA = DATABASE();
                """)
                tables = [row["TABLE_NAME"] for row in cursor.fetchall()]

                full_profile = {}

                # Step 2: Loop through each table and get data for that employee
                for table in tables:
                    try:
                        cursor.execute(f"SELECT * FROM {table} WHERE employee_id = %s", (emp_id,))
                        row = cursor.fetchone()
                        if row:
                            for key, value in row.items():
                                if key not in full_profile:  # Avoid overwriting
                                    full_profile[key] = value
                    except Exception as e:
                        print(f"Skipping table {table}: {e}")
                        
                return full_profile
    except Exception as e:
        raise Exception(f"Error retrieving full employee profile: {str(e)}")
