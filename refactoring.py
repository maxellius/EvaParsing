import io
import csv
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium_stealth import stealth
import time


def last_page():
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

    link = 1

    driver.get(f"https://eva.ua/ua/promotion/?p={link}")

    time.sleep(5)
    with io.open(f'index1.html', "w", encoding="utf-8") as file:
        file.write(driver.page_source)
        time.sleep(2)

    with open(f"index1.html", "r", encoding='utf-8') as file:
        contents = file.read()

    soup = BeautifulSoup(contents, 'lxml')
    pages_count = int(soup.find('nav', class_="sf-o-pagination promotions-pagination__pages").find_all('a')[-2].text)

    for page in range(2, pages_count + 1):
        driver.get(f"https://eva.ua/ua/promotion/?p={page}")
        time.sleep(5)

        with io.open(f'index{page}.html', "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        time.sleep(2)

    for page in range(1, pages_count + 1):
        with open(f"index{page}.html", "r", encoding='utf-8') as file:
            contents = file.read()

        soup = BeautifulSoup(contents, 'lxml')

        # offer = soup.find('div', class_='name dotdotdot').text.strip()  # название карточки товара
        cards = soup.find_all('div', class_="promotion-tile promotions__item")  # все карточки товара на странице

        for card in cards:
            promotion_list = card.find('div', class_="promotion-tile__image-wrap").find('a')
            info_block = card.find('div', class_="info-block")
            # рабочие
            links = promotion_list.get('href').strip()
            urls = [f'https://eva.ua{links}']



            # name = promotion_list.find('source').get('alt')
            # не рабочие
            # days = info_block.find('span', class_="days_bl").text.strip().replace('\n', ' ')
            # hours = info_block.find('span', class_="hour_bl").text.strip()
            # minutes = info_block.find('span', class_="min_bl").text.strip()

            # timer = f'{name}\n{url}\n{days} {hours} годин {minutes} хвилин\n'
            # timer = f'https://eva.ua{url}'

            # with io.open('database.csv', 'a', encoding="utf-8") as file:
            #     writer = csv.writer(file, delimiter='.')
            #     writer.writerow(
            #         {timer}
            #     )
            for url in urls:
                driver.get(url)
                time.sleep(5)
                with open('itemsours.html', 'w', encoding='utf-8') as file:
                    file.write(driver.page_source)
                with open('itemsours.html', 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file.read(), 'lxml')
                    items_image = soup.find_all('div', class_="product products__product-card")
                    for image in items_image:
                        img = image.find('div', class_="product__image-wrapper")\
                            .find('div', class_="sf-image product__image product__image--show").find('img').get('src')
                        nameitems = image.find('div', class_="product__image-wrapper")\
                            .find('div',class_="sf-image product__image product__image--show").find(
                            'img').get('alt')
                        discont = image.find('a', class_="sf-link product__link")\
                            .find('span', class_="m-badges__text").text.strip()
                        specprice = image.find('div', class_="product__details-info")\
                            .find('div', class_="product__price-box")\
                            .find('span', class_="product__special-price").text.strip()
                        regprice = image.find('div', class_="product__details-info")\
                            .find('div',class_="product__price-box").find(
                            'span', class_="product__regular-price").text.strip()
                        itemurl = image.find('div', class_="product__details-info").find('a').get('href')

                        itemlist = f'{nameitems}' \
                                   f' {specprice}/{regprice}' \
                                   f' {discont} ' \
                                   f'{itemurl}'


                        with io.open('itemlist.json', 'w', encoding='utf-8') as f:
                            f.write(itemlist)

                        print(img)
                        print(discont)
                        print(specprice)
                        print(regprice)
                        print(nameitems)






    # with open('database.csv', 'r', encoding='utf-8') as file:
    #     contents = file.readlines()
    #     for get in contents:
    #         driver.get(get)
    #
    #     soup = BeautifulSoup(driver.page_source, 'lxml')
    #     items_image = soup.find_all('div', class_="product products__product-card")
    #     for image in items_image:
    #         img = image.find('div', class_="product__image-wrapper").find('div',
    #                                                                       class_="sf-image product__image product__image--show").find(
    #             class_="noscript").get('src')
    #         nameitems = image.find('div', class_="product__image-wrapper").find('div',
    #                                                                             class_="sf-image product__image product__image--show").find(
    #             class_="noscript").get('alt')
    #         discount = image.find('a', class_="sf-link product__link").find('div',
    #                                                                         class_="sf-badge m-badges__item m-badges__item--discount").find(
    #             'span', class_="m-badges__text").text.strip()
    #         specprice = image.find('div', class_="product__details-info").find('div', class_="product__price-box").find(
    #             'span', class_="product__special-price").text.strip()
    #         regprice = image.find('div', class_="product__details-info").find('div', class_="product__price-box").find(
    #             'span', class_="product__regular-price").text.strip()
    #
    #         print(img)
    #         print(discount)
    #         print(specprice)
    #         print(regprice)
    #         print(nameitems)
















# def find_items_url():
#     with open('database.csv', 'r', encoding="utf-8") as file:
#         for line in file.readlines():
#             if 'http' in line:
#                 with open('itemsurl.json', 'a', encoding='utf-8') as urlfile:
#                     urlfile.write(line)

last_page()

# def find_items(soup, retry=5):
#     with io.open('itemsurl.json', 'r', encoding='utf-8') as file:
#         url = file.readlines()
#         for item in url:
#             driver.get(item)
#             time.sleep(5)
#             try:
#                 cards = soup.find('div', class_="product")
#                 print(f'+ {cards}')
#                 print(cards)
#                 print(len(cards))
#             except Exception as ex:
#                 if retry:
#                     print(f'[INFO] retry={retry} + item')
#                     return find_items(soup=soup, retry=(retry - 1))
#                 else:
#                     raise
#             for card in cards:
#                 discont = card.find('div', class_="product-label product-label--position-1 product-label--color-1") \
#                     .text
#                 productname = card.find('a', class_="product__link product__name").text
#                 specprice = card.find('span', class_="product__special-price").text
#                 regprice = card.find('span', class_="product__regular-price").text
#                 itemurl = card.find('a', class_="product__link product__name").get('href')
#
#                 itemlist = f'{productname} {specprice}/{regprice} {discont} {itemurl}'
#
#                 with io.open('itemlist.json', 'w', encoding='utf-8') as f:
#                     f.write(itemlist)














    # def delete_file_html(self, pages_count):
    #     for page in range(1, pages_count):
    #         os.remove(f'index{page}.html')
    #     os.remove('itemsurl.json')

















# def main():
    # pages_count, soup = last_page()
    # collect_cards(pages_count=pages_count, soup=soup)
    # find_items_url()
    # # find_items(soup=soup)











# if __name__ == '__main__':
#     main()


