from flask import Blueprint, request, jsonify
import google.generativeai as genai
from utils.sql_generator import generate_sql_from_prompt
from models.employee_model import get_employees_by_query

ai_summary_bp = Blueprint('ai_summary', __name__)

@ai_summary_bp.route('/ai-summary', methods=['POST'])
def ai_summary():
    data = request.get_json()
    user_input = data.get('query')
    include_contact = data.get('include_contact', False)

    if not user_input:
        return jsonify({"error": "Query is required"}), 400

    # Step 1: Generate SQL query from user prompt
    sql_query = generate_sql_from_prompt(user_input)

    # Step 2: Execute the SQL query to get employee data
    employees = get_employees_by_query(sql_query)

    # Step 3: Generate summary excluding sensitive info
    summary_lines = []
    contact_info = []

    for emp in employees:
        # Collect contact info only if requested
        if include_contact:
            contact_info.append({
                "name": f"{emp.get('first_name')} {emp.get('last_name')}",
                "email": emp.get('email'),
                "phone": emp.get('phone')
            })

        # Summarize non-sensitive data
        summary_lines.append(
            f"{emp.get('first_name')} {emp.get('last_name')} is a {emp.get('age', 'N/A')} year old "
            f"{emp.get('sex', 'N/A')} located in {emp.get('location', 'N/A')} with {emp.get('experience', 'N/A')} "
            f"experience and hobbies including {emp.get('hobbies', 'N/A')}."
        )

    summary = "\n".join(summary_lines) if summary_lines else "No employee data found."
    prompt = f"""
                You are an intelligent assistant. 
                Generate a 4 paragraph summary describing the following person based on the following details:
                {summary}
                Ensure the summary sounds natural, 
                professional, and privacy-conscious. Exclude any contact info and 
                sensitive data like marital_status, birthdates.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        try:
            response = model.generate_content(prompt)
            summary = response.text.strip()
        except Exception as e:
            summary = f"Error generating summary: {str(e)}"
    except Exception as e:
        summary = f"Error generating summary: {str(e)}"

    return jsonify({
        "sql_query": sql_query,
        "summary": summary,
        "contact_info": contact_info if include_contact else []
    })
