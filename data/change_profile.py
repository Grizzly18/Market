from tkinter import PhotoImage
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields import EmailField


class ChangeForm(FlaskForm):
    email = EmailField('Новая почта')
    about = TextAreaField('Обо мне')
    address = StringField('Адрес')
    newpassword = PasswordField('Новый пароль')
    password = PasswordField('Старый Пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')