from data import db_session
from data.product import Product


def add_db(data):
    db_sess = db_session.create_session()
    new_data = []
    for product in data:
        s = db_sess.query(Product).filter(Product.url == product[3]).first()
        if s:
            new_data.append((product[0], product[1], product[2], product[3], product[4], s.id))
            continue
        Prod = Product(
            image=product[0],
            price=product[1],
            info=product[2],
            url=product[3]
        )
        db_sess.add(Prod)
        db_sess.commit()
        s = db_sess.query(Product).filter(Product.url == product[3]).first()
        new_data.append((product[0], product[1], product[2], product[3], product[4], s.id))
    return new_data