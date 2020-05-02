import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flask_login import login_required, login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import Project, User, Comment
from flask_login import LoginManager, current_user, login_user

bp = Blueprint('auth', __name__, url_prefix="/auth")

loginManager = LoginManager()

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
            #Must call db.commit() to save the changese made in the insert above
            db.session.commit()
            flash("Successfully registered user: " + username, "success")
            return redirect(url_for('auth.login'))

        flash(error, 'error')

    return render_template('auth/register.html', page="register")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    #Redirect user to index page if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = getUser(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            login_user(user)
            flash("Successfully logged in as " + username, "info")
            nextPage = request.args.get('next')
            #Make sure the URL is not null and that the URL is on our current domain
            #We don't want someone to modify the next request parameter to send the user to a different site
            #As this causes security concerns...
            if not nextPage or url_parse(nextPage).netlog != '':
                return redirect(url_for('index'))
            return redirect(nextPage)

        flash(error, 'warning')

    return render_template('auth/login.html', page="login")

@bp.route('/logout')
def logout():
    logout_user()
    #Flash the logout message
    flash("Successfully logged out!", 'info')
    return redirect(url_for('index'))

#Create a function to return the user
def getUser(username):
    return User.query.filter(User.username == username).first()
    
#Create a function to return the user by id
def getUserByID(id):
    return User.query.filter(User.id == id).first()

#This tells flask-login how to get the user login information
@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))