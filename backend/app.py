from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate
from database.models import db
from database.schemas import ma
from resources.auth import LoginResource, RegisterResource
from resources.cars import AllCarResource, UserCarResource
from resources.assignment import TeacherAssignmentResource
from resources.students_assignments import TeacherStudentAssignmentsResource, StudentsAssignmentsResource, StudentsAssignmentResource
from resources.group import GroupResource
from resources.user_text import UserTextResource
from resources.users_groups import UserGroupsResource, DeleteUserFromGroupResource
from dotenv import load_dotenv
from os import environ

# Adds variables from .env file to environment
load_dotenv()

# Creates instances of additional libraries
bcrypt = Bcrypt()
jwt= JWTManager()
cors = CORS()
migrate = Migrate()

def create_app():
    """
    App factory that creates app instance
    """
    # Creates app instance
    app = Flask(__name__)

    # Loads config properties from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

    # Registers all routes with API
    api = create_routes()

    # Registers Flask app with additional libraries created/imported above
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)

    return app


def create_routes():
    """
    Creates Flask Restful instance and registers all Resource routes
    """
    api = Api()
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(AllCarResource, '/api/cars')
    api.add_resource(UserCarResource, '/api/user_cars')
    # TODO: Create files for your Resources in resources folder, add them here
    api.add_resource(TeacherAssignmentResource, '/api/assignments')
    api.add_resource(TeacherStudentAssignmentsResource, '/api/get_student_assignments')
    api.add_resource(StudentsAssignmentsResource, '/api/myassignments')
    api.add_resource(StudentsAssignmentResource, '/api/myassignments/<int:assignment_id>')
    api.add_resource(GroupResource, '/api/mygroups')
    api.add_resource(UserGroupsResource, '/api/add_users_to_group')
    api.add_resource(DeleteUserFromGroupResource, '/api/delete_users_from_the_group/<int:users_groups_id>')
    api.add_resource(UserTextResource, '/api/my_text')
    return api
