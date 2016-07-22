# coding: utf-8

import os
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key is here'
app.config['QINIU_EMAIL'] = os.getenv('QINIU_EMAIL')
app.config['QINIU_PASS'] = os.getenv('QINIU_PASS')
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['BANNER_API'] = 'http://127.0.0.1:5000/api/banner/'


from . import views, forms
