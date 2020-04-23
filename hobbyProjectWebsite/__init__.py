import os

from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy


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

    #Simple route to return
    @app.route('/hello')
    def hello():
	    return render_template('hello.html')

    @app.route('/helloWorld')
    def helloWorld():
        return "Hello World!"

    #About route
    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.before_request
    def hook():
        posts = blog.get_posts()
        if 'posts' not in g:
            g.posts = posts
            print("Added posts to g")

    from . import auth
    app.register_blueprint(auth.bp)

    #The blog blueprint does not have an `url_prefix` because it will be at '/'
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    #Initialize the SQLAlchemy app
    from hobbyProjectWebsite.db import db
    db.init_app(app)

    return app