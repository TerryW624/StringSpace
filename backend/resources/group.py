from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, Group, UserText, UsersGroups
from database.schemas import group_schema, groups_schema, user_texts_schema, many_users_groups_schema, users_groups_schema
import json

class GroupResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            groups = UsersGroups.query.filter_by(user_id=user_id)
            return many_users_groups_schema.dump(groups), 200
        else:
            return "Not a valid user", 401

    @jwt_required()
    def post(self):
        current_user = get_jwt()
        print(current_user)
        user_id = current_user.get('id')
        if user_id:
            form_data = request.get_json()
            new_group = group_schema.load(form_data)
            db.session.add(new_group)
            db.session.commit()
            user_data = {
                "user_id": user_id,
                "group_id": new_group.id
            }
            new_users_group = users_groups_schema.load(user_data)
            # new_users_group.user_id = user_id
            # new_users_group.group_id = new_group.id
            db.session.add(new_users_group)
            db.session.commit()
            group = group_schema.dump(new_group)
            return group, 201
        else:
            return "Not a valid user", 401
        

