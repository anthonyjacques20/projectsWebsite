from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
import datetime 
from hobbyProjectWebsite.db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(Text,  nullable = False, unique = True)
    password = Column(Text, nullable = False)
    
    
    result_all = Column(JSON)
    result_no_stop_words = Column(JSON)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}, username {}>'.format(self.id, self.username)

    def __len__(self):
        return 3

class Project(db.Model):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key = True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    created = Column(DateTime, nullable = False, default = datetime.datetime.utcnow)
    title = Column(Text, nullable = False)
    body = Column(Text, nullable = False)
    image = Column(Text, default = None, nullable = False)
    githuburl = Column(Text, default = None)
    moreinfourl = Column(Text, default = None)
    supportimages = Column(Text, default = None)

    result_all = Column(JSON)
    result_no_stop_words = Column(JSON)

    def __init__(self, author_id, created, title, body, image, githuburl = None, moreinfourl = None, supportimages = None):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body
        self.image = image
        self.githuburl = githuburl
        self.moreinfourl = moreinfourl
        self.supportimages = supportimages

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __len__(self):
        return 9

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key = True)
    text = Column(Text,  nullable = False, unique = True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable = False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    created = Column(DateTime, nullable = False, default = datetime.datetime.utcnow)

    
    
    result_all = Column(JSON)
    result_no_stop_words = Column(JSON)

    def __init__(self, text, project_id, author_id, created):
        self.text = text
        self.project_id = project_id
        self.author_id = author_id
        self.created = created

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __len__(self):
        return 4