from utils.db import get_db_connection

def insert_employee(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO employees (
        first_name, last_name, age, sex, married, location, phone, email,
        education, social_links, about_self, experience, hobbies, username, password
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    values = tuple(data[k] for k in (
        'first_name', 'last_name', 'age', 'sex', 'married', 'location', 'phone',
        'email', 'education', 'social_links', 'about_self', 'experience',
        'hobbies', 'username', 'password'
    ))

    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def get_employees_by_query(query):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print("❌ SQL Execution Error:", e)
        return []
