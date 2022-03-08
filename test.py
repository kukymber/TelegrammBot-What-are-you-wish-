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
    await message.answer(text='Привет')  # вывод на команду start
    await message.answer(text='О чем ты мечтаешь?')
    await FSWaitAnswer.what_you_need.set()  # устанавливаем состояние


async def echo(message: Message):
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
        data['what_you_need'] = message  # не точно(Записывает сообщение в what_you_need)
    # await FSWaitAnswer.next()  # не точно ( то же самое что и через прокси)
    waiting_for_input = data['what_you_need']  # !!!
    await echo(waiting_for_input)
    # await state.finish()
    await FSWaitAnswer.next()  # если отключить, то всегда перехватывает сообщения
    await message.answer(text='Это то что ты хочешь?')
    # await FSWaitAnswer.waiting_for_agree.set()  # добавить иф на обработку двух вариантов


async def continuation_search(message: Message, state=FSMContext):
    await message.answer(text="здесь будет функция, но пока нет")  # нужно запарсить видео и и абзац по поиску
    await state.finish()


async def again_search(this_input_for_search):
    input_some = this_input_for_search
    await echo(input_some)


@dp.message_handler(state=FSWaitAnswer.waiting_for_agree)
async def test(message: Message, state: FSMContext):
    if message.text == 'То что нужно':
        await continuation_search(message, state=FSMContext)
    else:
        # async with state.proxy() as data:
        #     this_input_for_search = data['what_you_need']
        await bot.send_message(chat_id=message.chat.id, text="попробую снова")
        async with state.proxy() as data:
            this_input_for_search = data['what_you_need']
        await again_search(this_input_for_search)


@dp.message_handler()
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton(text='То что нужно')
    keyboard.add(button_1)
    button_2 = 'Это не то что я хочу'
    keyboard.add(button_2)
    # await message.answer(reply_markup=keyboard)

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
