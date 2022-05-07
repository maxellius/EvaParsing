from selenium import webdriver
from selenium_stealth import stealth
import time
from bs4 import BeautifulSoup
import json

token = '5375193903:AAHiM-tJeyo79-lkrSnSuuj9oIF7aseI_g0'

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_argument("--headless")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r"C:\chromedriver.exe")

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://eva.ua/ua/promotion/amigo-amiga-29-03/"
driver.get(url)
time.sleep(5)
with open('itemsours.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
with open('itemsours.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
        items_image = soup.find_all('div', class_="product products__product-card")
        for image in items_image:
                img = image.find('div', class_="product__image-wrapper").find('div', class_="sf-image product__image product__image--show").find(class_="noscript").get('src')
                nameitems = image.find('div', class_="product__image-wrapper").find('div', class_="sf-image product__image product__image--show").find(class_="noscript").get('alt')
                discount = image.find('a', class_="sf-link product__link").find('div', class_="sf-badge m-badges__item m-badges__item--discount").find('span', class_="m-badges__text").text.strip()
                specprice = image.find('div', class_="product__details-info").find('div', class_="product__price-box").find('span', class_="product__special-price").text.strip()
                regprice = image.find('div', class_="product__details-info").find('div', class_="product__price-box").find('span', class_="product__regular-price").text.strip()

                print(img)
                print(discount)
                print(specprice)
                print(regprice)
                print(nameitems)
        # print(soup.prettify())
        # print(soup.get_text())
        # for link in soup.find_all('div',class_="product products__product-card"):
        #         print(link.get_text())

# print(soup.prettify())

# cards = soup.find('div', class_="product__visible-part")
# print(cards)
# print(len(cards))
# for card in cards:
# img = soup.find('div', class_="product__visible-part").find('div', class_="product__image-wrapper").find('div', class_="sf-image product__image product__image--show")
#         # .find(class_='noscript').get('src')
# print(img)
# driver.quit()