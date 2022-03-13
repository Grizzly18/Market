import flask
from flask import Flask, make_response, render_template, redirect, flash
from data import db_session
from sqlalchemy import update
from requests import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.RequestHistory import History
from data.favorite import Favorite
from data.users import User
from forms.user import RegisterForm
from data.autor import LoginForm
from data.product import Product
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
        s = db_sess.query(User).filter(User.email == form.email.data).first()
        Fav = Favorite(
            FavoriteProducts="",
            user_id=s.id
        )
        His = History(
            History="",
            user_id=s.id
        )
        db_sess.add(Fav)
        db_sess.add(His)
        db_sess.commit()
        logout_user()
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


@app.route("/profile")
def profile():
    return render_template("profile.html", title='Профиль')


@app.route("/search/q=<product>")
def search(product):
    print(1)
    return render_template("product.html", title=product, cards=add_db(parser(product=product)))


@app.route("/")
def main_page():
    cards = add_db(popular()[:5])
    historycards = []
    try:
        db_sess = db_session.create_session()
        s = db_sess.query(History).filter(History.user_id == current_user.id).first().History.split(',')
        print(s)
        if s != ['']:
            historycards = add_db(parser(s[-1])[:5])
        if len(historycards) < 5:
            historycards = cards
    except:
        historycards = cards
    return render_template("main.html", title='Главная страница', cards=cards, historycards=historycards)


@app.route("/delete-favorite", methods=['GET', 'POST'])
def delete_favorite(): 
    try:
        if (flask.request.method == 'POST'):
            db_sess = db_session.create_session()
            prod_id = flask.request.data.decode()
            s = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id).first()
            t = s.FavoriteProducts.split(',')
            t.remove(prod_id)
            s.FavoriteProducts = (','.join(t)).lstrip(',')
            db_sess.commit()
            return redirect('/favorite')
    except Exception:
        return redirect('/favorite')


@app.route("/add-favorite", methods=['GET', 'POST'])
def add_favorite(): 
    try:
        if (flask.request.method == 'POST'):
            db_sess = db_session.create_session()
            prod_id = flask.request.data.decode()
            s = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id).first()
            if prod_id not in s.FavoriteProducts:
                s.FavoriteProducts = (s.FavoriteProducts + f",{prod_id}").lstrip(',')
                db_sess.commit()
    except Exception:
        # flash('Вы успешно вошли в систему')
        pass
    return render_template("main.html",  title="Избранное", cards=parser(product="рюкзак"))


@app.route("/favorite")
def favorite():
    db_sess = db_session.create_session()
    s = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id).first().FavoriteProducts.split(',')
    data = []
    for prod in s:
        if prod != '':
            temp = db_sess.query(Product).filter(Product.id == prod).first()
            data.append((temp.image, temp.price, temp.info, temp.url, temp.brand, temp.id))
    return render_template("favorite.html",  title="Избранное", cards=data)


@app.route("/popular")
def popular_products():
    return render_template("popular.html", title='Популярное', cards=add_db(popular(20)))


@app.route("/history")
def history():
    historycards = []
    try:
        db_sess = db_session.create_session()
        s = db_sess.query(History).filter(History.user_id == current_user.id).first().History.split(',')
        if s != ['']:
            historycards = add_db(parser(s[-1]))
        if len(historycards) < 5:
            historycards = add_db(popular(20))
    except:
        historycards = add_db(popular(20))
    return render_template("history.html", title='На основе просмотров', cards=historycards)


@app.route("/help")
def help():
    return render_template("help.html", title='Помощь', cards=parser(product="рюкзак")[:5])


def main():
    db_session.global_init("db/main.db")
    app.run()


if __name__ == '__main__':
    main()