from aiogram.types import ReplyKeyboardMarkup

from data import config, db

def get_menu_keyboard(user_id, is_admin = False):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('4000 UC', 'Metro royale pass')
    keyboard.add('X-suit collection')

    if user_id == config.owner_id:
        keyboard.add('👨‍💻 Административная панель')

    return keyboard

def get_admin_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add('📊 Статистика', '📣 Рассылка')
    keyboard.add('🔗 Управление')
    keyboard.add('ℹ️ Главное меню')

    return keyboard