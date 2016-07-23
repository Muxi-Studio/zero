# coding: utf-8
import requests
from . import app, qiniu, rds
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
            if session.get('login') == True:
                f(*args, **kwargs)
            else:
                return redirect(url_for('login'))


# banners = [] --> redis queue.
# rds.set('banners', [])
# rds.save()


@app.route('/')
def index():
    if session.get('login'):
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/banner/')
def banner():
    if session.get('login'):
        r = requests.get(app.config['BANNER_API'])
        try:
            banner_json = r.json()
        except ValueError as e:
            banner_json = []
        return render_template('resource.html', banner_json=banner_json)
    else:
        return redirect(url_for('login'))


@app.route('/calendar/')
def calendar():
    if session.get('login'):
        r = requests.get(app.config['CALENDAR_API'])
        try:
            banner_json = r.json()
        except ValueError as e:
            banner_json = []
        return render_template('resource.html', banner_json=banner_json)
    else:
        return redirect(url_for('login'))


def allowed_file(filename, upload_filename):
    filename_list = []
    file_list = eval(rds.get('banners')) or [] + \
                eval(rds.get('calendar')) or []
    for file_dict in file_list:
        filename_list += file_dict.keys()
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'] and \
            upload_filename not in filename_list


@app.route('/upload/', methods=['GET'])
def upload():
    if session.get('login'):
        return render_template('upload.html')
    else:
        return redirect(url_for('login'))


@app.route('/banner_upload/', methods=['POST', 'GET'])
def banner_upload():
    if session.get('login'):
        form = UploadForm()
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename, form.filename.data):
                # 七牛文件上传
                url = form.url.data
                filename = form.filename.data
                qiniu.save(file, filename)
                if not rds.get('banners'):
                    rds.set('banners', [])
                banners = eval(rds.get('banners'))
                banners.append({filename: url})
                rds.set('banners', banners)
                rds.save()
                return redirect(url_for('banner'))
        return render_template('upload_resource.html', form=form,
                                name='Banner')
    else:
        return redirect(url_for('login'))


@app.route('/calendar_upload/', methods=['POST', 'GET'])
def calendar_upload():
    if session.get('login'):
        form = UploadForm()
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename, form.filename.data):
                # 七牛文件上传
                url = form.url.data
                filename = form.filename.data
                qiniu.save(file, filename)
                if not rds.get('calendars'):
                    rds.set('calendars', [])
                calendars = eval(rds.get('calendars'))
                calendars.append({filename: url})
                rds.set('calendars', calendars)
                rds.save()
                return redirect(url_for('calendar'))
        return render_template('upload_resource.html', form=form,
                                name='Calendar')
    else:
        return redirect(url_for('login'))


@app.route('/delete/')
def delete():
    if session.get('login'):
        # from request args get filename
        filename = request.args.get('filename')
        qiniu.delete(filename)
        banners = eval(rds.get('banners')) 
        for i, banner in enumerate(banners):
            if banner.keys()[0] == filename:
                del banners[i]
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
