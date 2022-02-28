from main import bot, dp  # берем методы и функции из фала майн

from aiogram.types import Message  # функцию отправки сообщения в телеграм
from confing import admin_id  # из конфиг берем номер айди


async def send_to_admin(dp):  # функция отпрвки сообщения после запуска бота
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


@dp.message_handler()
async def echo(message: Message):   # функция ответа на строку ввода
    text = f'Привет, ты написал {message.text}'     # message.text = то что ввели
    await bot.send_message(chat_id=message.from_user.id,
                           text=text)   # отвечает, то что мы ввели
    await message.answer(text=text)