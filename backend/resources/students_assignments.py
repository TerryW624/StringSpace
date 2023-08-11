from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource
from database.models import db, StudentsAssignments, User
from database.schemas import many_students_assignments_schema, students_assignments_schema

class StudentsAssignmentsResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt()
        user_id = current_user.get('id')
        is_student = current_user.get('is_student')
        teacher_id = current_user.get('teacher_id')
        if is_student == True and teacher_id:
            student_assignments = StudentsAssignments.query.filter_by(student_id=user_id)
            return many_students_assignments_schema.dump(student_assignments), 200
        else:
            return "Not a valid user", 401

class StudentsAssignmentResource(Resource):
#     @jwt_required()
#     def get(self, students_assignments_id):
#         user_id = get_jwt_identity()
#         student_assignment = 

    @jwt_required()
    def put(self, assignment_id):
        current_user = get_jwt()
        user_id = current_user.get('id')
        is_student = current_user.get('is_student')
        teacher_id = current_user.get('teacher_id')
        if is_student == True and teacher_id:
            form_data = request.get_json()
            print("form data: ", form_data)
            assignment = StudentsAssignments.query.filter_by(student_id=user_id, assignment_id=assignment_id).first()
            assignment.is_completed = form_data.get('is_completed')
            assignment.notes = form_data.get('notes')
            assignment.student_check_in = form_data.get('student_check_in')
            # assignment.verified = True
            db.session.commit()
            return students_assignments_schema.dump(assignment)        
        else:
            return "Not a valid user", 401
        
class TeacherStudentAssignmentsResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt()
        user_id = current_user.get('id')
        is_teacher = current_user.get('is_teacher')
        if is_teacher == True:
            students = User.query.filter_by(teacher_id=user_id)
            student_assignments = []
            for student in students:
                student_assignments += StudentsAssignments.query.filter_by(student_id=student.id)
            return many_students_assignments_schema.dump(student_assignments), 200
        else:
            return "Not a valid user", 401