from utils.ai_helper import call_gemini

def generate_sql_from_prompt(user_input):
    prompt = f"""
    You are an expert SQL generator. Given a natural language request by user, produce a MySQL SELECT query against the 'employees' table that best matches the request. 
    Only output the SQL query, no explanations.

    employee table has these columns : first_name, last_name, age, sex, married, location, phone, email,
        education, social_links, about_self, experience, hobbies, username, password

    Request: "{user_input}"
    """
    sql = call_gemini(prompt).strip("```")
    # ... validate and return

    sql = sql.strip('sql\n')
    print("🧠 Gemini raw output:", repr(sql))  # Use repr to see hidden chars

    # print("", repr(sql.strip('\n')))

    if ";" in sql:
        sql = sql.split(";")[0].strip() + ";"

    print("final sql query : " , repr(sql))

    if not sql.lower().startswith("select") or "employees" not in sql.lower():
        print("❌ Invalid SQL — using fallback.")
        return "SELECT * FROM employees;"

    return sql
