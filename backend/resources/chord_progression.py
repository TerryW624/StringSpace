from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask_restful import Resource
from database.models import db, Assignment
from database.schemas import assignment_schema, assignments_schema



