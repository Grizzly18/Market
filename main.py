import flask
from flask import Flask, make_response, render_template, redirect
from data import db_session
from requests import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from forms.user import RegisterForm
from data.autor import LoginForm
from Parser import parser, popular
from functions import add_db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


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
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)




@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            # about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/catalog")
def catalog():
    return render_template("catalog.html", title='Каталог')


@app.route("/search/q=<string:product>")
def search(product):
    return render_template("product.html", title=product, cards=parser(product="рюкзак"))


@app.route("/")
def main_page():
    return render_template("main.html", title='Главная страница', cards=add_db(popular()[:5]))


@app.route("/add-favorite", methods=['GET', 'POST'])
def add_favorite():
    if (flask.request.method == 'POST'):
        print(flask.request.data.decode())
        print(1)
    return render_template("main.html",  title="Избранное", cards=parser(product="рюкзак"))


@app.route("/favorite")
def favorite():
    return render_template("favorite.html",  title="Избранное", cards=parser(product="рюкзак"))


@app.route("/help")
def help():
    return render_template("help.html", title='Помощь', cards=parser(product="рюкзак")[:5])


def main():
    db_session.global_init("db/main.db")
    app.run()


if __name__ == '__main__':
    main()