from sqlalchemy.dialects.postgresql import JSON
from flask_sqlalchemy import SQLAlchemy
import datetime 

#Create a globally accessible database
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, sqllite_autoincrement = True)
    username = db.Column(db.Text,  nullable = False, unique = True)
    password = db.Column(db.Text, nullable = False)
    
    
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, title, result_all, result_no_stop_words):
        self.title = title
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key = True, sqllite_autoincrement = True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    created = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow)
    title = db.Column(db.Text, nullable = False)
    body = db.Column(db.Text, nullable = False)
    image = db.Column(db.Text, default = None)
    githubURL = db.Column(db.Text, default = None)
    moreInfoURL = db.Column(db.Text, default = None)

    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, title, result_all, result_no_stop_words):
        self.title = title
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)