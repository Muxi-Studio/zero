# coding: utf-8

from flask_wtf import Form
from wtforms.fields import StringField, PasswordField
from wtforms.fields import TextAreaField
from wtforms.fields import SubmitField, SelectField
from wtforms.validators import Required


class LoginForm(Form):
    email = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField('Login')


class UploadForm(Form):
    filetypes = ['1.Banner', '2.Calendar']
    filename = TextAreaField(validators=[Required()])
    url = TextAreaField()
    types = SelectField('ImageType', choices=[(f, f) for f in filetypes],
                        validators=[Required()])
    submit = SubmitField('Upload')
