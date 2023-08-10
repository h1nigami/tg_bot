from aiogram.dispatcher.filters.state import State, StatesGroup

class StorageChangeLink(StatesGroup):
    value = State()
    link = State()

class StorageChangeNewLink(StatesGroup):
    value = State()
    link = State()

class StorageEditManager(StatesGroup):
    value = State()

class StorageDeleteAdmin(StatesGroup):
    value = State()

class StorageAddAdmin(StatesGroup):
    value = State()

