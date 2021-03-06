import flask
import random
from flask import Flask, make_response, render_template, redirect, flash, jsonify
from data import db_session
from sqlalchemy import update
from requests import *
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.RequestHistory import History
from data.favorite import Favorite
from data.users import User
from forms.user import RegisterForm
from data.autor import LoginForm
from data.change_profile import ChangeForm
from data.product import Product
from Parser import parser, popular
from functions import add_db, get_normal_url_for_product, price_to_int, sort_cards


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


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


@app.route('/change-profile', methods=['GET', 'POST'])
def change_profile():
    form = ChangeForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user and user.check_password(form.password.data):
            if len(form.email.data) >= 1:
                user.email = form.email.data
            if len(form.newpassword.data) >= 1:
                user.set_password(form.newpassword.data)
            if len(form.about.data) >= 1:
                user.about = form.about.data
            if len(form.address.data) > 1:
                user.address = form.address.data
            db_sess.commit()
            return redirect("/")
        return render_template('change_profile.html', message="Wrong password", form=form)
    return render_template('change_profile.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="???????????? ???? ??????????????????")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='??????????????????????',
                                   form=form,
                                   message="?????????? ???????????????????????? ?????? ????????")
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
    return render_template('register.html', title='??????????????????????', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/catalog")
def catalog():
    return render_template("catalog.html", title='??????????????')


@app.route("/profile")
def profile():
    db_sess = db_session.create_session()
    s = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id).first().FavoriteProducts.split(',')
    data = []
    for prod in s:
        if prod != '':
            temp = db_sess.query(Product).filter(Product.id == prod).first()
            data.append((temp.image, temp.price, temp.info, temp.url, temp.brand, temp.id))
    req = db_sess.query(History).filter(History.user_id == current_user.id).first().History.split(',')
    return render_template("profile.html", title='??????????????', favourite_cards=data, requests_cards=req)


@app.route("/search/q=<product>")
def search_html(product):
    product = get_normal_url_for_product(product)
    try:
        db_sess = db_session.create_session()
        s = db_sess.query(History).filter(History.user_id == current_user.id).first()
        t = product[0]
        if t not in s.History:
            s.History = (s.History + f",{t}").lstrip(',')
            db_sess.commit()
    except Exception:
        pass

    if (product[1] is not None):
        cards = add_db(parser(product=product[0], 
                            sort=product[1], male=product[2], size=product[3], price=product[4], brand=product[5]))
        if product[1] == "price_asc":
            new_cards = sorted(cards, key=sort_cards)
        else:
            new_cards = sorted(cards, key=sort_cards, reverse=True)
        if (product[6] == 'json'):
            json_cards = []
            for card in new_cards:
                json_cards.append({
                    'link': card[3],
                    'price': card[1],
                    'name': card[2],
                    'url_image': card[0],
                    'online store': card[4] 
                })
            return jsonify(json_cards)
        return render_template("product.html", title="???????????????????? ????????????", cards=new_cards)
    else:
        new_cards = add_db(parser(product=product[0], 
                            sort=product[1], male=product[2], size=product[3], price=product[4], brand=product[5]))
        if (product[6] == 'json'):
            json_cards = []
            for card in new_cards:
                json_cards.append({
                    'link': card[3],
                    'price': card[1],
                    'name': card[2],
                    'url_image': card[0],
                    'online store': card[4] 
                })
            return jsonify(json_cards)
        return render_template("product.html", title="???????????????????? ????????????", cards=new_cards)



def main_page():
    cards = add_db(popular()[:5])
    historycards = []
    try:
        db_sess = db_session.create_session()
        s = db_sess.query(History).filter(History.user_id == current_user.id).first().History.split(',')
        if s != ['']:
            rt = random.randint(0, len(s) - 1)
            historycards = add_db(parser(s[rt])[:5])
        if len(historycards) < 5:
            historycards = cards
    except:
        historycards = cards
    return (cards, historycards)


@app.route("/<format>")
def main_page_json(format):
    cards = main_page()
    if (len(format.split('=')) > 1 and format.split('=')[1] == 'json'):
        json_cards = []
        for card in cards[0]:
            json_cards.append({
                'link': card[3],
                'price': card[1],
                'name': card[2],
                'url_image': card[0],
                'online store': card[4] 
            })
        return jsonify(json_cards)
    return render_template("main.html", title='?????????????? ????????????????', cards=cards[0], historycards=cards[1])


@app.route("/")
def main_page_html():
    cards = main_page()
    return render_template("main.html", title='?????????????? ????????????????', cards=cards[0], historycards=cards[1])


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
        # flash('???? ?????????????? ?????????? ?? ??????????????')
        pass
    return render_template("main.html",  title="??????????????????", cards=parser(product="????????????"))


@app.route("/favorite")
def favorite():
    db_sess = db_session.create_session()
    data = []
    try:
        s = db_sess.query(Favorite).filter(Favorite.user_id == current_user.id).first().FavoriteProducts.split(',')
        for prod in s:
            if prod != '':
                temp = db_sess.query(Product).filter(Product.id == prod).first()
                data.append((temp.image, temp.price, temp.info, temp.url, temp.brand, temp.id))
    except Exception:
        pass
    return render_template("favorite.html",  title="??????????????????", cards=data)


@app.route("/popular")
def popular_products():
    return render_template("popular.html", title='????????????????????', cards=add_db(popular(20)))


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
    return render_template("history.html", title='???? ???????????? ????????????????????', cards=historycards)


@app.route("/help")
def help():
    return render_template("help.html", title='????????????', cards=parser(product="????????????")[:5])


def main():
    db_session.global_init("db/main.db")
    app.run()


if __name__ == '__main__':
    main()