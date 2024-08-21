import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import NewSeries, AddMeasurements
import db
import models
from keyboards import get_finish_keyboard
from texts import get_measurement_adding_text

router = Router()
router.message.filter(F.text)
logger = logging.getLogger(__name__)


@router.message(StateFilter(None), Command("new"))
async def new_series(message: Message, state: FSMContext):
    await message.answer(
        "Создание новой серии измерений. Для отмены введите /cancel\n\nВведите название:"
    )
    await state.set_state(NewSeries.choosing_title)


@router.message(NewSeries.choosing_title)
async def new_series_title(message: Message, state: FSMContext):
    await state.update_data(series_title=message.text)
    await message.answer("Введите название для оси абсцисс:")
    await state.set_state(NewSeries.choosing_x_name)


@router.message(NewSeries.choosing_x_name)
async def new_series_x_title(message: Message, state: FSMContext):
    await state.update_data(series_x_title=message.text)
    await message.answer("Введите название для оси ординат:")
    await state.set_state(NewSeries.choosing_y_name)


@router.message(NewSeries.choosing_y_name)
async def new_series_x_title(message: Message, state: FSMContext):
    await state.update_data(series_y_title=message.text)
    user_data = await state.get_data()
    done_text = f"Готово, измерения будут сохранены под названием {user_data['series_title']} с осями {user_data['series_x_title']} и {user_data['series_y_title']}"
    await message.answer(done_text)

    await state.set_state(AddMeasurements.adding)
    msg = await message.answer(
        get_measurement_adding_text(
            user_data["series_x_title"], user_data["series_y_title"]
        ),
        reply_markup=get_finish_keyboard(),
    )
    await state.update_data(series_msg=msg)
    await state.update_data(measurements=[])

    series = models.Series(
        user_id=message.chat.id,
        title=user_data["series_title"],
        x_name=user_data["series_x_title"],
        y_name=user_data["series_y_title"],
    )
    connection = await db.get_mysql_connection("tetraplot")
    await state.update_data(connection=connection)
    series_id = await db.measuring.add_series(connection, series)
    await state.update_data(series_id=series_id)
    logger.info(f"Created new series with id {series_id}")
