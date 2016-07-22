# coding: utf-8
import requests
from . import app
from flask import render_template, session, redirect, g, url_for, request
from .forms import LoginForm, UploadForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email == app.config['QINIU_EMAIL'] and \
           password == app.config['QINIU_PASS']:
            session['login'] = True
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    if session.get('login'):
        session['login'] = False
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


def login_required(f):
    def decorator(*args, **kwargs):
        with app.test_request_context():
            if session.get('login'):
                f(*args, **kwargs)
            else:
                return '<h1>Forbidden</h1>'


@login_required
@app.route('/')
def index():
    if session.get('login'):
        r = requests.get(app.config['BANNER_API'])
        banner_json = r.json()
        return render_template('index.html',
            banner_json=banner_json)
    else:
        return '<h1>Forbidden</h1>'


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@login_required
@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = form.filename.data
            file.url = form.url.data
            sendFile = {"upload_file": file}
            requests.post(app.config['BANNER_API'] + '%s' % 'save/',
                          headers={'Content-Type': 'multipart/form-data'},
                          files=sendFile)
            return redirect(url_for('index'))
    return render_template('upload.html', form=form)
