from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, Chat
from database.schemas import chat_schema, chats_schema

class ChatResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user_chats = Chat.query.filter_by(user_id=user_id)
        return chats_schema.dump(user_chats), 200