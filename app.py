import streamlit as st
from models.employee_model import insert_employee, get_employees_by_query
from utils.sql_generator import generate_sql_from_prompt
from utils.ai_helper import call_gemini

st.set_page_config(page_title="Employee AI Summary", layout="centered")
st.title("🧠 Employee AI Summary Generator")

# Initialize session state
if "last_employee" not in st.session_state:
    st.session_state.last_employee = None
if "view_contact" not in st.session_state:
    st.session_state.view_contact = False
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""
if "employee_options" not in st.session_state:
    st.session_state.employee_options = []
if "selected_employee_index" not in st.session_state:
    st.session_state.selected_employee_index = 0
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False

# Mode switch
mode = st.radio("Choose Action", ["Add Employee", "Search & Generate Summary"])

# ---------------------- ADD EMPLOYEE ----------------------
if mode == "Add Employee":
    st.session_state.view_contact = False
    with st.form("add_form", clear_on_submit=True):
        st.subheader("Add New Employee")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", min_value=18, max_value=100)
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        married = st.checkbox("Married")
        location = st.text_input("Location")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        education = st.text_area("Education")
        social_links = st.text_input("Social Media Link")
        about_self = st.text_area("About Yourself")
        experience = st.text_area("Work Experience")
        hobbies = st.text_area("Hobbies")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Submit")
        if submitted:
            emp = {
                "first_name": first_name,
                "last_name": last_name,
                "age": age,
                "sex": sex,
                "married": married,
                "location": location,
                "phone": phone,
                "email": email,
                "education": education,
                "social_links": social_links,
                "about_self": about_self,
                "experience": experience,
                "hobbies": hobbies,
                "username": username,
                "password": password
            }
            insert_employee(emp)
            st.success("✅ Employee added successfully.")
            st.session_state.form_submitted = True

# ---------------------- SEARCH + SUMMARY ----------------------
elif mode == "Search & Generate Summary":
    st.subheader("Search Employee")
    user_query = st.text_input("Enter a search query (e.g. 'Find employee in Florida')")

    if st.button("Search"):
        sql = generate_sql_from_prompt(user_query)
        st.code(sql, language="sql")

        try:
            results = get_employees_by_query(sql)
            if results:
                st.session_state.employee_options = results
                st.session_state.search_triggered = True
                st.session_state.summary_text = ""
                st.session_state.view_contact = False
            else:
                st.warning("No results found.")

        except Exception as e:
            st.error(f"❌ Failed: {e}")

    # Ask user to choose from multiple results AFTER search
    if st.session_state.search_triggered and st.session_state.employee_options:
        employee_names = [f"{emp['first_name']} {emp['last_name']} ({emp['email']})" for emp in st.session_state.employee_options]
        selected_index = st.selectbox("Select an employee to generate summary:", list(range(len(employee_names))), format_func=lambda x: employee_names[x])

        if st.button("Generate Summary"):
            employee = st.session_state.employee_options[selected_index]
            st.session_state.selected_employee_index = selected_index
            st.session_state.last_employee = employee
            full_name = f"{employee['first_name']} {employee['last_name']}"

            prompt = f"""Generate a 3-paragraph professional summary for:
Name: {full_name}
Age: {employee['age']}
Sex: {employee['sex']}
Location: {employee['location']}
Education: {employee['education']}
About: {employee['about_self']}
Experience: {employee['experience']}
Hobbies: {employee['hobbies']}
Do not include phone, email, or contact information in the summary itself."""

            with st.spinner("Generating AI Summary..."):
                st.session_state.summary_text = call_gemini(prompt)

    # Display summary if available
    if st.session_state.summary_text:
        st.subheader("📄 AI-Generated Summary")
        st.write(st.session_state.summary_text)

    # Show Contact button only after summary
    if st.session_state.summary_text:
        if st.button("Show Contact Details"):
            st.session_state.view_contact = True

    if st.session_state.view_contact and st.session_state.last_employee:
        emp = st.session_state.last_employee
        st.subheader("📞 Contact Details")
        st.markdown(f"""
- **Phone:** {emp['phone']}
- **Email:** {emp['email']}
- **Location:** {emp['location']}
- **Social:** {emp['social_links']}
""")
