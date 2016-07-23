# coding: utf-8

import os
import redis
from flask import Flask
from flask_qiniustorage import Qiniu


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key is here'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['BANNER_API'] = 'http://123.56.41.13:5000/api/banner/'
app.config['CALENDAR_API'] = 'http://123.56.41.13:5000/api/calendar/'
# qiniu config
app.config['QINIU_EMAIL'] = os.getenv('QINIU_EMAIL')
app.config['QINIU_PASS'] = os.getenv('QINIU_PASS')
app.config['QINIU_ACCESS_KEY'] = os.getenv('QINIU_ACCESS_KEY')
app.config['QINIU_SECRET_KEY'] = os.getenv('QINIU_SECRET_KEY')
app.config['QINIU_BUCKET_NAME'] = 'ccnustatic'
app.config['QINIU_BUCKET_DOMAIN'] = 'oao7x1n3m.bkt.clouddn.com'


qiniu = Qiniu(app)
rds = redis.StrictRedis(host='localhost', port=6384, db=0)


from . import views, forms
