from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import bot

from data import config, db
from keyboards.inline import get_sub_menu_keyboard

reply_messages_ids = []

class IsAdminMessage(BoundFilter):
    async def check(self, message: types.Message):
        global reply_messages_ids

        user = await db.get_user(message.from_user.id)
        if user:
            return str(message.from_user.id) == config.owner_id or user[1]
        
        if not (message.message_id) in reply_messages_ids:
            await message.answer('Бот обновился, введите /start')
            reply_messages_ids.append(message.message_id)
        return False

class IsAdminCallBack(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        global reply_messages_ids

        user = await db.get_user(call.from_user.id)
        if user:
            return str(call.from_user.id) == config.owner_id or user[1]
        
        if not (call.message.message_id) in reply_messages_ids:
            await call.message.answer('Бот обновился, введите /start')
            reply_messages_ids.append(call.message.message_id)
        return False

class IsUserMessage(BoundFilter):
    async def check(self, message: types.Message):
        global reply_messages_ids

        user = await db.get_user(message.from_user.id)
        if not user:
            if not (message.message_id) in reply_messages_ids:
                await message.answer('Бот обновился, введите /start')
                reply_messages_ids.append(message.message_id)
            return False

        sponsors = await db.get_all_sponsors()
        if sponsors:
            for sponsor in sponsors:
                if sponsor[0] == 0:
                    continue
                
                user_channel_status = await bot.get_chat_member(chat_id=sponsor[0], user_id=message.from_user.id)
                if user_channel_status["status"] == 'left':
                    if not (message.message_id) in reply_messages_ids:
                        await message.answer('❗️ Для начала работы c ботом необходимо подписаться на канал.', reply_markup=get_sub_menu_keyboard(sponsors))
                        reply_messages_ids.append(message.message_id)
                    return False
            return True
        else:
            if not (message.message_id) in reply_messages_ids:
                await message.answer('Добавьте спонсоров в админке!')
                reply_messages_ids.append(message.message_id)
            return False