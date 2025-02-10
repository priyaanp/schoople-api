from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    amount_per_student = db.Column(db.String)
    min_student_count = db.Column(db.String)
    launch = db.Column(db.Date)
    expiry = db.Column(db.Date)  # Assuming expiry is stored as a date
    type = db.Column(db.String)
    status = db.Column(db.Boolean)

class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    offer_percentage = db.Column(db.String)
    discount_amount = db.Column(db.String)
    additional_amount = db.Column(db.String)
    launch = db.Column(db.Date)
    expiry = db.Column(db.Date)
    is_school_secific = db.Column(db.Boolean)
    status = db.Column(db.Boolean)

    subscription = db.relationship('Subscription', backref='offers', lazy=True)

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String, nullable=False)
    role_type = db.Column(db.String, nullable=False)  # Can be 'admin', 'staff', or 'student'
    is_active = db.Column(db.Boolean, default=True)
    
    
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    staff = db.relationship('Staff', backref='user', lazy='joined')
    roles = db.relationship('Role', secondary='user_roles', backref='users')
    def set_password(self, raw_password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(raw_password)


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)    

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)    

class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    syllabus = db.Column(db.String, nullable=True)  # E.g., CBSE, ICSE, State Board
    status = db.Column(db.Boolean, default=True)    

class AcademicYear(db.Model):
    __tablename__ = 'academic_years'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=False)   
    

class SchoolSubscription(db.Model):
    __tablename__ = 'school_subscription'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'), nullable=True)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    no_of_students_subscription = db.Column(db.String, nullable=True)
    subscription_amount = db.Column(db.String, nullable=True)
    payment_status = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, default=True)
    subscription_date = db.Column(db.Date, nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)

    school = db.relationship('School')
    subscription = db.relationship('Subscription')
    offer = db.relationship('Offer')
    academic_year = db.relationship('AcademicYear')    

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String, nullable=False)
    menu_name = db.Column(db.String, nullable=False)
    module_link = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)  # Allow null for parent_id
    is_active = db.Column(db.Boolean, default=True)
    is_visible_in_app = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer)  # Allow null for parent_id

    parent = db.relationship('Module', remote_side=[id], backref=db.backref('children', lazy='dynamic'))

class SchoolSubscriptionModuleRolePermission(db.Model):
    __tablename__ = 'school_subscription_module_role_permission'

    id = db.Column(db.Integer, primary_key=True)
    school_subscription_id = db.Column(db.Integer, db.ForeignKey('school_subscription.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), nullable=False)

    school_subscription = db.relationship('SchoolSubscription')
    module = db.relationship('Module')
    role = db.relationship('Role')
    permission = db.relationship('Permission')        

class StaffType(db.Model):
    __tablename__ = 'staff_types'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)    

class Staff(db.Model):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    staff_type_id = db.Column(db.Integer, db.ForeignKey('staff_types.id'), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String, nullable=False)
    permanent_address = db.Column(db.String)
    communication_address = db.Column(db.String)
    blood_group = db.Column(db.String)
    qualification = db.Column(db.String)
    is_section_in_charge = db.Column(db.Boolean, default=False)
    section_details = db.Column(db.String)
    is_transport_in_charge = db.Column(db.Boolean, default=False)
    transport_details = db.Column(db.String)
    joining_date = db.Column(db.Date)
    relieving_date = db.Column(db.Date)
    relieving_comment = db.Column(db.String)
    status = db.Column(db.Boolean, default=True)

    school = db.relationship('School', backref='staffs')
    staff_type = db.relationship('StaffType', backref='staffs')
    staffs_grades = db.relationship('StaffsGrades', back_populates='staff')

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    status = db.Column(db.Boolean, default=True)

    school = db.relationship('School', backref='clubs')




class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    student_code = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=True)
    aadhar_number = db.Column(db.String, nullable=True)
    photo = db.Column(db.String, nullable=True)
    date_of_admission = db.Column(db.Date, nullable=True)
    admission_number = db.Column(db.String, nullable=True)
    identification_mark = db.Column(db.String, nullable=True)
    interests = db.Column(db.String, nullable=True)
    hobbies = db.Column(db.String, nullable=True)
    student_email = db.Column(db.String, nullable=True)
    religion = db.Column(db.String, nullable=True)
    caste = db.Column(db.String, nullable=True)
    permanent_address = db.Column(db.String, nullable=True)
    communication_address = db.Column(db.String, nullable=True)
    mother_name = db.Column(db.String, nullable=True)
    father_name = db.Column(db.String, nullable=True)
    father_qualification = db.Column(db.String, nullable=True)
    mother_qualification = db.Column(db.String, nullable=True)
    father_occupation = db.Column(db.String, nullable=True)
    mother_occupation = db.Column(db.String, nullable=True)
    father_mobile = db.Column(db.String, nullable=True)
    mother_mobile = db.Column(db.String, nullable=True)
    father_email = db.Column(db.String, nullable=True)
    mother_email = db.Column(db.String, nullable=True)
    annual_income = db.Column(db.String, nullable=True)
    blood_group = db.Column(db.String, nullable=True)
    mother_tongue = db.Column(db.String, nullable=True)
    is_single_girl = db.Column(db.Boolean, default=False)
    is_minority = db.Column(db.Boolean, default=False)
    sibling_status = db.Column(db.Boolean, default=False)
    relieving_date = db.Column(db.Date, nullable=True)
    relieving_comment = db.Column(db.String, nullable=True)
    status = db.Column(db.Integer, nullable=True)

    # Relationships
    school = db.relationship('School', backref='students')  # Relates to the `schools` table

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.first_name} {self.last_name}, school_id={self.school_id})>"

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String, nullable=False)

    # Relationship with the School model
    school = db.relationship('School', backref='grades')

    def __repr__(self):
        return f"<Grade(id={self.id}, title={self.title})>"

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String, nullable=False)

    # Relationship with the School model
    school = db.relationship('School', backref='sections')

    def __repr__(self):
        return f"<Section(id={self.id}, title={self.title})>"
    
class SchoolsGradesSections(db.Model):
    __tablename__ = 'schools_grades_sections'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)

    school = db.relationship('School', backref='grades_sections')
    grade = db.relationship('Grade', backref='grades_sections')
    section = db.relationship('Section', backref='grades_sections')
    academic_year = db.relationship('AcademicYear', backref='grades_sections')

    def __repr__(self):
        return f"<SchoolsGradesSections(id={self.id})>"

class House(db.Model):
    __tablename__ = 'houses'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    color = db.Column(db.String, nullable=True)
    status = db.Column(db.Boolean, default=True)

    school = db.relationship('School', backref='houses')

    def __repr__(self):
        return f"<House(id={self.id}, title={self.title}, school_id={self.school_id})>"

class Transport(db.Model):
    __tablename__ = 'transports'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    driver_code = db.Column(db.String, nullable=False)
    vehicle_number = db.Column(db.String, nullable=False)
    route_number = db.Column(db.String, nullable=False)
    route_name = db.Column(db.String, nullable=False)
    vehicle_gps_device_id = db.Column(db.String, nullable=True)
    vehicle_tracking_url = db.Column(db.String, nullable=True)
    in_charge_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)

    # Relationships
    driver = db.relationship('Staff', foreign_keys=[driver_id])
    in_charge = db.relationship('Staff', foreign_keys=[in_charge_id])
    school = db.relationship('School', backref='transports')

class SchoolStudent(db.Model):
    __tablename__ = 'school_student'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=True)
    clubs = db.Column(db.String, nullable=True)  # Assuming it's a comma-separated string
    school_grade_section_id = db.Column(db.Integer, db.ForeignKey('schools_grades_sections.id'), nullable=True)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    transport_id = db.Column(db.Integer, db.ForeignKey('transports.id'), nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=True)  # Active/Inactive
    roll_number = db.Column(db.String, nullable=True)

    # Relationships
    student = db.relationship('Student', backref='school_student', lazy=True)
    house = db.relationship('House', backref='school_students', lazy=True)
    grade_section = db.relationship('SchoolsGradesSections', backref='school_students', lazy=True)
    academic_year = db.relationship('AcademicYear', backref='school_students', lazy=True)
    transport = db.relationship('Transport', backref='school_students', lazy=True)

    def __repr__(self):
        return f"<SchoolStudent(id={self.id}, student_id={self.student_id}, status={self.status})>"
    
class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    title = db.Column(db.String, nullable=False)

    school = db.relationship('School', backref='subjects', lazy=True)

    def __repr__(self):
        return f"<Subject id={self.id}, title={self.title}, school_id={self.school_id}>"


    
class StaffsGrades(db.Model):
    __tablename__ = 'staffs_grades'

    id = db.Column(db.Integer, primary_key=True)
    schools_grades_sections_id = db.Column(db.Integer, db.ForeignKey('schools_grades_sections.id'), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)
    transport_id = db.Column(db.Integer, db.ForeignKey('transports.id'), nullable=True)
    is_class_in_charge = db.Column(db.Boolean, nullable=False, default=False)
    is_class_in_charge_second = db.Column(db.Boolean, nullable=False, default=False)
    is_transport_in_charge = db.Column(db.Boolean, nullable=False, default=False)
    class_in_charge_id = db.Column(db.Integer, db.ForeignKey('schools_grades_sections.id'), nullable=False)    
    class_in_charge_second_id = db.Column(db.Integer, db.ForeignKey('schools_grades_sections.id'), nullable=False)

    # Relationships
    school_grade_section = db.relationship(
        'SchoolsGradesSections', 
        foreign_keys=[schools_grades_sections_id]
    )
    staff = db.relationship('Staff', back_populates='staffs_grades')
    subject = db.relationship('Subject')
    transport = db.relationship('Transport')
    class_in_charge_section = db.relationship(
        'SchoolsGradesSections', 
        foreign_keys=[class_in_charge_id]
    )
    class_in_charge_second_section = db.relationship(
        'SchoolsGradesSections', 
        foreign_keys=[class_in_charge_second_id]
    )
    schools_grades_sections = db.relationship(
        'SchoolsGradesSections',
        backref='staffs_grades',
        foreign_keys=[schools_grades_sections_id]  # Specify the foreign key explicitly
    )
class ExamMarks(db.Model):
    __tablename__ = 'exam_marks'
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)

class ExamMarkDetails(db.Model):
    __tablename__ = 'exam_mark_details'
    id = db.Column(db.Integer, primary_key=True)
    exam_mark_id = db.Column(db.Integer, db.ForeignKey('exam_marks.id'), nullable=False)
    evaluation_type = db.Column(db.String(50), nullable=False)
    weightage = db.Column(db.Float, nullable=False)
    marks_obtained = db.Column(db.Float, nullable=False)
    marks_out_of = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<StaffsGrades id={self.id}, staff_id={self.staff_id}, schools_grades_sections_id={self.schools_grades_sections_id}>"
    
class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    schools_grades_sections_id = db.Column(db.Integer, db.ForeignKey('schools_grades_sections.id'), nullable=False)
    is_hourly = db.Column(db.Boolean, default=False)
    attendence_date = db.Column(db.Date, nullable=False)
    period = db.Column(db.String, nullable=True)
    time_slot = db.Column(db.Integer, nullable=True)
    is_present_morning = db.Column(db.Boolean, default=False)
    is_present_afternoon = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)
    created_on = db.Column(db.Date, nullable=False)
    updated_by = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=True)
    updated_on = db.Column(db.Date, nullable=True)

    # Relationships
    student = db.relationship('Student', backref='attendances')
    staff = db.relationship('Staff', foreign_keys=[staff_id], backref='attendances_created')
    created_by_staff = db.relationship('Staff', foreign_keys=[created_by], backref='attendances_creator')
    updated_by_staff = db.relationship('Staff', foreign_keys=[updated_by], backref='attendances_updater')
    schools_grades_sections = db.relationship('SchoolsGradesSections', backref='attendances')

    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, staff_id={self.staff_id}, attendence_date={self.attendence_date})>"

class TimeTable(db.Model):
    __tablename__ = 'time_tables'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    schools_grades_sections_id = db.Column(db.Integer, db.ForeignKey('schools_grades_sections.id'), nullable=False)

    # Relationships
    academic_year = db.relationship('AcademicYear', backref='time_tables', lazy=True)
    school = db.relationship('School', backref='time_tables', lazy=True)
    grade_section = db.relationship('SchoolsGradesSections', backref='time_tables', lazy=True)

    # Single relationship for details
    time_table_details = db.relationship('TimeTableDetails', backref='time_table', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<TimeTable(id={self.id}, school_id={self.school_id}, academic_year_id={self.academic_year_id})>"


class TimeTableDetails(db.Model):
    __tablename__ = 'time_table_details'

    id = db.Column(db.Integer, primary_key=True)
    time_table_id = db.Column(db.Integer, db.ForeignKey('time_tables.id'), nullable=False)
    day_name = db.Column(db.String, nullable=False)
    order_number = db.Column(db.Integer, nullable=True)
    time_slot = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staffs.id'), nullable=False)

    # Relationships
    subject = db.relationship('Subject', backref='time_table_details', lazy=True)
    staff = db.relationship('Staff', backref='time_table_details', lazy=True)

    def __repr__(self):
        return (f"<TimeTableDetails(id={self.id}, day_name={self.day_name}, "
                f"time_slot={self.time_slot}, subject_id={self.subject_id}, staff_id={self.staff_id})>")

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title})>" 