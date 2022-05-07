import io
import csv
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium_stealth import stealth
import time


pages_count = 1

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

def open(url):
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
        pages_count = int(soup.find('nav', class_="sf-o-pagination promotions-pagination__pages").find_all('a')[-2].text)
        print(pages_count)
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
                print(pages_count)
            except AttributeError:
                pages_count = 1

            for page in range(1, pages_count + 1):
                driver.get(f"{urls}?p={page}")
                time.sleep(5)

                soup = BeautifulSoup(driver.page_source, 'lxml')

                # offer = soup.find('div', class_='name dotdotdot').text.strip()  # название карточки товара
                cards = soup.find('div', class_="product products__product-card")  # все карточки товара на странице
                print(len(cards))

                cards = soup.find_all('div', class_="product products__product-card")  # все карточки товара на странице
                for card in cards:
                    try:
                        discont = card.find('span', class_="m-badges__text").text.strip()
                    except AttributeError:
                        continue
                    try:
                        productname = card.find('a', class_="sf-link product__link product__name").text.strip()
                    except AttributeError:
                        continue
                    try:
                        specprice = card.find('span', class_="product__special-price").text.strip()
                    except AttributeError:
                        continue
                    try:
                        regprice = card.find('span', class_="product__regular-price").text.strip()
                    except AttributeError:
                        continue
                    try:
                        iurl = card.find('a', class_="sf-link product__link product__name").get('href')
                    except AttributeError:
                        continue
                    print(f'https://eva.ua/ua{iurl}\n{productname}\n{discont}\n{specprice}\{regprice}')







        # with io.open(f'index{page}.html', "w", encoding="utf-8") as file:
        #     file.write(driver.page_source)
        #
        # time.sleep(2)
        # return pages_count





def main():
    print('Введите название раздела')
    open(url = url_stoks[input()])


if __name__ == '__main__':
    main()













from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import token
from newevaparser import eva
import  json
import time


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(massage: types.Message):
    start_buttons = ['Корея', 'Парфумерія', 'Макіяж', 'Обличчя', 'Волосся', 'Дітям', 'Корея']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await massage.answer('Привет, выбери раздел', reply_markup=keyboard)

@dp.message_handler(Text(equals='Корея'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите...')

    # eva()

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("productname"), item.get("url"))}\n'\
            f'{hbold("Скидка: ")}{item.get("discont")}\n' \
            f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n'\
            f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)





if __name__ =='__main__':
    executor.start_polling(dp)