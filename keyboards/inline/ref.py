from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_ref_setting_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(text=f'✅ Создать', callback_data=f'create_referal'))
    keyboard.add(InlineKeyboardButton(text=f'🔗 Посмотреть', callback_data=f'show_referal'))
    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'settings'))

    return keyboard

def ref_return_keyboard(name = ''):
    keyboard = InlineKeyboardMarkup()
    
    if name:
        keyboard.add(InlineKeyboardButton(text=f'⚙️ Изменить', callback_data=f'change_ref:{name}'))
        keyboard.add(InlineKeyboardButton(text=f'❌ Удалить', callback_data=f'delete_referal:{name}'))
    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'seting_referals'))

    return keyboard

def get_delete_ref_keyboard(name):
    keyboard = InlineKeyboardMarkup()
    
    if name:
        keyboard.add(InlineKeyboardButton(text=f'✅', callback_data=f'ref_d:{name}'))
        keyboard.add(InlineKeyboardButton(text=f'❌', callback_data=f'ref_nd'))

    return keyboard