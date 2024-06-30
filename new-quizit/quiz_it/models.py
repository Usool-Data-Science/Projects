from quiz_it import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create the database models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profession = db.Column(db.Enum('Student', 'Teacher', 'Others'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    area_of_interest = db.Column(db.String(50))
    school = db.Column(db.String(50))
    school_id = db.Column(db.Integer, nullable=False)
    histories = db.relationship('History', backref='owner', lazy=True)
    questions = db.relationship('Question', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.id}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.String(20), nullable=False)
    export_type = db.Column(db.Enum('Download', 'On-page'))
    quiz_count = db.Column(db.Integer, nullable=False)
    user_mode = db.Column(db.Enum('Student', 'Teacher', 'Others'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mcqs = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"History('{self.id}', '{self.category}', '{self.quiz_count}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.String(20), nullable=False)
    quiz_count = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mcqs = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Question('{self.id}', '{self.category}', '{self.user_id}')"
