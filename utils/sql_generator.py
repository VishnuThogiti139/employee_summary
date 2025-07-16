from utils.extract_schema import get_clean_schema_string
from config import API_KEYS
import openai
import google.generativeai as genai

def generate_sql_prompt(user_prompt):
    schema_text = get_clean_schema_string()  # Retrieve schema as string

    if not schema_text:
        return "Error: Schema is missing or invalid."

    # Generate prompt for the AI model
    return f"""
    You are a SQL assistant that can dynamically generate SQL queries.

    Here is the schema of the database:
    {schema_text}

    Based on the schema above, generate a SQL query that answers the 
    following user request:
    {user_prompt}

    Include necessary JOINs based on the relationships between 
    tables and return all relevant fields. 
    Only return the SQL query, no markdown, no explanations.
    """

def call_ai(model_name, prompt):
    try:
        if model_name.lower() == "gemini":
            genai.configure(api_key=API_KEYS["Gemini"])
            return genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt).text
        elif model_name.lower() == "openai":
            openai.api_key = API_KEYS["OpenAI"]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        
        return "[Unsupported model]"

    except Exception as e:
        return f"Error occurred with {model_name}: {str(e)}"

def clean_sql_query(sql_text: str) -> str:
    # """
    # Clean up the SQL query to remove 
    # unwanted characters or markdown.
    # """
    sql_text = sql_text.strip()
    sql_text = sql_text.replace("```sql", "").replace("```", "").strip()  # Remove any code block markers
    return sql_text
