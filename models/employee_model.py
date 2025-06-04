from utils.db import get_connection

def insert_employee(personal, contact, education, experience, profile):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees (first_name, last_name, age, sex, married)
        VALUES (%s, %s, %s, %s, %s)
    """, personal)
    emp_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO employee_contact (employee_id, phone, email, location, social_links)
        VALUES (%s, %s, %s, %s, %s)
    """, (emp_id, *contact))

    cursor.execute("""
        INSERT INTO employee_education (employee_id, education)
        VALUES (%s, %s)
    """, (emp_id, education))

    cursor.execute("""
        INSERT INTO employee_experience (employee_id, experience)
        VALUES (%s, %s)
    """, (emp_id, experience))

    cursor.execute("""
        INSERT INTO employee_profile (employee_id, about_self, hobbies, username, password)
        VALUES (%s, %s, %s, %s, %s)
    """, (emp_id, *profile))

    conn.commit()
    cursor.close()
    conn.close()


def search_employees_by_sql(sql):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
