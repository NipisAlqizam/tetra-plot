import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiomysql import Connection

from states import NewSeries, AddMeasurements
import db
import models
from keyboards import get_pages_keyboard
from keyboards import PagesCallbackFactory
from texts import get_measurement_adding_text

router = Router()
router.message.filter(F.text)


@router.message(StateFilter(None), Command("list"))
async def list(message: Message, state: FSMContext, connection: Connection):
    series_by = await db.measuring.get_series_by_user_id(connection, message.chat.id)
    series_list = []
    series_list.append(f"Выберите серию измерений: ")
    for i, series in enumerate(series_by, start=1):
        series_list.append(
            f"{i}. {series.title} с осями {series.x_name} и {series.y_name}"
        )
    await message.answer(
        "\n".join(series_list), reply_markup=get_pages_keyboard(series_by)
    )


@router.callback_query(PagesCallbackFactory.filter())
async def callback_id_read(
    callback: CallbackQuery, callback_data: PagesCallbackFactory, connection: Connection
):
    measurements_by = await db.measuring.get_measurements(
        connection, callback_data.series_id
    )
    measurements_list = []
    measurements_list.append(
        f"Вы выбрали серию измерений {callback_data.series_id} \n\n Сохранённые данные:\n"
    )
    for measurement in measurements_by:
        measurements_list.append(
            f"{measurement.x} {measurement.y} {measurement.comment}"
        )
    await callback.message.answer("\n".join(measurements_list))
    await callback.answer()
