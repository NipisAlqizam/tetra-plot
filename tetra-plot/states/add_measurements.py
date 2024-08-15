from aiogram.fsm.state import State, StatesGroup


class AddMeasurements(StatesGroup):
    adding = State()
