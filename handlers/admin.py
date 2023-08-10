from loader import dp, bot
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types

from keyboards.inline import get_sponsors_keyboard, get_sponsors_delete_keyboard, get_sponsors_canced_keyboard, get_send_mailing_menu, get_manager_canced_keyboard, get_admin_setting_menu_keyboard, get_admin_canced_setting_keyboard, get_admin_set_menu_keyboard, get_ref_setting_menu_keyboard, ref_return_keyboard, get_delete_ref_keyboard
from keyboards.default import get_admin_menu_keyboard

from filters import IsAdminCallBack, IsAdminMessage
from data import db, config
from states import StorageChangeLink,StorageChangeNewLink, StorageMailing, StorageEditManager, StorageAddAdmin, StorageDeleteAdmin, StorageChangeReferal, StorageCreateReferal, StorageShowReferal

@dp.message_handler(IsAdminMessage(), commands=['admin'], state='*')
@dp.message_handler(IsAdminMessage(), text='👨‍💻 Административная панель', state='*')
async def admin_start(message: types.Message, state:FSMContext):
    await state.finish()

    await message.answer('Админ панель', reply_markup=get_admin_menu_keyboard())

# Управление
@dp.message_handler(IsAdminMessage(), text='🔗 Управление', state='*')
@dp.callback_query_handler(IsAdminCallBack(), text='settings', state='*')
async def settings(message: types.Message, state:FSMContext):
    await state.finish()

    if type(message) == types.Message:
        await message.answer('Управление', reply_markup=get_admin_setting_menu_keyboard())
    else:
        await message.message.delete()
        await message.message.answer('Управление', reply_markup=get_admin_setting_menu_keyboard())

# Управление спонсорами
@dp.callback_query_handler(IsAdminCallBack(), text='setting_sponsors', state='*')
async def set_sponsors(call: types.CallbackQuery, state: FSMContext):
    sponsors = await db.get_all_sponsors()
    await call.answer('DONE')
    await call.message.delete()
    await call.message.answer('Список спонсоров:', reply_markup=get_sponsors_keyboard(sponsors))

@dp.callback_query_handler(IsAdminCallBack(), text_startswith='info:')
async def set_sponsors(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    sponsor = call.data.split(':')[1]
    s = await db.get_sponsor(sponsor)

    await call.message.answer(
        f'🔒 ID Telegram : {sponsor}\n\n'
        f'🔗 Ссылка: {s[1]}', reply_markup=get_sponsors_delete_keyboard(sponsor)
    )

# Добавление спонсора
@dp.callback_query_handler(IsAdminCallBack(), text='change_link')
async def change_link(call: types.CallbackQuery, state: FSMContext):
    await call.answer('DONE')

    await StorageChangeLink.value.set()
    await call.message.answer('Введите ID группы')

@dp.message_handler(IsAdminMessage(),state=StorageChangeLink.value)
async def change_link_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    await StorageChangeLink.next()
    await message.answer('Введите ссылку на группу')

@dp.message_handler(IsAdminMessage(), state=StorageChangeLink.link)
async def change_link_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await db.create_sponsor(data['id'], message.text)
        except:
            await state.finish()
            return await message.answer('Не добавлено!', reply_markup=get_sponsors_canced_keyboard())

    await state.finish()
    await message.answer('Добавлено!', reply_markup=get_sponsors_canced_keyboard())

# Удаление спонсора
@dp.callback_query_handler(IsAdminCallBack(), text_startswith='delspons:')
async def delete_link_del(call: types.CallbackQuery, state: FSMContext):
    await db.delete_sponsor(call.data.split(':')[1])
    await call.message.answer('Удалено!', reply_markup=get_sponsors_canced_keyboard())

# Изменение спонсора
@dp.callback_query_handler(IsAdminCallBack(), text_startswith='changes:')
async def delete_link_del(call: types.CallbackQuery, state: FSMContext):
    await StorageChangeNewLink.value.set()
    async with state.proxy() as data:
        data['sponsor'] = call.data.split(':')[1]
    await call.message.answer('Введите новый ID группы')

@dp.message_handler(IsAdminMessage(),state=StorageChangeNewLink.value)
async def change_link_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    await StorageChangeNewLink.next()
    await message.answer('Введите ссылку на группу')

@dp.message_handler(IsAdminMessage(), state=StorageChangeNewLink.link)
async def change_link_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await db.edit_sponsor(data['sponsor'], data['id'], message.text)

    await state.finish()
    await message.answer('Изменено!', reply_markup=get_sponsors_canced_keyboard())

# FAQ
@dp.message_handler(IsAdminMessage(), text='📊 Статистика')
async def faq(message: types.Message, state: FSMContext):
    await state.finish()

    users = await db.get_all_users()
    active_users = await db.get_all_active_users()
    await message.answer(f'''👥 Всего пользователей: {len(users)}
👥 Активных пользователей: {len(active_users)}''')
    

# Рассылка
@dp.message_handler(IsAdminMessage(), text='📣 Рассылка')
async def mailing(message: types.Message, state:FSMContext):
    await StorageMailing.value.set()
    await message.answer('📣 Отправьте в этот чат материал для рассылки:')

    async with state.proxy() as data:
        data['text'] = ''
        data['photo'] = ''
        data['buttons'] = []

@dp.message_handler(IsAdminMessage(), state=StorageMailing.value) # Добавление текста
async def mailing_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

        if 'mes' in data:
            await data['mes'].delete()
    
        if data['photo']:
            data['mes'] = await message.answer_photo(data['photo'], data['text'], reply_markup=get_send_mailing_menu(data['buttons'], send=True))
        else:
            data['mes'] = await message.answer(data['text'], reply_markup=get_send_mailing_menu(data['buttons'], send=True))

@dp.message_handler(IsAdminMessage(), state=StorageMailing.value, content_types=[types.ContentType.PHOTO]) # Добавление фото
async def mailing_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        if message.caption:
            data['text'] = message.caption
        
        if 'mes' in data:
            await data['mes'].delete()
        
        if data['photo']:
            data['mes'] = await message.answer_photo(data['photo'], data['text'], reply_markup=get_send_mailing_menu(data['buttons'], send=True))
        else:
            data['mes'] = await message.answer(data['text'], reply_markup=get_send_mailing_menu(data['buttons'], send=True))

@dp.callback_query_handler(IsAdminCallBack(), text='add_button', state=StorageMailing.value) # Добавление кнопки
async def mailing_button(call: types.CallbackQuery, state: FSMContext):
    await call.answer('DONE')
    
    await StorageMailing.button.set()
    await call.message.answer('Введите: название кнопки - ссылка')

@dp.message_handler(IsAdminMessage(), state=StorageMailing.button)
async def mailing_button_set(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.text.split(' - ')) == 2:
            data['buttons'].append(message.text)
        else:
            return await message.answer(
                'Введите: название кнопки - ссылка\n\n'
                'Что бы создать кнопку по новой нажмите "Кнопка"'
            )
        
        if 'mes' in data:
            await data['mes'].delete()
        
        if data['photo']:
            data['mes'] = await message.answer_photo(photo=data['photo'], caption=data['text'], reply_markup=get_send_mailing_menu(data['buttons'], send=True))
        else:
            data['mes'] = await message.answer(data['text'], reply_markup=get_send_mailing_menu(data['buttons'], send=True))
    await StorageMailing.value.set() 
    

@dp.callback_query_handler(IsAdminCallBack(), text='mailing_send', state=StorageMailing.value) # Отправка рассылки
async def mailing_send(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Рассылка начата')
    
    users = await db.get_all_users()
    async with state.proxy() as data:
        photo = data['photo']
        text = data['text']

    await state.finish()

    
    for user in users:
        try:
            if photo:
                await bot.send_photo(user[0], photo, text, reply_markup=get_send_mailing_menu(data['buttons']))
            else:
                await bot.send_message(user[0], text, reply_markup=get_send_mailing_menu(data['buttons']))
        except:
            pass
    
    await call.message.answer(f'Рассылка окончена\nПользователей получивих рассылку: {len(users)}')


    

@dp.callback_query_handler(IsAdminCallBack(), text='mailing_canced', state='*') # Отмена рассылки
async def mailing_canced(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено!')

    await state.finish()

# Менеджер
@dp.callback_query_handler(IsAdminCallBack(), text='manager', state='*')
async def manager(call: types.CallbackQuery, state:FSMContext):
    await call.message.delete()
    await call.answer('DONE')
    await StorageEditManager.value.set()
    await call.message.answer('📣 Отправьте в этот чат никнейм менеджера без @:', reply_markup=get_manager_canced_keyboard())

@dp.message_handler(IsAdminMessage(), state=StorageEditManager.value)
async def manager_set(message: types.Message, state: FSMContext):
    await state.finish()
    config.set_manager(message.text)
    await message.answer('Установлено', reply_markup=get_manager_canced_keyboard())

# Управление администраторами
@dp.callback_query_handler(IsAdminCallBack(), text='seting_admins')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    admins = await db.get_all_admins()
    text = '🧑‍💻 Список адмнов:\n\n'
    for i, admin in enumerate(admins):
        text += f'{i + 1}. {admin[2]} - ID <code>{admin[0]}</code>\n'
    await call.message.answer(text, reply_markup=get_admin_set_menu_keyboard())

# Добавление администратора
@dp.callback_query_handler(IsAdminCallBack(), text='add_admin')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer('DONE')

    await StorageAddAdmin.value.set()
    await call.message.answer('Введите ID администратора')

@dp.message_handler(IsAdminMessage(), state=StorageAddAdmin.value)
async def set_add_admin(message: types.Message, state: FSMContext):
    await state.finish()

    await db.add_admin(int(message.text))
    await message.answer('Добавлен!', reply_markup=get_admin_canced_setting_keyboard())

# Удаление администратора
@dp.callback_query_handler(IsAdminCallBack(), text='delete_admin')
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.answer('DONE')

    await StorageDeleteAdmin.value.set()
    await call.message.answer('Введите ID администратора')

@dp.message_handler(IsAdminMessage(), state=StorageDeleteAdmin.value)
async def set_add_admin(message: types.Message, state: FSMContext):
    await state.finish()

    await db.delete_admin(int(message.text))
    await message.answer('Удален!', reply_markup=get_admin_canced_setting_keyboard())

# Рефералы
@dp.callback_query_handler(IsAdminCallBack(), text='seting_referals', state='*')
async def ref_settings(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    refs = await db.get_all_ref()

    text = ''
    for i, ref in enumerate(refs):
        referals = len(await db.get_all_user_ref(ref[1]))
        text += f'{i + 1}. {ref[1]} - ({ref[2] + referals} / {ref[2]}) пользователей\n'

    await call.message.answer(f'🔗 Статистика: \n\n{text}', reply_markup=get_ref_setting_menu_keyboard())

# Создание реферала
@dp.callback_query_handler(IsAdminCallBack(), text='create_referal', state='*')
async def create_ref(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await StorageCreateReferal.value.set()
    await call.message.answer('[СОЗДАНИЕ] Введите название рефералки:', reply_markup=ref_return_keyboard())

@dp.message_handler(IsAdminMessage(), state=StorageCreateReferal.value)
async def create_ref_set(message: types.Message, state: FSMContext):
    alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    ref = message.text.replace(' ', '_')
    if alphabet.isdisjoint(ref.lower()):
        await db.create_ref(ref)
        await state.finish()
        return await message.answer(f'Рефералка {ref} добавлена!', reply_markup=ref_return_keyboard())
    await message.answer('Введите имя без русских символов!', reply_markup=ref_return_keyboard())

# Удаление реферала
@dp.callback_query_handler(IsAdminCallBack(), text_startswith='delete_referal:', state='*')
async def delete_ref(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    name = call.data.split(':')[1]

    await call.message.answer(f'Вы точно хотите удалить "{name}"?', reply_markup=get_delete_ref_keyboard(name))

@dp.callback_query_handler(IsAdminCallBack(), text='ref_nd', state='*')
async def delete_ref_canced(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    await call.message.answer('Отменено!', reply_markup=ref_return_keyboard())

@dp.callback_query_handler(IsAdminCallBack(), text_startswith='ref_d:', state='*')
async def delete_ref_canced(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()

    name = call.data.split(':')[1]
    await db.delete_ref(name)

    await call.message.answer('Удалено!', reply_markup=ref_return_keyboard())

# Просмотр реферала
@dp.callback_query_handler(IsAdminCallBack(), text='show_referal', state='*')
async def show_ref(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await StorageShowReferal.value.set()
    await call.message.answer('[ПРОСМОТР] Введите название рефералки:', reply_markup=ref_return_keyboard())

@dp.message_handler(IsAdminMessage(), state=StorageShowReferal.value)
async def show_ref_name(message: types.Message, state: FSMContext):
    await state.finish()

    ref = await db.get_ref(message.text)
    referals = len(await db.get_all_user_ref(message.text))
    if ref:
        me = await bot.get_me()
        return await message.answer(
            f'🔒 ID: {ref["id"]}\n'
            f'🏷 Имя: {ref["name"]}\n\n'
            f'Количество приглашенных: <b>{ref["referals"] + referals} чел.</b>\n'
            f'Количество дошедших: <b>{ref["referals"]} чел.</b>\n\n'
            f'🔗 Ссылка: https://t.me/{me.username}?start={ref["name"]}\n', reply_markup=ref_return_keyboard(name=ref['name'])
        )

    return await message.answer(f'Рефералка не найдена!', reply_markup=ref_return_keyboard())

# Изменить реферала
@dp.callback_query_handler(IsAdminCallBack(), text_startswith='change_ref:', state='*')
async def change_ref(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    await StorageChangeReferal.value.set()
    async with state.proxy() as data:
        data['name'] = call.data.split(':')[1]

    await call.message.answer('Введите новое "Имя"', reply_markup=ref_return_keyboard())

@dp.message_handler(IsAdminMessage(), state=StorageChangeReferal.value)
async def show_ref_name(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        ref = message.text.replace(' ', '_')
        if alphabet.isdisjoint(ref.lower()):
            await db.change_ref(data['name'], ref)
            await message.answer('Изменено', reply_markup=ref_return_keyboard())
            return await state.finish()
        await message.answer('Введите ссылку без русских символов!', reply_markup=ref_return_keyboard())