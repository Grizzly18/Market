import requests
from translate import Translator
from bs4 import BeautifulSoup as BS
import urllib.request
import random
from datetime import datetime

translator = Translator(from_lang="russian",to_lang="english")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
}


def load_img_from_web(link_web, link_img):
    resource = urllib.request.urlopen(link_web)
    out = open(link_img, 'wb')
    out.write(resource.read())
    out.close()


def sneakerhead(product):
    link = f"https://sneakerhead.ru/search/?q={product}"
    response = requests.get(link, headers=HEADERS, timeout=1)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".product-cards__item"):
        try:
            result.append(("https://sneakerhead.ru" + el.select("img")[1]['src'], el.select(".product-card__price-value")[0].text.strip(), 
                        el.select(".product-card__link")[0].text.strip(), 
                        "https://sneakerhead.ru" + el.select(".product-card__link")[0]['href'],
                        "sneakerhead"))
        except Exception:
            pass
    return result


def lamoda(product, sort=None, male=None, size=None, price=None): # &page=2
    link = f"https://www.lamoda.ru//catalogsearch/result/?q={product}"
    if (male is not None):
        link += f"&gender_section={male}&multigender_page=1"
    if (sort is not None): # discount - скидка;  price_desc - по убыванию цен; price_asc - по возрастанию цен
        link += f"&sort={sort}"
    if (size is not None):
        link += f"&size_values={size}"
    if (price is not None):
        link += f"&price={price}" #21360,112840
    response = requests.get(link, timeout=1)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".x-product-card__card"):
        try:
            result.append((el.select("img")[0]['src'], el.select("span")[0].text, 
                        el.select(".x-product-card-description__brand-name")[0].text + " " + el.select(".x-product-card-description__product-name")[0].text, 
                        "https://www.lamoda.ru" + el.select("a")[0]['href'],
                        "lamoda"))
        except Exception:
            pass
    return result


# ПРОБЛЕМА
# def street_beat(product):
#     link = f"https://street-beat.ru/cat/?q={product}"
#     response = requests.get(link, headers=HEADERS)
#     soup = BS(response.content, "lxml")
#     result = []
#     for el in soup.select(".product-container__standard"):
#         try:
#             result.append((el.select("img")[0]['src'], el.select("span")[0].text, 
#                         el.select(".product-card__info")[0].text, 
#                         "https://street-beat.ru/" + el.select("a")[0]['href']))
#         except Exception:
#             pass
#     return result


def superstep(product):
    link = f"https://superstep.ru/catalog/?q={product}"
    response = requests.get(link, headers=HEADERS, timeout=1)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".product-item"):
        try:
            result.append(("https://superstep.ru" + el.select(".product-item-image")[0]['src'], el.select("span")[0].text.strip(), 
                           el.select(".product-name")[0].text.strip(),
                           "https://superstep.ru" + el.select(".product-image-wrapper a")[0]['href'],
                            "superstep"))
        except Exception:
            pass
    return result


def asos(product): # НА АНГЛИЙСКОМ
    product = translator.translate(product)
    link = f"https://www.asos.com/en/search/?q={product}"
    response = requests.get(link, headers=HEADERS, timeout=1)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select("._3TqU78D"):
        # Далеко не все фотки прогружаются
        try:
            result.append((el.select("img")[0]['src'], el.select("span ._16nzq18")[0].text, 
                        el.select("h2")[0].text, 
                        el['href'], "asos"))
        except Exception:
            pass
    return result


def popular(count=5):
    prods = ["Верхнаяя одежда", "Спортивная одежда", "Обувь", "Футболки и майки", "Платье", "Водолазки", "Брюки", "Толстовки и свитшоты", 
             "Пиджаки", "Костюмы", "Аксессуары", "Шорты", "Рубашки", "Платья", "Nike", "Adidas", "Polo", "Юбки"]
    p = []
    req = []
    while (len(p) < count):
        res = random.randint(1, 2)
        prod = random.randint(0, len(prods) - 1)
        if (res, prod, ) in req:
            continue
        req.append((res, prod,))
        try:
            if res == 1:
                p += lamoda(prods[random.randint(0, len(prods) - 1)])
            if res == 2:
                p += sneakerhead(prods[random.randint(0, len(prods) - 1)])
            if res == 3:
                p += superstep(prods[random.randint(0, len(prods) - 1)])
            if res == 4:
                p += sneakerhead(prods[random.randint(0, len(prods) - 1)])
        except Exception:
            pass
    return p


def parser(product, count=20, sort=None, male=None, size=None, price=None, brand=None):
    if (brand is not None):
        product += f" {brand}"
    time = datetime.now()
    p =  []
    while (len(p) < count):
        if ((datetime.now() - time).seconds > 8):
            return "К сожалению, мы ничего не смогли найти"
        res = random.randint(1, 2)
        try:
            if res == 1:
                p += lamoda(product, sort=sort, male=male, size=size, price=price)
            if res == 2:
                p += sneakerhead(product)
            if res == 3:
                p += superstep(product)
            if res == 4:
                p += asos(product)
        except Exception:
            pass
    return p