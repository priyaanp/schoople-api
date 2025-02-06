from datetime import timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import AcademicYear, SchoolStudent, SchoolsGradesSections, TimeTable, TimeTableDetails, db, User, Student
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from werkzeug.security import check_password_hash
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'a6r2iLt8P7$%@!>98uQ/!h2FwXs'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
# Choose the configuration based on an environment variable or hardcoded value
env = 'development'  # Change to 'testing' or 'production' as needed

if env == 'development':
    app.config.from_object(DevelopmentConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
elif env == 'production':
    app.config.from_object(ProductionConfig)

db.init_app(app)
jwt = JWTManager(app)

# Login Endpoint
@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login and return student data with a JWT token."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check for user existence
    user = User.query.filter_by(username=username, is_active=True).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Retrieve student details
    student = Student.query.filter_by(id=user.student_id).first()
    if not student:
        return jsonify({"error": "No student data available for this user."}), 404

    # Get school_student and grade/section details
    school_student = SchoolStudent.query.filter_by(student_id=student.id).first()
    grade_section = (
        SchoolsGradesSections.query.filter_by(id=school_student.school_grade_section_id).first()
        if school_student else None
    )

    grade = grade_section.grade.title if grade_section and grade_section.grade else None
    section = grade_section.section.title if grade_section and grade_section.section else None
    active_academic_year = AcademicYear.query.filter_by(active=True).first()

    # Student response data
    student_data = {
        "school_id": grade_section.school_id,
        "school_code": grade_section.school.title,
        "school_name": grade_section.school.code,
        "school_grade_section_id": grade_section.id,
        "active_academic_year_id":active_academic_year.id,
        "student_id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "middle_name": student.middle_name,
        "dob": student.dob,
        "photo": student.photo,
        "admission_number": student.admission_number,
        "student_code": student.student_code,
        "father_name": student.father_name,
        "mother_name": student.mother_name,
        "grade": grade,
        "section": section,
        "aadhar_number": student.aadhar_number,
        "permanent_address": student.permanent_address,
        "communication_address": student.communication_address,
        "hobbies": student.hobbies,
        "father_email": student.father_email,
        "mother_email": student.mother_email,
        "annual_income": student.annual_income,
        "blood_group": student.blood_group,
        "status": student.status,
    }

    # Create a token
    token = create_access_token(identity=str(user.id))

    return jsonify({"token": token, "student_data": student_data}), 200

@app.route('/api/student-data/<int:id>', methods=['GET'])
@jwt_required()
def get_student_data(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    


    student = Student.query.filter_by(id=id).first()
    if not student:
        return jsonify({"error": "No student data available for this user."}), 404

    # Get school_student and grade/section details
    school_student = SchoolStudent.query.filter_by(student_id=student.id).first()
    grade_section = (
        SchoolsGradesSections.query.filter_by(id=school_student.school_grade_section_id).first()
        if school_student else None
    )

    grade = grade_section.grade.title if grade_section and grade_section.grade else None
    section = grade_section.section.title if grade_section and grade_section.section else None
    active_academic_year = AcademicYear.query.filter_by(active=True).first()
    # Student response data
    student_data = {
        "school_id": grade_section.school_id,
        "school_code": grade_section.school.title,
        "school_name": grade_section.school.code,
        "school_grade_section_id": grade_section.id,
        "active_academic_year_id":active_academic_year.id,
        "student_id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "middle_name": student.middle_name,
        "dob": student.dob,
        "photo": student.photo,
        "admission_number": student.admission_number,
        "student_code": student.student_code,
        "father_name": student.father_name,
        "mother_name": student.mother_name,
        "grade": grade,
        "section": section,
        "aadhar_number": student.aadhar_number,
        "permanent_address": student.permanent_address,
        "communication_address": student.communication_address,
        "hobbies": student.hobbies,
        "father_email": student.father_email,
        "mother_email": student.mother_email,
        "annual_income": student.annual_income,
        "blood_group": student.blood_group,
        "status": student.status,
    }

    return jsonify({"student_data": student_data}), 200

@app.route('/api/timetable-details', methods=['GET'])
def get_timetable_details():
    # Fetch query parameters
    academic_year_id = request.args.get('academic_year_id')
    school_id = request.args.get('school_id')
    school_grade_section_id = request.args.get('school_grade_section_id')

    if not (academic_year_id and school_id and school_grade_section_id):
        return jsonify({"error": "Missing required query parameters"}), 400

    # Query the timetable and related details
    timetable = TimeTable.query.filter_by(
        school_id=school_id,
        academic_year_id=academic_year_id,
        schools_grades_sections_id=school_grade_section_id
    ).first()

    if not timetable:
        return jsonify([])  # Return an empty list if no timetable exists

    # Fetch timetable details
    details = TimeTableDetails.query.filter_by(time_table_id=timetable.id).order_by(TimeTableDetails.order_number.asc()).all()

    # Format response
    response_data = [
        {
            "day_name": detail.day_name,
            "order_number": detail.order_number,
            "time_slot": detail.time_slot,
            "subject": detail.subject.title if detail.subject else "N/A",
            "staff": f"{detail.staff.first_name} {detail.staff.last_name}" if detail.staff else "N/A"
        }
        for detail in details
    ]

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)


