import asyncio
from aiogram import Bot, Dispatcher, executor  # Bot - class, despetcher - develery, executor start bot work
from confing import bot_token  # import data from another fail
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# loop = asyncio.get_event_loop()   # для работы с acsyncio получаем поток данных
bot = Bot(bot_token, parse_mode='HTML')  # передали в класс бот его хэш
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == '__main__':
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)
                                # скип = пропускает сообщения, когда бот не рабоатет




