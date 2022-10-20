from datetime import date

from flask import Flask
from flask_admin.model import typefmt
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager

import cloudinary

cloudinary.config(
    cloud_name="dif0oia5b",
    api_key="386971183136555",
    api_secret="inkWOO7C2gLlFFr8AqGu18ut4xE"
)

app = Flask(__name__)
app.secret_key = '%^&*()GhjkkVBNMFGY#$%^&*)(*&^456789876'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345678@localhost/quanlyhocsinh?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['STUDENT_SIZE'] = 20

app.config['FLASK_ADMIN_SWATCH'] = 'Simplex'
admin = Admin(app=app, name='QUẢN LÝ HỌC SINH', template_mode='bootstrap4')
db = SQLAlchemy(app=app)
babel = Babel(app=app)
login = LoginManager(app=app)


@babel.localeselector
def get_locale():
    return 'vi'


def date_format(view, value):
    return value.strftime('%d/%m/%Y')


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    date: date_format
})
