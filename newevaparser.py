from bs4 import BeautifulSoup
import pyautogui
from selenium import webdriver
from selenium_stealth import stealth
import time
import json
import pyautogui
from selenium.webdriver.common.keys import Keys
pages_count = 1
result = []


def eva(stoks = 'Чоловікам'):
    url_stoks = {
        'Парфумерія': 'https://eva.ua/ua/promotion/type/1/',
        'Макіяж': 'https://eva.ua/ua/promotion/type/2/',
        'Обличчя': 'https://eva.ua/ua/promotion/type/3/',
        'Волосся': 'https://eva.ua/ua/promotion/type/4/',
        'Дітям': 'https://eva.ua/ua/promotion/type/5/',
        'Корея': 'https://eva.ua/ua/promotion/type/6/',
        'Нігті': 'https://eva.ua/ua/promotion/type/7/',
        'Догляд за собою': 'https://eva.ua/ua/promotion/type/8/',
        'Тіло та ванна': 'https://eva.ua/ua/promotion/type/9/',
        'Побутова хімія': 'https://eva.ua/ua/promotion/type/10/',
        'Чоловікам': 'https://eva.ua/ua/promotion/type/11/',
        'Товари для дому': 'https://eva.ua/ua/promotion/type/12/',
        'Одяг, аксесуари': 'https://eva.ua/ua/promotion/type/13/',
        'Dermatocosmetics': 'https://eva.ua/ua/promotion/type/15/',
        'БАДи (харчові добавки)': 'https://eva.ua/ua/promotion/type/16/',
        'Professional_cosmetics': 'https://eva.ua/ua/promotion/type/17/',
    }
    print('Введите раздел')
    url = url_stoks[stoks]
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

    
    driver.get(url)
    time.sleep(5)
   
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        pages_count = int(
            soup.find('nav', class_="sf-o-pagination promotions-pagination__pages").find_all('a')[-2].text)
    except AttributeError:
        pages_count = 1

    for page in range(1, pages_count + 1):
        driver.get(f"{url}?p={page}")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        # offer = soup.find('div', class_='name dotdotdot').text.strip()  # название карточки товара
        cards = soup.find_all('div', class_="promotion-tile promotions__item")  # все карточки товара на странице

        for card in cards:
            promotion_list = card.find('div', class_="promotion-tile__image-wrap").find('a')
            info_block = card.find('div', class_="info-block")
            # рабочие
            links = promotion_list.get('href').strip()
            urls = f'https://eva.ua{links}'
            driver.get(urls)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            try:
                pages_count = int(soup.find('nav', class_="sf-o-pagination products__pagination").find_all('a')[-2].text)
            except AttributeError:
                pages_count = 1

            for page in range(1, pages_count + 1):
                driver.get(f"{urls}?p={page}")
                time.sleep(5)
                # pyautogui.scroll(-3500)
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(1)


                soup = BeautifulSoup(driver.page_source, 'lxml')

                # offer = soup.find('div', class_='name dotdotdot').text.strip()  # название карточки товара


                cards = soup.find_all('div', class_="product products__product-card")  # все карточки товара на странице
                for card in cards:
                    try:
                        if card.find('span', class_="m-badges__text").text.strip() is not None and card.\
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
                                item_img_url = card.find('div', class_="sf-image product__image product__image--show") \
                                    .find('img').get('src')
                            except AttributeError:
                                continue
                            # print(f'https://eva.ua/ua{item_iurl}\n{item_productname}{item_discont}\n{item_specprice}\{item_regprice}')

                            result.append(
                                {
                                    'discont': item_discont,
                                    'productname': item_productname,
                                    'specprice': item_specprice,
                                    'regprice': item_regprice,
                                    'url': f'https://eva.ua{item_iurl}',
                                    'img': item_img_url
                                }
                            )

                        with open('result.json', 'w', encoding='utf-8') as file:
                            json.dump(result, file, indent=4, ensure_ascii=False)
                    except AttributeError:
                        continue




def main():
    eva()


if __name__ == '__main__':
    main()
