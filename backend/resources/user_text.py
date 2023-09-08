from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, UserText, User
from database.schemas import user_text_schema, user_texts_schema

class UserTextResource(Resource):        
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if user_id:
            form_data = request.get_json()
            new_text = user_text_schema.load(form_data)
            new_text.user_id = user_id
            db.session.add(new_text)
            db.session.commit()
            return user_text_schema.dump(new_text), 201
        else:
            return "Not a valid user", 401
