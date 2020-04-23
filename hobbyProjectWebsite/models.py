from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
import datetime 
from hobbyProjectWebsite.db import db

class User(db.Model):
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
        return '<id {}>'.format(self.id)

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

    result_all = Column(JSON)
    result_no_stop_words = Column(JSON)

    def __init__(self, author_id, created, title, body, image, githuburl = None, moreinfourl = None):
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body
        self.image = image
        self.githuburl = githuburl
        self.moreinfourl = moreinfourl

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __len__(self):
        return 8