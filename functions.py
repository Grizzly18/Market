from data import db_session
from data.product import Product


def add_db(data):
    if (data == "К сожалению, мы ничего не смогли найти"):
        return "К сожалению, мы ничего не смогли найти"
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
            url=product[3],
            brand=product[4]
        )
        db_sess.add(Prod)
        db_sess.commit()
        s = db_sess.query(Product).filter(Product.url == product[3]).first()
        new_data.append((product[0], product[1], product[2], product[3], product[4], s.id))
    return new_data


def get_normal_url_for_product(url):
    url = url.split("&")
    product, sort, male, size, price, brand = url[0], None, None, None, None, None
    for i in range(1, len(url)):
        if "sort" in url[i]:
            sort = url[i].split('=')[1]
        if "size" in url[i]:
            size = url[i].split('=')[1]
        if "price" in url[i]:
            price = url[i].split('=')[1]
        if "brand" in url[i]:
            brand = url[i].split('=')[1]
    return (product, sort, male, size, price, brand)


def price_to_int(a):
    return int(a[:-1].replace(" ", ""))


def sort_cards(x):
    return price_to_int(x[1].replace("\xa0", ''))