# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import InputRequired, Email, DataRequired


class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[DataRequired()], render_kw={'autofocus': True})
    password = PasswordField(u'Password', validators=[DataRequired()])


class MarkCheck(FlaskForm):
    student_id = StringField(u'ID Học sinh', validators=[DataRequired()])
    subject_id = StringField(u'Mã môn', validators=[DataRequired()])
    semester_id = StringField(u'Mã học kì', validators=[DataRequired()])
