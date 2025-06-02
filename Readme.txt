"I built a full-stack Python web application that collects employee data, stores it in a MySQL database, and uses Google’s Gemini AI to generate human-like summaries and SQL queries based on user input."

📦 Technologies & Tools Used
**Python (Flask)**: Used to build the backend REST API and serve the web UI.

**MySQL**: Stores all employee data in a structured table.

**Postman**: Used for testing the API endpoints like /add, /search, and /summary.

**HTML (Jinja2 templates)**: Displays the frontend interface for searching and showing summaries.

**Google Gemini Pro API**: AI model that converts user queries into SQL and generates natural-language summaries of employees.

🔁 How the System Works (Flow)
Add Employee:

A user submits employee details (name, age, job info, etc.) via Postman or frontend.

This data is saved into the employees table in MySQL using a POST API.

Search Employee (AI SQL Generator):

The user enters a natural language query like:
"Find employees in Dallas"

The query is sent to Gemini AI, which returns a raw SQL query:
SELECT * FROM employees WHERE location LIKE '%Dallas%';

That SQL is executed in MySQL, and matching employee records are returned.

Generate AI Summary:

The selected employee record is sent to Gemini again.

Gemini responds with a professional 3-paragraph summary based on their profile.

Contact Info:

The user can click a "Contact" button (or use another endpoint) to view the employee’s email, phone, and LinkedIn.