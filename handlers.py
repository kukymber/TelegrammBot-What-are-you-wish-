from main import bot, dp  # берем методы и функции из фала майн
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton  # функцию отправки сообщения в телеграм
from aiogram.dispatcher.filters.state import State, StatesGroup
from confing import admin_id  # из конфиг берем номер айди
import requests
from bs4 import BeautifulSoup
from random import randint


async def send_to_admin(dp):  # функция отпрвки сообщения после запуска бота
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


# class wait_answer(StatesGroup):
#     waiting_for_agree = State()
#     # waiting_for_food_size = State()


@dp.message_handler(commands=['start'])  # устанавливаем команды, после них вывод
async def command_start(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text='Привет')  # вывод на команду start
    await bot.send_message(chat_id=message.from_user.id, text='О чем ты мечтаешь?')
    echo(message)

def echo(message: Message):
    key_for_picture = message.text  # ключ по которому будет производится поиск
    url = f'https://www.google.ru/search?q={key_for_picture}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'
    response = requests.get(url)  # запрос по адресу
    soup = BeautifulSoup(response.text, features="html.parser")  # преобразование файла
    images = []
    for img in soup.findAll('img'):  # проход по результатам выборки по тегам
        images.append(img.get('src'))  # собирает словарь с сылками на картинки
    picture_for_agree = images[randint(1, 10)]
    await bot.send_message(text=picture_for_agree)


@dp.message_handler()
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup()
    button_1 = KeyboardButton(text="То что нужно")
    keyboard.add(button_1)
    button_2 = "Это не то что я хочу"
    keyboard.add(button_2)
    await message.answer("Это то что ты хочешь?", reply_markup=keyboard)


@dp.message_handler(lambda message: Message == "То что нужно")
async def continuation_search(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="здесь будет функция, но пока нет")  # нужно запарсить видео и и абзац по поиску


@dp.message_handler(lambda message: Message == "Это не то что я хочу")
async def again_search(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="попробую снова")
    echo(message)

# @dp.message_handler()
# async def ask_user_agree(message: Message):
#     if message.text in ['yes']
#     await bot.send_message(chat_id=message.from_user.id, text='Это то, чего ты хочешь?')


# @dp.message_handler()
# async def echo(message: Message):  # функция ответа на строку ввода
#     text = f'Привет, ты написал {message.text}'  # message.text = то что ввели
#     await message.answer(text=text)  # выводит переменную text
#     await bot.send_message(chat_id=message.from_user.id,
#                            text=message.text)  # отвечает, то что мы ввели (message.text) - то что пришло в телеге
