import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from hobbyProjectWebsite.auth import login_required
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import Project, User, Comment

bp = Blueprint('comment', __name__, url_prefix="/<int:id>")

@bp.route('/create', methods=('GET','POST'))
@login_required
def create(id):
    if request.method == 'POST':
        #Grab text from the form
        text = request.form['text']
        #Grab the id from the url_prefix
        project_id = id
        author_id = g.user['id']
        error = None

        if not text:
            error = 'Comment text is required.'
        
        if error is not None:
            flash(error, 'error')
        else:
            comment = Comment(
                text = text,
                project_id = project_id,
                author_id = author_id,
                created = datetime.now()
            )
            #Add and commit the comment
            db.session.add(comment)
            db.session.commit()
            flash("Successfully created comment", 'info')

        #Redirect to the show page with parameters
        return redirect(url_for('project.show', id=id))
    else:
        return "You are in the create comment page for id: " + str(id)


def get_comments(projectID):
    #Join the users table and replace the user id with the username from the users table
    comments = Comment.query.join(User, Comment.author_id==User.id).add_columns(Comment.text, Comment.created, User.username).filter(Comment.project_id==projectID).order_by(Comment.created).all()
    print(comments)
    return comments