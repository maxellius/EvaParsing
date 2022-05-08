import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium_stealth import stealth
import pyautogui
from selenium.webdriver.common.keys import Keys
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

# options.add_argument("--headless")

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
result = []
driver.get('https://eva.ua/ua/promotion/men-6-26/?p=1')
time.sleep(5)
# pyautogui.scroll(-3500)
driver.find_element_by_tag_name('body').send_keys(Keys.END)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'lxml')
# offer = soup.find('div', class_='name dotdotdot').text.strip()  # название карточки товара
cards = soup.find_all('div', class_="product products__product-card")  # все карточки товара на странице

for card in cards:
    try:
        if card.find('span', class_="m-badges__text").text.strip() is not None and card. \
                find('span', class_="m-badges__text").text.strip() != "Акція!":
            try:
                item_discont = card.find('span', class_="m-badges__text").text.strip()
            except AttributeError:
                continue
            try:
                item_productname = card.find('a',
                                             class_="sf-link product__link product__name").text.strip()
            except AttributeError:
                continue
            try:
                item_specprice = card.find('span', class_="product__special-price").text.replace('\xa0',
                                                                                                 '').strip()
            except AttributeError:
                continue
            try:
                item_regprice = card.find('span', class_="product__regular-price").text.replace('\xa0',
                                                                                                '').strip()
            except AttributeError:
                continue
            try:
                item_iurl = card.find('a', class_="sf-link product__link product__name").get('href')
            except AttributeError:
                continue
            try:
                item_img_url = card.find('div', class_="product__image-wrapper").find('div', class_="sf-image product__image product__image--show")
                    # .find('img').get('src')
            except AttributeError:
                continue
            # print(f'https://eva.ua/ua{item_iurl}\n{item_productname}{item_discont}\n{item_specprice}\{item_regprice}\n{item_img_url}')
            print(item_img_url)

        #     result.append(
        #         {
        #             'discont': item_discont,
        #             'productname': item_productname,
        #             'specprice': item_specprice,
        #             'regprice': item_regprice,
        #             'url': f'https://eva.ua{item_iurl}',
        #             'img': item_img_url
        #         }
        #     )
        #
        # with open('result.json', 'w', encoding='utf-8') as file:
        #     json.dump(result, file, indent=4, ensure_ascii=False)
    except AttributeError:
        continue





