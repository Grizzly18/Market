import requests
from bs4 import BeautifulSoup as BS
import urllib.request


def load_img_from_web(link_web, link_img):
    resource = urllib.request.urlopen(link_web)
    out = open(link_img, 'wb')
    out.write(resource.read())
    out.close()


def lamoda(product):
    response = requests.get(f"https://www.lamoda.ru/catalogsearch/result/?q={product}")
    soup = BS(response.content, "lxml")
    result = []
    for el in soup.select(".x-product-card__card"):
        # Далеко не все фотки прогружаются
        try:
            result.append((el.select("img")[0]['src'], el.select("span")[0].text, 
                        el.select(".x-product-card-description__brand-name")[0].text, 
                        el.select(".x-product-card-description__product-name")[0].text, ))
        except Exception:
            pass
    return result


product = str(input())

for i in lamoda(product):
    print(i)
