import os
from collections import defaultdict

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
#from hobbyProjectWebsite import create_app
from werkzeug.security import check_password_hash, generate_password_hash

#Create a globally accessible database
db = SQLAlchemy()

def init_db(db):
    #Drop all tables
    db.drop_all()

    #Create all tables
    db.create_all()

    #Seed database
    insertUser = '''INSERT INTO users (username, password) VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');'''

    insertProject = '''INSERT INTO projects (title, body, author_id, created, image, githubURL, moreInfoURL) VALUES
  ('test title', 'test body', 1, '2018-01-01 00:00:00', 'image text', 'github URL', 'more info URL');'''

    insertComment = '''INSERT INTO comments (text, project_id, author_id, created) VALUES
  ('test comment', 1, 1, '2021-02-02 00:00:00');'''

    #Execute statements
    db.engine.execute(insertUser)
    db.engine.execute(insertProject)
    db.engine.execute(insertComment)