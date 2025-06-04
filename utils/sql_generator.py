def generate_sql_prompt(user_prompt):
    return f"""
You are an expert MySQL assistant. Write a SQL SELECT query based on this natural language request:
\"\"\"{user_prompt}\"\"\"

Always include these fields in the SELECT clause:
- e.id
- e.first_name
- e.last_name
- ec.phone
- ec.email
- ec.location
- ec.social_links
- ee.education
- ep.about_self
- ep.hobbies
- ep.username
- ep.password
- ex.experience
- e.age
- e.sex
- e.married

Use appropriate JOINs between:
- employees (alias: e)
- employee_contact (alias: ec)
- employee_education (alias: ee)
- employee_experience (alias: ex)
- employee_profile (alias: ep)
"""
def clean_sql_query(sql_text: str) -> str:
    sql_text = sql_text.strip()
    if sql_text.startswith("```sql"):
        sql_text = sql_text.replace("```sql", "").strip()
    sql_text = sql_text.replace("```", "").strip()
    return sql_text
