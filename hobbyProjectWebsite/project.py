from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from werkzeug.exceptions import abort

from hobbyProjectWebsite.auth import login_required, adminRequired
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.comment import get_comments
from hobbyProjectWebsite.models import Project, User, Comment
from flask_login import current_user
import json

bp = Blueprint('project', __name__,url_prefix="/projects")

@bp.route('/')
def index():
    projects = get_projects()
    for project in projects:
        maxCharacters = 200
        if len(project['body']) > maxCharacters:
            project['body'] = project['body'][:maxCharacters] + '...'
    return render_template('project/index.html', projects=projects, page="projects")

@bp.route('/<int:id>')
def show(id):
    project = get_project(id, check_author=False)
    comments = get_comments(id)
    return render_template('project/show.html', project = project, comments = comments)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
@adminRequired
def create():
    if request.method == 'POST':        
        title = request.form['title']
        body = request.form['body']
        image = request.form['image']
        githuburl = request.form['githuburl']
        moreinfourl = request.form['moreinfourl']
        #Support image is a list of strings
        #This will take all of the extra keys for 'supportImages'
        #And make a list for 'supportImages"
        supportImages = json.dumps(request.form.to_dict(flat=False)['supportimages'])
        if supportImages is None:
            supportImages = ''
        error = None
        
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error, 'error')
        else:
            project = Project(
                author_id = current_user.id,
                created = datetime.now(),
                title = title,
                body = body,
                image = image,
                githuburl = githuburl,
                moreinfourl = moreinfourl,
                supportimages = supportImages
            )
            db.session.add(project)
            db.session.commit()
            flash("Successfully created project named: " + title, "success")
            return redirect(url_for('project.index'))
    
    return render_template('project/create.html')

def get_projects():
    projects = db.engine.execute(
        'SELECT p.id, p.title, p.body, p.image, p.githubURL, p.moreinfoURL, p.created, p.author_id, u.username'
        ' FROM projects p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    columns = ['id', 'title', 'body', 'image', 'githuburl', 'moreinfourl', 'created', 'author_id', 'username']
    #Convert to a dictionary
    projects = [{columns[i]: project[columns[i]] for i in range(0,len(project)) } for project in projects]
    #projects = Project.query.all()
    return projects

def get_project(id, check_author=True):
    #Another example of how to perform a join using SQLAlechemy rather than raw SQL
    #project = db.session.query(Project, User).join(User, Project.author_id == User.id).first()
    project = db.engine.execute(
        'SELECT p.id, p.title, p.body, p.image, p.githubURL, p.moreinfoURL, p.created, p.author_id, u.username, p.supportimages'
        ' FROM projects p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ' + str(id)
    ).first()

    if project is None:
        abort(404, "Project id {0} doesn't exist.".format(id))

    if check_author and project['author_id'] != current_user.id:
        abort(403)

    columns = ['id', 'title', 'body', 'image', 'githuburl', 'moreinfourl', 'created', 'author_id', 'username', 'supportimages']
    #Convert to a dictionary
    project = {columns[i]: project[columns[i]] for i in range(0,len(project)) }
    if project['supportimages'] is not None:
        project['supportimages'] = json.loads(project['supportimages'])

    return project


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
@adminRequired
def edit(id):
    project = get_project(id)

    if request.method == 'POST':
        project['title'] = request.form['title']
        project['body'] = request.form['body']
        project['image'] = request.form['image']
        project['githuburl'] = request.form['githuburl']
        project['moreinfourl'] = request.form['moreinfourl']
        project['supportimages'] = json.dumps(request.form.to_dict(flat=False)['supportimages'])

        error = None

        if not project['title']:
            error = 'Title is required.'

        if error is not None:
            flash(error, 'error')
        else:
            #Delete the username from project as it is not in the Project model
            del project["username"]
            #Update the project with the new information
            db.session.query(Project).\
                filter(Project.id == id).\
                update(project)
            db.session.commit()
            flash("Successfully updated project named: " + project['title'], "success")
            return redirect(url_for('project.index'))

    return render_template('project/edit.html', project=project)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@adminRequired
def delete(id):
    get_project(id)
    #Delete comments for that project
    db.engine.execute('DELETE FROM comments where project_id = ' + str(id))
    #Delete the project
    db.engine.execute('DELETE FROM projects WHERE id = ' + str(id))
    return redirect(url_for('project.index'))