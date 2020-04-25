import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import Project, User, Comment

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif getUser(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user = User(
                username = username,
                password = generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            #Must call db.commit() to save the changese made in the insert above
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', page="register")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = getUser(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            #Session is a dict that stores data across requests
            #When validation succeeds, the user's id is stored in a new session.
            #Data is stored in a cookie that is sent to the browser and the browser sends it back
            #With sub-sequent requests.  Flask signs the data so it can't be tampererd
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', page="login")

#This registers a function to run before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = getUserByID(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Create a function to return the user
def getUser(username):
    user = User.query.filter(User.username == username).first()
    if user:
        columns = ['id', 'username', 'password']
        #Return the dictionary
        return {columns[i]: getattr(user, columns[i]) for i in range(0,len(user)) }
    else:
        return None
    
#Create a function to return the user by id
def getUserByID(id):
    user = User.query.filter(User.id == id).first()
    if user:
        columns = ['id', 'username', 'password']
        #Return the dictionary
        return {columns[i]: getattr(user, columns[i]) for i in range(0,len(user)) }
    else:
        return None
    
#This function checks to see if the user is logged in
#If a user is logged in, then it continues to the view
#If the user is NOT logged in, the it redirects to the login page
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view (**kwargs)
    return wrapped_view