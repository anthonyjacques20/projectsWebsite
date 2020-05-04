import os

from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from hobbyProjectWebsite.auth import loginManager


def create_app(test_config=None):
    #Create the app
    #instance_relative_config=True tells the app that the configuration files are relative to the instance folder
    #The instance folder is located outside the hobbyProjectWebsite package and can hold local data that shouldn't be committed to version control
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("Hobby Project Website app.instance_path: " + app.instance_path)

    if test_config is None:
        app.config.from_object(os.environ['APP_SETTINGS'])
        
        #Load config from the config.py file in the instance folder (when it exists)
        #app.config.from_pyfile('config.py', silent=True)
    else:
        print(test_config)
        #Load the test config if it is passed into the app
        app.config.from_mapping(test_config)

    @app.route('/')
    def landing():
        return render_template('landing.html')
    app.add_url_rule('/', endpoint='landing')

    #About route
    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.before_request
    def hook():
        projects = project.get_projects()
        if 'projects' not in g:
            g.projects = projects
            print("Added projects to g")

    from . import auth
    app.register_blueprint(auth.bp)

    #The project blueprint does not have an `url_prefix` because it will be at '/'
    from . import project
    app.register_blueprint(project.bp)
    app.add_url_rule('/projects/', endpoint='index')

    from . import comment
    app.register_blueprint(comment.bp)

    #Initialize the SQLAlchemy app
    from hobbyProjectWebsite.db import db
    db.init_app(app)

    #Initialize Flask-Login
    loginManager.init_app(app)
    #Tell Flask-Login which function ('login') to use when trying to login
    loginManager.login_view = 'auth.login'
    loginManager.login_message_category = "info"

    return app