from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager, db
import config

from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy='dynamic')

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.Text, nullable=False)
    task = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

