from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    teacher_id = db.Column(db.Integer, nullable=True)
    is_teacher = db.Column(db.Boolean, nullable=False)
    is_student = db.Column(db.Boolean, nullable=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.username

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    # Adds user_id as an Integer column on the car table which references the id column on user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Establishes object relation between car-user so we can grab values like car.user.username
    user = db.relationship("User")

# TODO: Add your models below, remember to add a new migration and upgrade database
class ChordProgression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    song_id = db.Column(db.String(255), nullable=False)
    user = db.relationship("User")

class GroupChat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"))
    user = db.relationship("User")
    chat = db.relationship("Chat")

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=True)
    project_item_id = db.Column(db.String(255), nullable=True)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(255), nullable=False)
    assignment_item_id = db.Column(db.String(255), nullable=False)
    teacher = db.relationship("User")

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")

students_assignments = db.Table("students_assignments",
                                db.Column("student_id", db.Integer, db.ForeignKey("user.id")),
                                db.Column("assignment_id", db.Integer, db.ForeignKey("assignment.id")),
                                db.Column("notes", db.String(255)),
                                db.Column("is_completed", db.Boolean),
                                db.Column("student_check_in", db.String(255)))

users_projects = db.Table("users_projects",
                          db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                          db.Column("project_id", db.Integer, db.ForeignKey("project.id")))

users_group_chats = db.Table("users_group_chats",
                             db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                             db.Column("group_chat_id", db.Integer, db.ForeignKey("group_chat.id")))

