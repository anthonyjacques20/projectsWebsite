import sqlite3
import os
from collections import defaultdict

import click
from flask import current_app, g
from flask.cli import with_appcontext

from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #This tells the connection to return rows that behave like dicts
        g.db.row_factory = sqlite3.Row
        print("Added db to g")

    return g.db

def close_db(e=None):
    db= g.pop('db', None)

    if db is not None:
        db.close()

def seed_db(db = None):
    if db is None:
        db = get_db()

    #Create a dummy author
    author = {
        "username": "baller",
        "password": generate_password_hash(os.environ["DB_BALLERPASSWORD"])
    }
    #Save the author
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (author["username"], author["password"])
    )
    #Must call db.commit() to save the changese made in the insert above
    db.commit()

    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (author["username"],)
    ).fetchone()

    posts = [
        {
            "title": "Senior Project",
            "body": "Used an arduino with different physical inputs (heartbeat sensors) and outputs (turn signals) to create both an exercise and safety system. Utilized object oriented programming in C to create user objects with weight, age, height, calories burned, etc.",
            "author_id": user['id'],
            "image": "/static/SeniorProjectRearView.jpg"
        },
        {
            "title": "Linear Motion Cabinet",
            "body": "Project to build a cabinet that has uses a Raspberry Pi and a worm gear to raise and lower the cabinet. The ultimate goal being to be able put a projector in the cabinet and be able to hide the projector when it is not in use. I am planning on incorporating commands into a Google Home to be able to send request to the Raspberry Pi.",
            "author_id": user['id'],
            "image": "https://images.unsplash.com/photo-1535016120720-40c646be5580?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80",
            "githubURL": "https://github.com/anthonyjacques20/Linear-Motion-Cabinet"
        },
        {
            "title": "Web Developer Bootcamp",
            "body": "Completed a web developer bootcamp using NodeJS, Express, and MongoDB to learn about web development.",
            "author_id": user['id'],
            "image": "https://images.unsplash.com/photo-1472437774355-71ab6752b434?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1867&q=80"
        },
        {
            "title": "YelpCamp",
            "body": "A large project creating a website for sharing and commenting on campgrounds.  Used NodeJS, Express, and MongoDB.",
            "author_id": user['id'],
            "image": "https://images.unsplash.com/photo-1563299796-17596ed6b017?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2250&q=80",
            "githubURL": "https://github.com/anthonyjacques20/yelpcamp"
        }
    ]

    #Add the data
    for postDict in posts:
        print(postDict)
        post = defaultdict(lambda: None, postDict)
        print(post)
        print(type(post))
        db.execute(
            'INSERT INTO post (title, body, author_id, image, githubURL, moreInfoURL)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (post["title"], post["body"], user['id'], post["image"], post["githubURL"], post["moreInfoURL"])
        )
    #Save the data
    db.commit()

def init_db(seedDB = False):
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    #Only seed the database if requested
    if seedDB:
        seed_db(db)

#Create a command line command and return a messag eto the user
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables"""
    init_db()
    click.echo('Initialized the database!')

def init_app(app):
    #Call the close_db function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    #Add a new command that can be called with the flask command
    app.cli.add_command(init_db_command)