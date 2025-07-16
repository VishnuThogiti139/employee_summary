import streamlit as st
from models.employee_model import insert_employee_dynamic, search_employees_by_sql, get_full_employee_profile
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
    st.subheader("Personal Details")
    personal_fields = {
        "first_name": st.text_input("First Name"),
        "last_name": st.text_input("Last Name"),
        "age": st.number_input("Age", min_value=0),
        "sex": st.selectbox("Sex", ["Male", "Female", "Other"]),
        "married": st.checkbox("Married")
    }

    st.subheader("Contact Info")
    contact_fields = {
        "phone": st.text_input("Phone"),
        "email": st.text_input("Email"),
        "location": st.text_input("Location"),
        "social_links": st.text_area("Social Media Links")
    }

    st.subheader("Education & Experience")
    education_fields = {
        "education": st.text_area("Education")
    }
    experience_fields = {
        "experience": st.text_area("Experience")
    }

    st.subheader("Profile")
    profile_fields = {
        "about_self": st.text_area("About Self"),
        "hobbies": st.text_area("Hobbies"),
        "username": st.text_input("Username"),
        "password": st.text_input("Password")
    }

    if st.form_submit_button("➕ Add Employee"):
        all_fields = {}
        all_fields.update(personal_fields)
        all_fields.update(contact_fields)
        all_fields.update(education_fields)
        all_fields.update(experience_fields)
        all_fields.update(profile_fields)

        try:
            insert_employee_dynamic(all_fields)  # NEW function
            st.session_state["added_success"] = True
        except Exception as e:
            st.error(f"❌ Error adding employee: {str(e)}")
            st.session_state["added_success"] = False

# Show success message if available
if st.session_state.get("added_success"):
    st.success("✅ Employee added successfully!")
    st.session_state["added_success"] = False

# --- Search Section ---
st.subheader("🔍 Search Employees")
user_query = st.text_input("Enter natural language search")
ai_model = st.selectbox("Choose AI Model", ["Gemini", "OpenAI", "DeepSeek"])

if st.button("🔎 Search"):
    if st.session_state.employee_options:
        st.session_state.employee_options = []
    try:
        # Generate the SQL query prompt based on schema and user query
        sql_prompt = generate_sql_prompt(user_query)
        ai_sql = call_ai(ai_model, sql_prompt)

        if not ai_sql:
            st.warning("AI did not return a SQL query.")
        else:
            # Clean the SQL query
            cleaned_sql = clean_sql_query(ai_sql)

            # Use search_employees_by_sql to fetch results from the database
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
    emp_names = [f"{emp['first_name']} {emp['last_name']} - (ID) : {emp['id']}" for emp in st.session_state.employee_options]
    selected_idx = st.selectbox("Select an employee to generate summary:", list(range(len(emp_names))), format_func=lambda x: emp_names[x])

    if st.button("📝 Generate Summary"):
        emp = st.session_state.employee_options[selected_idx]
        # st.session_state.last_employee = emp
        emp_id = emp["employee_id"]
        
        # Fetch the full profile of the selected employee
        emp_full = get_full_employee_profile(emp_id)

        emp_data_str = "\n".join(f"{key}: {value}" for key, value in emp_full.items())

        prompt = f"""
        You are an expert career assistant.
        Generate a natural, professional 3-paragraph summary of employee based on the 
        following details:
        {emp_data_str}
        DO NOT include ID, contact details or sensitive information in the summary.
        highlight name, skills, education, experience, and personality strengths.
        remaining useful information.
        Make it sound confident and workplace-ready.
        """
        try:
            with st.spinner("Generating AI Summary..."):
                st.session_state.summary_text = call_ai(ai_model, prompt)
                st.session_state.last_employee = emp_full  # ✅ Update full profile here
                st.session_state.view_contact = False  # Reset contact view
        except Exception as e:
            st.error(f"❌ Error generating AI summary: {str(e)}")

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
- **Phone:** {emp.get('phone', 'N/A')}
- **Email:** {emp.get('email', 'N/A')}
- **Location:** {emp.get('location', 'N/A')}
- **Social Links:** {emp.get('social_links', 'N/A')}
""")
