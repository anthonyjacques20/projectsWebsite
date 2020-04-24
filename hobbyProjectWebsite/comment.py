import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

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

        if not text:
            error = 'Comment text is required.'
        
        if error is not None:
            flash(error)
        else:
            Comment(
                text = text,
                project_id = project_id,
                author_id = author_id
            )

        #Redirect to the show page with parameters
        return redirect(url_for('project.show', id=id))
    else:
        return "You are in the create comment page for id: " + str(id)