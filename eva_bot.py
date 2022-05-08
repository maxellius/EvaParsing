from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import token
from newevaparser import eva
import json
import time


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(massage: types.Message):
    start_buttons = ['Корея', 'Чоловікам', 'Макіяж', 'Обличчя', 'Волосся', 'Дітям']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await massage.answer('Привет, выбери раздел', reply_markup=keyboard)

@dp.message_handler(Text(equals='Корея'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите...')

    eva('Корея')

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{item.get("img")}\n' \
               f'{"_______________"}\n' \
               f'{hlink(item.get("productname"), item.get("url"))}\n' \
               f'{hbold("Скидка: ")}{item.get("discont")}\n' \
               f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n' \
               f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)


@dp.message_handler(Text(equals='Чоловікам'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите... Собираю информацию.')

    eva('Чоловікам')

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{item.get("img")}\n' \
               f'{"_______________"}\n' \
               f'{hlink(item.get("productname"), item.get("url"))}\n' \
               f'{hbold("Скидка: ")}{item.get("discont")}\n' \
               f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n' \
               f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)


@dp.message_handler(Text(equals='Макіяж'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите...')

    eva('Макіяж')

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{item.get("img")}\n' \
               f'{"_______________"}\n' \
               f'{hlink(item.get("productname"), item.get("url"))}\n' \
               f'{hbold("Скидка: ")}{item.get("discont")}\n' \
               f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n' \
               f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)


@dp.message_handler(Text(equals='Обличчя'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите...')

    eva('Обличчя')

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{item.get("img")}\n' \
               f'{"_______________"}\n' \
               f'{hlink(item.get("productname"), item.get("url"))}\n' \
               f'{hbold("Скидка: ")}{item.get("discont")}\n' \
               f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n' \
               f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)



@dp.message_handler(Text(equals='Волосся'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите...')

    eva('Волосся')

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{item.get("img")}\n' \
               f'{"_______________"}\n' \
               f'{hlink(item.get("productname"), item.get("url"))}\n' \
               f'{hbold("Скидка: ")}{item.get("discont")}\n' \
               f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n' \
               f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)



@dp.message_handler(Text(equals='Дітям'))
async def Korea(message: types.Message):
    await message.answer('Пожалуйста подождите...')

    eva('Дітям')

    with open('result.json', encoding='utf-8') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{item.get("img")}\n' \
               f'{"_______________"}\n' \
               f'{hlink(item.get("productname"), item.get("url"))}\n' \
               f'{hbold("Скидка: ")}{item.get("discont")}\n' \
               f'{hbold("Цена со скидкой: ")}{item.get("specprice")}\n' \
               f'{hbold("Цена без скидки: ")}{item.get("regprice")}'

        if index%20 == 0:
            time.sleep(3)

        await message.answer(card)

if __name__ =='__main__':
    executor.start_polling(dp)