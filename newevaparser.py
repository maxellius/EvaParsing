from bs4 import BeautifulSoup

from selenium import webdriver
from selenium_stealth import stealth
import time
import json

pages_count = 1
result = []


def eva(stoks):
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

    #     url_stoks = {
    #         'Perfumery': 'https://eva.ua/ua/promotion/type/1/',
    #         'Makeup': 'https://eva.ua/ua/promotion/type/2/',
    #         'Disguise': 'https://eva.ua/ua/promotion/type/3/',
    #         'Hair': 'https://eva.ua/ua/promotion/type/4/',
    #         'Children': 'https://eva.ua/ua/promotion/type/5/',
    #         'Korea': 'https://eva.ua/ua/promotion/type/6/',
    #         'Nails': 'https://eva.ua/ua/promotion/type/7/',
    #         'Self_care': 'https://eva.ua/ua/promotion/type/8/',
    #         'Body_and_bath': 'https://eva.ua/ua/promotion/type/9/',
    #         'Household_chemicals': 'https://eva.ua/ua/promotion/type/10/',
    #         'Goods_for_the_home': 'https://eva.ua/ua/promotion/type/12/',
    #         'Clothes_accessories': 'https://eva.ua/ua/promotion/type/13/',
    #         'Dermatocosmetics': 'https://eva.ua/ua/promotion/type/15/',
    #         'Dietary_supplements': 'https://eva.ua/ua/promotion/type/16/',
    #         'Professional_cosmetics': 'https://eva.ua/ua/promotion/type/17/',
    #     }
    driver.get(url)
    time.sleep(5)
    # with io.open(f'index1.html', "w", encoding="utf-8") as file:
    #     file.write(driver.page_source)
    #     time.sleep(2)
    #
    # with open(f"index1.html", "r", encoding='utf-8') as file:
    #     contents = file.read()
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
            try:
                pages_count = int(soup.find('nav', class_="sf-o-pagination promotions-pagination__pages")
                                  .find_all('a')[-2].text)
            except AttributeError:
                pages_count = 1

            for page in range(1, pages_count + 1):
                driver.get(f"{urls}?p={page}")
                time.sleep(5)

                soup = BeautifulSoup(driver.page_source, 'lxml')

                # offer = soup.find('div', class_='name dotdotdot').text.strip()  # название карточки товара
                cards = soup.find('div', class_="product products__product-card")  # все карточки товара на странице

                cards = soup.find_all('div', class_="product products__product-card")  # все карточки товара на странице
                for card in cards:
                    try:
                        item_discont = card.find('span', class_="m-badges__text").text.strip()
                        if item_discont != 'Акція':
                            continue
                        else:
                            pass
                    except AttributeError:
                        continue
                    try:
                        item_productname = card.find('a', class_="sf-link product__link product__name").text.strip()
                    except AttributeError:
                        continue
                    try:
                        item_specprice = card.find('span', class_="product__special-price").text.strip()
                    except AttributeError:
                        continue
                    try:
                        item_regprice = card.find('span', class_="product__regular-price").text.strip()
                    except AttributeError:
                        continue
                    try:
                        item_iurl = card.find('a', class_="sf-link product__link product__name").get('href')
                    except AttributeError:
                        continue

                    result.append(
                        {
                            'discont': item_discont,
                            'productname': item_productname,
                            'specprice': item_specprice,
                            'regprice': item_regprice,
                            'url': f'https://eva.ua{item_iurl}'
                        }
                    )
                    with open('result.json', 'w', encoding='utf-8') as file:
                        json.dump(result, file, indent=4, ensure_ascii=False)

                        # print(f'https://eva.ua/ua{item_iurl}\n{item_productname}\n{item_discont}\n{item_specprice}\{item_regprice}')









        # with io.open(f'index{page}.html', "w", encoding="utf-8") as file:
        #     file.write(driver.page_source)
        #
        # time.sleep(2)
        # return pages_count





def main():
    eva()


if __name__ == '__main__':
    main()
