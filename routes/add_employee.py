from flask import Blueprint, request, jsonify
from models.employee_model import insert_employee

add_employee_bp = Blueprint('add_employee', __name__)

@add_employee_bp.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    # Validate minimum required fields
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({"error": "first_name and last_name are required"}), 400

    try:
        insert_employee(data)
        return jsonify({"message": "Employee added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
