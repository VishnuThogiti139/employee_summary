from utils.db import get_connection

def get_db_schema():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                
                schema = []
                for table in tables:
                    columns = get_table_schema(cursor, table)
                    col_info = ", ".join(f"{col[0]} ({col[1]})" for col in columns)
                    schema.append(f"Table: {table}\nColumns: {col_info}")
                
                return schema
    except Exception as e:
        print(f"Error retrieving schema: {str(e)}")
        return []

def get_table_schema(cursor, table):
    cursor.execute(f"DESCRIBE {table}")
    return cursor.fetchall()

def get_clean_schema_string():
    schema_lines = get_db_schema()
    return "\n".join(schema_lines)
