from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, Assignment
from database.schemas import assignment_schema, assignments_schema


class TeacherAssignmentResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt()
        user_id = current_user.get('id')
        is_teacher = current_user.get('is_teacher')
        if is_teacher == True:
            teacher_assignments = Assignment.query.filter_by(user_id=user_id)
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
            return assignment_schema.dump(new_assignment), 201
        else:
            return "Not a valid user", 401

        
