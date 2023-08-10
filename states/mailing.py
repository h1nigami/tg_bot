from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageMailing(StatesGroup):
    value = State()
    button = State()