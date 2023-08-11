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
class UserText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    usertext = db.Column(db.String(255), nullable=False)
    user = db.relationship("User")

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_text_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(255), nullable=True)
    song_id = db.Column(db.String(255), nullable=True)
    video_id = db.Column(db.String(255), nullable=True)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(255), nullable=False)
    teacher = db.relationship("User")
    song_id = db.Column(db.String(255), nullable=True)
    video_id = db.Column(db.String(255), nullable=True)

class StudentsAssignments(db.Model):
    students_assignments_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    student = db.relationship("User")
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))
    assignment = db.relationship("Assignment")
    notes = db.Column(db.String(255), nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    student_check_in = db.Column(db.String(255), nullable=True)

users_groups = db.Table("users_groups",
                          db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                          db.Column("group_id", db.Integer, db.ForeignKey("group.id")))


