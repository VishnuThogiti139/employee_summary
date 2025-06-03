from flask import Blueprint, jsonify
from utils.db import get_db_connection

get_employee_bp = Blueprint('get_employee', __name__)

@get_employee_bp.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(employees)
