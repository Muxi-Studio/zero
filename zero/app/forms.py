# coding: utf-8

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.fields import TextAreaField
from wtforms.fields import SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    email = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField('Login')


class UploadForm(Form):
    filename = TextAreaField(validators=[Required()])
    url = TextAreaField()
    submit = SubmitField('Upload')
