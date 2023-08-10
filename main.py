from aiogram import executor
from handlers import dp

from data import db

async def on_sturtup(dp):
    await db.create_tables()
    print('Бот запущен!')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_sturtup)