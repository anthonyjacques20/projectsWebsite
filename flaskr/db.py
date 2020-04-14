import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #This tells theconnection to return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db= g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#Create a command line command and return a messag eto the user
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables"""
    init_db()
    click.echo('Initialized the database!')

def init_app(app):
    #Call the close_db function when cleaning upa fter returning the response
    app.teardown_appcontext(close_db)
    #Add a new command that can be called with the flask command
    app.cli.add_command(init_db_command)