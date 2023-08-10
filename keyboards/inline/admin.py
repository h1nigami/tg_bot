from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_set_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    
    keyboard.add(InlineKeyboardButton(text=f'✅', callback_data=f'add_admin'), InlineKeyboardButton(text=f'❌', callback_data=f'delete_admin'))
    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'settings'))

    return keyboard

def get_admin_canced_setting_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'seting_admins'))

    return keyboard

def get_admin_setting_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(text=f'🔥 Управление спонсорами', callback_data=f'setting_sponsors'))
    keyboard.add(InlineKeyboardButton(text=f'👨‍💻 Управление администраторами', callback_data=f'seting_admins'))
    keyboard.add(InlineKeyboardButton(text=f'🔗 Управление ссылками', callback_data=f'seting_referals'))
    keyboard.add(InlineKeyboardButton(text=f'🧑‍💻 Управление менеджером', callback_data=f'manager'))

    return keyboard