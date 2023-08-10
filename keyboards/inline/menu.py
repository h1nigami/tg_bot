from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_sub_menu_keyboard(channels):
    keyboard = InlineKeyboardMarkup()
    for channel in channels:
        keyboard.add(InlineKeyboardButton(text=f'Спонсор', url=channel[1]))
    keyboard.add(InlineKeyboardButton(text=f'✅ Проверить', callback_data=f'check_sub'))

    return keyboard

def get_invite_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton("Пригласить друга", switch_inline_query=f' - Привет! Я реально получил промокод на 1000 UC в этом боте! Переходи скорее! '))

    return keyboard

def get_get_menu_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'ПОЛУЧИТЬ 1000 UC БЕСПЛАТНО ⭐️', callback_data=f'invite'))

    return keyboard

def get_manager_canced_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'settings'))

    return keyboard