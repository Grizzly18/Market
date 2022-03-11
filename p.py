import requests
from bs4 import BeautifulSoup as BS
import urllib.request
import random
import urllib3
import time
import re


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75'
}


# список прокси-серверов
proxies = {
  'http': 'http://203.34.28.71:80',
  'https': 'http://195.174.34.57:10001',
}


def load_img_from_web(link_web, link_img):
    resource = urllib.request.urlopen(link_web)
    out = open(link_img, 'wb')
    out.write(resource.read())
    out.close()


def sneakerhead(product):
    link = f"https://sneakerhead.ru/search/?q={product}"
    response = requests.get(link, headers=HEADERS)
    soup = BS(response.content, "lxml")
    result = []
    print(soup)
    for el in soup.select(".product-cards__item"):
        try:
            result.append((el.select("source")[0]['srcset'], el.select(".product-card__price-value")[0].text, 
                        el.select(".product-card__link")[0].text, 
                        "https://street-beat.ru/" + el.select("product-card__link")[0]['href']))
        except Exception:
            pass
    return result


def lamoda(product, sort=None, male=None):
    link = f"https://www.lamoda.ru//catalogsearch/result/?q={product}"
    if (male is not None):
        link += f"&gender_section={male}&multigender_page=1"
    if (sort is not None): # discount - скидка;  price_desc - по убыванию цен; price_asc - по возрастанию цен
        link += f"&sort={sort}"
    response = requests.get(link)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".x-product-card__card"):
        try:
            result.append((el.select("img")[0]['src'], el.select("span")[0].text, 
                        el.select(".x-product-card-description__brand-name")[0].text + " " + el.select(".x-product-card-description__product-name")[0].text, 
                        "https://www.lamoda.ru" + el.select("a")[0]['href']))
        except Exception:
            pass
    return result


# ПРОБЛЕМА
def street_beat(product):
    link = f"https://street-beat.ru/cat/?q={product}"
    response = requests.get(link, headers=HEADERS)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".product-container__standard"):
        try:
            result.append((el.select("img")[0]['src'], el.select("span")[0].text, 
                        el.select(".product-card__info")[0].text, 
                        "https://street-beat.ru/" + el.select("a")[0]['href']))
        except Exception:
            pass
    return result


def superstep(product):
    link = f"https://superstep.ru/catalog/?q={product}"
    response = requests.get(link, headers=HEADERS)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".product-item"):
        try:
            result.append(("https://superstep.ru" + el.select(".product-item-image")[0]['src'], el.select("span")[0].text, 
                           el.select(".product-name")[0].text.strip(),
                           "https://superstep.ru" + el.select(".product-image-wrapper a")[0]['href']))
        except Exception:
            pass
    return result


def asos(product): # НА АНГЛИЙСКОМ
    link = f"https://www.asos.com/en/search/?q={product}"
    response = requests.get(link, headers=HEADERS)
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select("._3TqU78D"):
        # Далеко не все фотки прогружаются
        try:
            result.append((el.select("img")[0]['src'], el.select("span ._16nzq18")[0].text, 
                        el.select("h2")[0].text, 
                        el['href']))
        except Exception:
            pass
    return result


def parser(product):
    return lamoda(product)