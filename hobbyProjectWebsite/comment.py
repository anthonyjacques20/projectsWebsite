import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from hobbyProjectWebsite.auth import login_required
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import Project, User, Comment

bp = Blueprint('comment', __name__, url_prefix="/<int:id>/comments")

@bp.route('/', methods=['POST'])
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

@bp.route('/<int:commentID>/edit', methods=('GET','POST'))
@login_required
def edit(id, commentID):
    comment = getComment(commentID)

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
            comment = Comment.query.filter_by(id=commentID).first()
            comment.text = text
            #Commit the edited comment
            db.session.commit()
            flash("Successfully edited comment", 'info')

        #Redirect to the show page with parameters
        return redirect(url_for('project.show', id=id))
    else:
        if comment is None:
            abort(404, "Comment id {0} doesn't exist.".format(commentID))

        return render_template('comment/edit.html', projectID = id, comment = comment)

def getComment(commentID):
    #Join the users table and replace the user id with the username from the users table
    comment = Comment.query.join(User, Comment.author_id==User.id).add_columns(Comment.id, Comment.text, Comment.created, User.username, Comment.author_id).filter(Comment.id==commentID).first()
    if comment:
        columns = ['id', 'text', 'created', 'username', 'author_id']
        #Abort if someone other than the author tries to edit a comment
        if getattr(comment, 'author_id') != g.user['id']:
            abort(403)
        #Return the dictionary
        return {columns[i]: getattr(comment, columns[i]) for i in range(0,len(columns)) }

    return comment

def get_comments(projectID):
    #Join the users table and replace the user id with the username from the users table
    comments = Comment.query.join(User, Comment.author_id==User.id).add_columns(Comment.text, Comment.created, User.username, Comment.id).filter(Comment.project_id==projectID).order_by(Comment.created).all()
    print(comments)
    return comments