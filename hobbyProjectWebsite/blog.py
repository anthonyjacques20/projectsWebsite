from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from werkzeug.exceptions import abort

from hobbyProjectWebsite.auth import login_required
from hobbyProjectWebsite.models import db, Project, User

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = get_posts()
    return render_template('blog/index.html', posts=posts, page="home")

@bp.route('/<int:id>')
def show(id):
    post = get_post(id, check_author=False)
    return render_template('blog/show.html', post=post)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        image = request.form['image']
        githubURL = request.form['githubURL']
        moreInfoURL = request.form['moreInfoURL']
        error = None
        
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            project = Project(
                author_id = g.user['id'],
                created = datetime.now(),
                title = title,
                body = body,
                image = image,
                githubURL = githubURL,
                moreInfoURL = moreInfoURL
            )
            db.session.add(project)
            db.session.commit()

            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

def get_posts():
    projects = Project.query.all()
    return projects

def get_post(id, check_author=True):
    #Another example of how to perform a join using SQLAlechemy rather than raw SQL
    #project = db.session.query(Project, User).join(User, Project.author_id == User.id).first()
    project = db.engine.execute(
        'SELECT p.id, p.title, p.body, p.image, p.githubURL, p.moreinfoURL, p.created, p.author_id, u.username'
        ' FROM projects p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ' + str(id)
    ).first()
    columns = ['id', 'title', 'body', 'image', 'githuburl', 'moreinfourl', 'created', 'author_id', 'username']
    #Convert to a dictionary
    project = {columns[i]: project[columns[i]] for i in range(0,len(project)) }
    print("Project dictionary: ", project)

    if project is None:
        abort(404, "Project id {0} doesn't exist.".format(id))

    if check_author and project['author_id'] != g.user['id']:
        abort(403)

    return project


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    project = get_post(id)

    if request.method == 'POST':
        project['title'] = request.form['title']
        project['body'] = request.form['body']
        project['image'] = request.form['image']
        project['githuburl'] = request.form['githubURL']
        project['moreinfourl'] = request.form['moreInfoURL']
        error = None

        if not project['title']:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            #Delete the username from project as it is not in the Project model
            del project["username"]
            #Update the project with the new information
            db.session.query(Project).\
                filter(Project.id == id).\
                update(project)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/edit.html', project=project)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))