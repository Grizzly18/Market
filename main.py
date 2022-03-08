from flask import Flask, make_response, render_template, redirect
from data import db_session
from requests import *
from flask_login import LoginManager, login_user, logout_user, login_required
from data.users import User
from data.autor import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def main():
    return render_template("main.html", title='Главная страница')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/register")
def register():
    return render_template("register.html", title='Регистрация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/catalog")
def catalog():
    return render_template("catalog.html", title='Каталог')



def main():
    app.run()


if __name__ == '__main__':
    main()