from aiogram.fsm.state import State, StatesGroup


class NewSeries(StatesGroup):
    choosing_title = State()
    choosing_x_name = State()
    choosing_y_name = State()
