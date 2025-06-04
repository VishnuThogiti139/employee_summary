import streamlit as st
from models.employee_model import insert_employee, search_employees_by_sql
from utils.ai_helper import call_ai
from utils.sql_generator import generate_sql_prompt, clean_sql_query

# --- Session state initialization ---
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""
if "view_contact" not in st.session_state:
    st.session_state.view_contact = False
if "last_employee" not in st.session_state:
    st.session_state.last_employee = None
if "employee_options" not in st.session_state:
    st.session_state.employee_options = []
if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False

st.set_page_config("Employee AI Summary Generator", layout="centered")
st.title("🧠 Employee AI Summary App")

# --- Sidebar: Add Employee ---
st.sidebar.header("➕ Add New Employee")
with st.sidebar.form("add_form"):
    first, last = st.text_input("First Name"), st.text_input("Last Name")
    age = st.number_input("Age", min_value=0)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    married = st.checkbox("Married")
    phone, email = st.text_input("Phone"), st.text_input("Email")
    location = st.text_input("Location")
    social_links = st.text_area("Social Media Links")
    education = st.text_area("Education")
    experience = st.text_area("Experience")
    about = st.text_area("About Self")
    hobbies = st.text_area("Hobbies")
    username, password = st.text_input("Username"), st.text_input("Password")

    if st.form_submit_button("➕ Add Employee"):
        insert_employee(
            (first, last, age, sex, married),
            (phone, email, location, social_links),
            education,
            experience,
            (about, hobbies, username, password)
        )
        st.session_state["added_success"] = True

# Show success message if available
if st.session_state.get("added_success"):
    st.success("✅ Employee added successfully!")
    # Clear the flag to avoid showing it on every run
    st.session_state["added_success"] = False


# --- Search Section ---
st.subheader("🔍 Search Employees")
user_query = st.text_input("Enter natural language search")
ai_model = st.selectbox("Choose AI Model", ["Gemini", "OpenAI", "DeepSeek"])

if st.button("🔎 Search"):
    try:
        sql_prompt = generate_sql_prompt(user_query)
        ai_sql = call_ai(ai_model, sql_prompt)
        cleaned_sql = clean_sql_query(ai_sql)

        results = search_employees_by_sql(cleaned_sql)
        if results:
            st.session_state.employee_options = results
            st.session_state.search_triggered = True
            st.session_state.summary_text = ""
            st.session_state.view_contact = False
        else:
            st.warning("No matching employees found.")
    except Exception as e:
        st.error(f"❌ SQL Error: {e}")

# --- Choose from multiple results ---
if st.session_state.search_triggered and st.session_state.employee_options:
    emp_names = [f"{emp['first_name']} {emp['last_name']} ({emp['email']})" for emp in st.session_state.employee_options]
    selected_idx = st.selectbox("Select an employee to generate summary:", list(range(len(emp_names))), format_func=lambda x: emp_names[x])

    if st.button("📝 Generate Summary"):
        emp = st.session_state.employee_options[selected_idx]
        st.session_state.last_employee = emp

        prompt = f"""Generate a 3-paragraph professional summary for:
Name: {emp['first_name']} {emp['last_name']}
Age: {emp['age']}
Sex: {emp['sex']}
Location: {emp['location']}
Education: {emp['education']}
About: {emp['about_self']}
Experience: {emp['experience']}
Hobbies: {emp['hobbies']}
Do not include phone, email, or contact information in the summary."""
        with st.spinner("Generating AI Summary..."):
            st.session_state.summary_text = call_ai(ai_model, prompt)

# --- Summary Output ---
if st.session_state.summary_text:
    st.subheader("📄 AI-Generated Summary")
    st.write(st.session_state.summary_text)

    if st.button("📇 Show Contact Details"):
        st.session_state.view_contact = True

# --- Contact Info Output ---
if st.session_state.view_contact and st.session_state.last_employee:
    emp = st.session_state.last_employee
    st.subheader("📞 Contact Details")
    st.markdown(f"""
- **Phone:** {emp['phone']}
- **Email:** {emp['email']}
- **Location:** {emp['location']}
- **Social:** {emp['social_links']}
""")
