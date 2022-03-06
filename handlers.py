from main import bot, dp  # берем методы и функции из фала майн
from aiogram.types import Message  # функцию отправки сообщения в телеграм
from confing import admin_id  # из конфиг берем номер айди
import requests
from bs4 import BeautifulSoup
from random import randint


async def send_to_admin(dp):  # функция отпрвки сообщения после запуска бота
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


@dp.message_handler(commands=['start', 'help'])  # устанавливаем команды, после них вывод
async def command_start(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text='Привет')  # вывод на команду start
    await bot.send_message(chat_id=message.from_user.id, text='О чем ты мечтаешь?')


@dp.message_handler()
async def echo(message: Message):
    key_for_picture = message.text  # ключ по которому будет производится поиск
    url = f'https://www.google.ru/search?q={key_for_picture}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))
    picture_for_agree = images[randint(1, 10)]
    await message.answer(text=picture_for_agree)

# @dp.message_handler()
# async def echo(message: Message):  # функция ответа на строку ввода
#     text = f'Привет, ты написал {message.text}'  # message.text = то что ввели
#     await message.answer(text=text)  # выводит переменную text
#     await bot.send_message(chat_id=message.from_user.id,
#                            text=message.text)  # отвечает, то что мы ввели (message.text) - то что пришло в телеге
