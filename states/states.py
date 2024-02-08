from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    phone_number = State()
    name = State()
    surname = State()