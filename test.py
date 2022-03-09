from main import bot, dp  # берем методы и функции из фала майн
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton  # функцию отправки сообщения в телеграм
from aiogram.dispatcher.filters.state import State, StatesGroup
from confing import admin_id  # из конфиг берем номер айди
from aiogram.dispatcher import FSMContext
import requests
from bs4 import BeautifulSoup
from random import randint


async def send_to_admin(dp):  # функция отпрвки сообщения после запуска бота
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


class FSWaitAnswer(StatesGroup):
    what_you_need = State()
    waiting_for_agree = State()


@dp.message_handler(commands=['start'], state=None)  # устанавливаем команды, после них вывод
async def command_start(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["То что нужно", "Это то что ты хочешь"]
    keyboard.add(*buttons)
    await message.answer(text='Привет')  # вывод на команду start
    await message.answer(text='О чем ты мечтаешь?', reply_markup=keyboard)
    await FSWaitAnswer.what_you_need.set()  # устанавливаем состояние


async def get_link_picture(message: Message):
    key_for_picture = message.text  # ключ по которому будет производится поиск
    url = f'https://www.google.ru/search?q={key_for_picture}&newwindow=1&espv=2&source=lnms&tbm=isch&sa=X'
    response = requests.get(url)  # запрос по адресу
    soup = BeautifulSoup(response.text, features="html.parser")  # преобразование файла
    images = []
    for img in soup.findAll('img'):  # проход по результатам выборки по тегам
        images.append(img.get('src'))  # собирает словарь с сылками на картинки
    picture_for_agree = images[randint(1, 15)]
    await message.answer(text=picture_for_agree)


@dp.message_handler(state=FSWaitAnswer.what_you_need)
async def search_picture(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['what_you_need'] = message  # Записывает сообщение в what_you_need
    waiting_for_input = data['what_you_need']  # экземпляр объекта what_you_need
    await get_link_picture(waiting_for_input)  # вызов функции передаем полученое сообщение
    await FSWaitAnswer.next()  # выбираем следущее состояние после того, которое в хандлере
    await message.answer(text='Это то что ты хочешь?')


async def continuation_search(message: Message, state=FSMContext):
    await message.answer(text="здесь будет функция, но пока нет")  # нужно запарсить видео и и абзац по поиску
    await state.finish()


async def again_search(this_input_for_search):
    input_some = this_input_for_search
    await get_link_picture(input_some)


@dp.message_handler(state=FSWaitAnswer.waiting_for_agree)  # выполняется только после await FSWaitAnswer.next()
async def test(message: Message, state: FSMContext):
    if message.text == 'То что нужно':
        await continuation_search(message, state=FSMContext)  # вызываем функцию продолжения поиска(ютуб и абзац)
    else:
        await bot.send_message(chat_id=message.chat.id, text="попробую снова")
        async with state.proxy() as data:  # вытаскиваем переменную
            this_input_for_search = data['what_you_need']  # создаем экземпляр переменной
        await again_search(this_input_for_search)  # вызов функции, передаем экземпляр

# @dp.message_handler()
# async def cmd_start():
#     keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
#     button_1 = KeyboardButton(text='То что нужно')
#     keyboard.add(button_1)
#     button_2 = 'Это не то что я хочу'
#     keyboard.add(button_2)
#     await cmd_start(reply_markup=keyboard)

# @dp.message_handler()
# async def ask_user_agree(message: Message):
#     if message.text in ['yes']
#     await bot.send_message(chat_id=message.from_user.id, text='Это то, чего ты хочешь?')
