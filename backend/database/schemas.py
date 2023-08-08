from flask_marshmallow import Marshmallow
from marshmallow import post_load, fields, validates_schema, ValidationError
from database.models import User, Car, Assignment


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
class ChordProgressionSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    user_id = fields.Integer()
    song_id = fields.String(required=True)
    user = ma.Nested(UserSchema, many=False)
    class Meta:
        fields = ("id", "user_id", "song_id", "user")
    
    @post_load
    def create_chord_progression(self, data, **kwargs):
        return ChordProgressionSchema(**data)
    
chord_progression_schema = ChordProgressionSchema()
chord_progressions_schema = ChordProgressionSchema(many=True)

class ChatSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    text = fields.String(required=True)
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=False)

    @post_load
    def create_chat(self, data, **kwargs):
        return ChatSchema(**data)
    
chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)

class GroupChatSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=True)
    chat_id = fields.Integer()
    chat = ma.Nested(ChatSchema, many=True)
    class Meta:
        fields = ("id", "user_id", "chat_id", "user", "chat")

    @post_load
    def create_group_chat(self, data, **kwargs):
        return GroupChatSchema(**data)
    
group_chat_schema = GroupChatSchema()
group_chats_schema = GroupChatSchema(many=True)

class ProjectSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    text = fields.String(required=True)
    project_item_id = fields.String()
    class Meta:
        fields = ("id", "text", "project_item_id")

    @post_load
    def create_project(self, data, **kwargs):
        return ProjectSchema(**data)
    
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

class AssignmentSchema(ma.Schema):
    id = fields.Integer(primary_key=True)
    teacher_id = fields.Integer()
    text = fields.String(required=True)
    assignment_item_id = fields.String()
    teacher = ma.Nested(UserSchema, many=False)
    class Meta:
        fields = ("id", "teacher_id", "text", "assignment_item_id", "teacher")

    @post_load
    def create_assignment(self, data, **kwargs):
        return Assignment(**data)

assignment_schema = AssignmentSchema()
assignments_schema = AssignmentSchema(many=True)



class StudentsAssignmentsSchema(ma.Schema):
    student_id = fields.Integer()
    assignment_id = fields.Integer()
    notes = fields.String()
    is_completed = fields.Boolean(required=True)
    student_check_in = fields.String(required=True)
    student = ma.Nested(UserSchema, many=False)
    assignment = ma.Nested(AssignmentSchema, many=False)

    @post_load
    def create_students_assignments(self, data, **kwargs):
        return StudentsAssignmentsSchema(**data)
    
students_assignments_schema = StudentsAssignmentsSchema()
many_students_assignments_schema = StudentsAssignmentsSchema(many=True)

class UsersProjectsSchema(ma.Schema):
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=False)
    project_id = fields.Integer()
    project = ma.Nested(ProjectSchema, many=False)

    @post_load
    def create_users_projects(self, data, **kwargs):
        return UsersProjectsSchema(**data)

users_projects_schema = UsersProjectsSchema()
many_users_projects_schema = UsersProjectsSchema(many=True)

class UsersGroupChatsSchema(ma.Schema):
    user_id = fields.Integer()
    user = ma.Nested(UserSchema, many=False)
    group_chat_id = fields.Integer()
    group_chat = ma.Nested(GroupChatSchema, many=False)

    @post_load
    def create_users_group_chats(self, data, **kwargs):
        return UsersGroupChatsSchema(**data)

users_group_chats_schema = UsersGroupChatsSchema()
many_users_group_chats_schema = UsersGroupChatsSchema(many=True)

