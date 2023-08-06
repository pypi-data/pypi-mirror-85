"""
    Routes
    ~~~~~~
Programmer: Phiroj Kumar Dash
Course: CSC540

New functions added for uploading and downloading feature.

"""
from flask import Blueprint
from flask import flash
from flask import Flask
from flask import redirect, send_file, send_from_directory
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor, allowed_file
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect

import os
from wiki import create_app


bp = Blueprint('wiki', __name__)
directory = os.getcwd()
app = create_app(directory)



@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


# It will display the user the file.html page.
@bp.route('/file/')
@protect
def file():
    """
                :param : No input parameter
                :return: Render file.html file

    """

    path = app.config.get('UPLOAD_DIR')
    files = os.listdir(path)

    return render_template('file.html', files=files)


# This function allows users to upload the file from file.html page.
@bp.route('/upload/', methods=['GET', 'POST'])
def upload():
    """
                   :param : No input parameter
                   :return: Render file.html file

       """

    if request.method == 'POST':
        file = request.files['file']

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if not os.path.exists(app.config.get('UPLOAD_DIR')):
            os.makedirs(app.config.get('UPLOAD_DIR'), exist_ok=True)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config.get('UPLOAD_DIR'), file.filename))
            flash('"%s" was saved.' % file.filename)
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')

    path = app.config.get('UPLOAD_DIR')
    files = os.listdir(path)

    return render_template('file.html', files=files)


# This function allows user to download the file from file.html page
@bp.route('/download/', methods=['GET', 'POST'])
def download():
    """
                   :param : No input parameter
                   :return: Download the specific file or Render file.html file

       """
    fileName = request.form['fileName']
    try:
        path = os.path.join(app.config.get('UPLOAD_DIR'), fileName)
        flash('Downloaded file will be found in "Download" directory')
        # return send_file(path, as_attachment=True)
        return send_from_directory(app.config.get('UPLOAD_DIR'), fileName, as_attachment=True)
    except FileNotFoundError:
        flash('File Not found')
        path = app.config.get('UPLOAD_DIR')
        files = os.listdir(path)
        return render_template('file.html', files=files)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
