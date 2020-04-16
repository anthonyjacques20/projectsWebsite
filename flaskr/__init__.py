import os

from flask import Flask, render_template, g

def create_app(test_config=None):
    #Create the app
    #instance_relative_config=True tells the app that the configuration files are relative tothe instance folder
    #The instance folder is located outside the flaskr package and can hold local data that shouldn't be committed to version control
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #Load config from the config.py file in the instance folder (when it exists)
        app.config.from_pyfile('config.py', silent=True)
    else:
        #Load the test config if it is passed into the app
        app.config.from_mapping(test_config)

    #Ensure the instance path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Simple route to return
    @app.route('/hello')
    def hello():
	    return render_template('hello.html')

    @app.before_request
    def hook():
        posts = blog.get_posts()
        if 'posts' not in g:
            g.posts = posts
            print("Added posts to g")

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    #The blog blueprint does not have an `url_prefix` because it will be at '/'
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
