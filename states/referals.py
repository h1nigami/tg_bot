from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageCreateReferal(StatesGroup):
    value = State()

class StorageShowReferal(StatesGroup):
    value = State()

class StorageChangeReferal(StatesGroup):
    value = State()