AI-Powered Employee Summary App
A modular, extensible Streamlit-based web application to manage employee data, generate intelligent summaries using AI (Gemini, OpenAI, or DeepSeek), and display professional summaries and contact details.

🚀 Features
📋 Add employee details with modular data handling

🔍 Search employees using natural language queries

🤖 AI-generated summaries using selected LLMs

📇 Contact info display with summary

🧠 Supports multiple AI models: Gemini, OpenAI, and DeepSeek

🗃️ Modular MySQL database with normalized tables

🛠️ Tech Stack
Component	Tech
Frontend UI	Streamlit
Backend	Python, SQL, AI model integration
AI Models	Gemini, OpenAI GPT, DeepSeek (placeholder)
Database	MySQL with normalized schema
ORM / Queries	Raw SQL using mysql-connector-python

🗃️ Database Schema
The app uses a normalized relational schema. Key tables:

##sql
Copy
Edit
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    sex VARCHAR(10),
    married BOOLEAN
);

CREATE TABLE employee_contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    phone VARCHAR(20),
    email VARCHAR(100),
    location VARCHAR(100),
    social_links TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE employee_education (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    education TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE employee_experience (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    experience TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE employee_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    about_self TEXT,
    hobbies TEXT,
    username VARCHAR(50),
    password VARCHAR(255),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
📦 Project Structure
bash
Copy
Edit
employee_summary_app/
│
├── app.py                      # Streamlit UI app
├── config.py                   # API keys & DB config
│
├── models/
│   ├── __init__.py
│   └── employee_model.py       # Insert/search logic
│
├── utils/
│   ├── __init__.py
│   ├── ai_helper.py            # Call Gemini/OpenAI/DeepSeek
│   └── sql_generator.py        # Natural language → SQL
│
├── requirements.txt            # Dependencies
└── README.md                   # You're here!
#🔑 Config Setup
Edit config.py:

▶️ How to Run
1. 📦 Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
2. 🛢️ Create MySQL Database
sql
Copy
Edit
CREATE DATABASE employee_ai;
-- Then run the CREATE TABLE statements listed above
3. 🧠 Add API Keys
Update your config.py file with real API keys from:

https://ai.google.dev/ (Gemini)

https://platform.openai.com/ (OpenAI)

4. 🚀 Run the App
bash
Copy
Edit
streamlit run app.py
#💬 Example Queries
Try these natural queries in the UI:

employees in Texas with MBA

female employees from California

who lives in Florida and has MSc degree


📌 Notes
DeepSeek integration is a placeholder unless their API is available.

Ensure your MySQL user has full permissions to the employee_ai DB.

Handle API rate limits and timeouts gracefully for large user loads.








