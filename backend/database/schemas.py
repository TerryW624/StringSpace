from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, validates_schema, ValidationError
from database.models import *
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

    @validates_schema
    def validate_teacher_id(self, data, **kwargs):
        if data.get("is_student", True) and "teacher_id" not in data:
            raise ValidationError("teacher_id is required for students.")
        
    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)
    

    
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
class ProjectSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    text = fields.String(required=True)
    song_id = fields.String()
    video_id = fields.String()
    class Meta:
        fields = ("id", "text", "song_id", "video_id")

    @post_load
    def create_project(self, data, **kwargs):
        return Project(**data)
    
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

class AssignmentSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    teacher_id = fields.Integer()
    text = fields.String(required=True)
    teacher = ma.Nested(UserSchema, many=False)
    song_id = fields.String()
    video_id = fields.String()
    class Meta:
        fields = ("id", "teacher_id", "text", "song_id", "video_id", "teacher")

    @post_load
    def create_assignment(self, data, **kwargs):
        return Assignment(**data)

assignment_schema = AssignmentSchema()
assignments_schema = AssignmentSchema(many=True)



class StudentsAssignmentsSchema(ma.Schema):
    students_assignments_id = fields.Integer(primary_key=True)
    student_id = fields.Integer()
    assignment_id = fields.Integer()
    teacher_id = fields.Integer()
    notes = fields.String()
    is_completed = fields.Boolean()
    student_check_in = fields.String()
    student = ma.Nested(UserSchema, many=False)
    assignment = ma.Nested(AssignmentSchema, many=False)

    @post_load
    def create_students_assignments(self, data, **kwargs):
        return StudentsAssignments(**data)
    
students_assignments_schema = StudentsAssignmentsSchema()
many_students_assignments_schema = StudentsAssignmentsSchema(many=True)

class UsersProjectsSchema(ma.Schema):
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=False)
    project_id = fields.Integer()
    project = ma.Nested(ProjectSchema, many=False)

    @post_load
    def create_users_projects(self, data, **kwargs):
        return users_projects(**data)

users_projects_schema = UsersProjectsSchema()
many_users_projects_schema = UsersProjectsSchema(many=True)





