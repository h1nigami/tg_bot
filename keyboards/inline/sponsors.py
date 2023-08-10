from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_sponsors_keyboard(channels):
    keyboard = InlineKeyboardMarkup()
    
    for i, channel in enumerate(channels):
        keyboard.add(InlineKeyboardButton(text=f'{i + 1}', callback_data=f'info:{channel[0]}'))
    
    keyboard.add(InlineKeyboardButton(text=f'Добавить спонсора', callback_data=f'change_link'))
    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'settings'))

    return keyboard

def get_sponsors_delete_keyboard(channel_id):
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(InlineKeyboardButton(text=f'Удалить', callback_data=f'delspons:{channel_id}'))
    keyboard.add(InlineKeyboardButton(text=f'Изменить', callback_data=f'changes:{channel_id}'))
    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'setting_sponsors'))

    return keyboard

def get_sponsors_canced_keyboard():
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text=f'◀️ Вернуться', callback_data=f'setting_sponsors'))

    return keyboard