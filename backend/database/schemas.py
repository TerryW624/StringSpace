from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, validates, ValidationError
from database.models import User, Car


ma = Marshmallow()

# Auth Schemas
class RegisterSchema(ma.Schema):
    """
    Schema used for registration, includes password
    """
    id = fields.Integer(primary_key=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    is_teacher = fields.Boolean(required=True)
    is_student = fields.Boolean(required=True)
    teacher_id = fields.Integer()

    class Meta:
        fields = ("id", "username",  "password", "first_name", "last_name", "email", "teacher_id", "is_teacher", "is_student")

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)
    
    @validates('teacher_id')
    def validate_teacher_id(self, data, **kwargs):
        if data.get("is_student", False) and "teacher_id" not in data:
            raise ValidationError("teacher_id is required for students.")
    
class UserSchema(ma.Schema):
    """
    Schema used for displaying users, does NOT include password
    """
    id = fields.Integer(primary_key=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.String(required=True)
    teacher_id = fields.Integer()
    is_teacher = fields.Boolean(required=True)
    is_student = fields.Boolean(required=True)
    class Meta:
        fields = ("id", "username", "first_name", "last_name", "email", "teacher_id", "is_teacher", "is_student")

register_schema = RegisterSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Car Schemas
class CarSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    make = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.Integer()
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=False)
    class Meta:
        fields = ("id", "make", "model", "year", "user_id", "user")
    
    @post_load
    def create_car(self, data, **kwargs):
        return Car(**data)

car_schema = CarSchema()
cars_schema = CarSchema(many=True)


# TODO: Add your schemas below
