🧠 Employee AI Summary Generator
A Dynamic, AI-Powered HR Assistant for Intelligent Employee Summaries
Built with Streamlit | MySQL | LLMs (Gemini / OpenAI / DeepSeek)
By Vishnu Thogiti

📌 Overview
The Employee AI Summary Generator is a full-stack Streamlit application that allows users to:

Add new employee data through a dynamic form

Search employee records using natural language

Automatically generate a professional 3-paragraph summary of an employee using Large Language Models (LLMs)

Display contact details only on demand for privacy

Works with any database schema (no hardcoded table or column names)

🎯 Key Features
Feature	Description
🔍 Natural Language Search	Uses LLMs to convert human questions to SQL
🧠 AI-Generated Summaries	Summarizes employee profile into clean, professional text
🔐 Contact Privacy	Contact info shown only after user clicks “Show Contact”
📊 Dynamic Schema Handling	Adapts to any MySQL schema using SHOW TABLES and DESCRIBE
🔁 Multi-Model LLM Support	Gemini (working), OpenAI, and DeepSeek pluggable
🧱 Modular Code Design	Clean separation into models, utils, and api folders
🧪 Prompt Engineering	Safe, structured AI prompts without leaking private data

🖼️ UI Screens (Optional)
<details> <summary>Click to Expand</summary>
Add Employee via Sidebar

Natural Language Search Bar

Model Selector (Gemini/OpenAI/DeepSeek)

Summary Output Section

Contact Info Section (hidden until button click)

</details>
🧰 Tech Stack
Frontend/UI: Streamlit

Backend: Python, MySQL

AI/LLM APIs: Gemini (working), OpenAI (optional), DeepSeek (optional)

Database Interaction: MySQL Connector

LLM Prompting: Prompt engineering modules for summary + SQL generation

EMPLOYEE_SUMMARY-MAIN/
├── __pycache__/
├── _chroma_store/
├── libs/
│   ├── models/
│   │   ├── __pycache__/
│   │   └── employee_model.py
│   ├── routes/
│   │   ├── add_employee.py
│   │   ├── ai_summary.py
│   │   ├── dv/
│   │   └── get_employee.py
│   └── utils/
│       ├── __pycache__/
│       ├── ai_helper.py
│       ├── db.py
│       ├── extract_schema.py
│       ├── sql_generator.py
│       └── vector_store.py
├── .env
├── app.py
├── config.py
├── Need_to_change.txt
├── Readme.txt
└── requirements.txt

🚀 How to Run Locally

✅ Prerequisites
Python 3.9+

MySQL Server running locally with correct schema

Gemini API Key (or replace with your own LLM)

📦 Setup

git clone https://github.com/your-username/employee-ai-summary.git
cd employee-ai-summary

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🔑 Add your Gemini API Key
In utils/ai_helper.py, insert your Gemini key:


genai.configure(api_key="YOUR_GEMINI_API_KEY")

▶️ Run the App

streamlit run app.py

🔮 Future Extensions

 Add CSV bulk upload

 Enable feedback-based AI prompt refinement

 Secure deployment (Streamlit Cloud + GCP/AWS MySQL)

 RAG-based resume/doc parsing

 PDF/Word summary exports

 Role-based authentication (HR/Admin/Guest)

 Integration into Microsoft Power Platform (for enterprise use)

🙏 Acknowledgments
Special thanks to:

Gemini API for fast AI-powered responses

Streamlit for rapid UI building

MySQL for relational data modeling
##sql

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
