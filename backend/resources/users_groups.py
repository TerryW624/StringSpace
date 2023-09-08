from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, UsersGroups 
from database.schemas import users_groups_schema, many_users_groups_schema

class UserGroupsResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt()
        print(current_user)
        current_user_id = current_user.get('id')
        if current_user_id:
            form_data = request.get_json()
            new_group_user = users_groups_schema.load(form_data)
            db.session.add(new_group_user)
            db.session.commit()
            return users_groups_schema.dump(new_group_user), 201
        else:
            return "Not a valid user", 401
        
class DeleteUserFromGroupResource(Resource):
    @jwt_required()
    def delete(self, users_groups_id):
        user_from_group = UsersGroups.query.get_or_404(users_groups_id)
        db.session.delete(user_from_group)
        db.session.commit()
        return '', 204