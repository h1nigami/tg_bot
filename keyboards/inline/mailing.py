from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_mailing_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    
    
    keyboard.add(InlineKeyboardButton(text=f'✅', callback_data=f'mailing_send'))

    return keyboard

def get_send_mailing_menu(buttons, send=False):
    keyboard = InlineKeyboardMarkup()

    for button in buttons:
        but = button.split(' - ')
        keyboard.add(InlineKeyboardButton(text=but[0], url=but[1]))
    
    if send:
        keyboard.add(InlineKeyboardButton(text=f'➕ Кнопка', callback_data=f'add_button'))
        keyboard.add(InlineKeyboardButton(text=f'✅', callback_data=f'mailing_send'))
        keyboard.add(InlineKeyboardButton(text=f'❌', callback_data=f'mailing_canced'))

    return keyboard