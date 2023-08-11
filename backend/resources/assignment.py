from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, Assignment, User, StudentsAssignments
from database.schemas import assignment_schema, assignments_schema, students_assignments_schema


class TeacherAssignmentResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt()
        user_id = current_user.get('id')
        is_teacher = current_user.get('is_teacher')
        if is_teacher == True:
            teacher_assignments = Assignment.query.filter_by(teacher_id=user_id)
            print(teacher_assignments)
            return assignments_schema.dump(teacher_assignments), 200
        else:
            return "Not a valid user", 401
        
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        print(current_user)
        user_id = current_user.get('id')
        is_teacher = current_user.get('is_teacher')
        if is_teacher == True:
            form_data = request.get_json()
            new_assignment = assignment_schema.load(form_data)
            new_assignment.teacher_id = user_id
            db.session.add(new_assignment)
            db.session.commit()
            students = User.query.filter_by(teacher_id=user_id)
            for student in students:
                assignment_data = {}
                new_students_assignment = students_assignments_schema.load(assignment_data)
                new_students_assignment.student_id = student.id
                new_students_assignment.assignment_id = new_assignment.id
                db.session.add(new_students_assignment)
                db.session.commit()
            return assignment_schema.dump(new_assignment), 201
        else:
            return "Not a valid user", 401

        
