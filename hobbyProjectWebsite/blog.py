from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from hobbyProjectWebsite.auth import login_required
from hobbyProjectWebsite.db import get_db

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
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, image, githubURL, moreInfoURL)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (title, body, g.user['id'], image, githubURL, moreInfoURL)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

def get_posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, image, githubURL, moreInfoURL, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return posts

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, image, githubURL, moreInfoURL, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)

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
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, image = ?, githubURL = ?, moreInfoURL = ?'
                ' WHERE id = ?',
                (title, body, image, githubURL, moreInfoURL, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/edit.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))