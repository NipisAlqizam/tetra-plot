import logging
import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import AddMeasurements
import db
import models
import texts
from keyboards import get_finish_keyboard

router = Router()
router.message.filter(F.text)
logger = logging.getLogger(__name__)


@router.message(AddMeasurements.adding)
async def add_measurement(message: Message, state: FSMContext):
    user_data = await state.get_data()
    match: re.Match = re.match(
        r"(\d+(?:[,.]\d+)?) (\d+(?:[,.]\d+)?)(?: (.+))?", message.text
    )
    if match is None:
        await message.answer(
            "Нужно ввести через пробел два числа и, опционально, комментарий"
        )
        return
    x = match.group(1)
    y = match.group(2)
    try:
        comment = match.group(3)
    except IndexError:
        comment = ""
    if comment is None:
        comment = ""

    logger.debug(f"Received {x=}, {y=}, {comment=}")
    if "," in x:
        x = x.replace(",", ".")
    if "," in y:
        y = y.replace(",", ".")
    x = float(x)
    y = float(y)
    logger.info(f"Got {x=}, {y=}, {comment=}")

    measurement = models.Measurement(
        series_id=user_data["series_id"],
        measurement_time=message.date,
        x=x,
        y=y,
        comment=comment,
    )
    await db.measuring.add_measurement(user_data["connection"], measurement)

    measurements: list[models.Measurement] = user_data["measurements"]
    logger.info(user_data["measurements"])
    measurements.append(measurement)
    series_msg: Message = user_data["series_msg"]
    await series_msg.edit_text(
        texts.get_measurement_adding_text(
            user_data["series_x_title"], user_data["series_y_title"], measurements
        ),
        reply_markup=get_finish_keyboard(),
    )


@router.callback_query(AddMeasurements.adding, F.data == "finish")
async def finish_measurement(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    connection = user_data["connection"]
    connection.close()

    series_msg: Message = user_data["series_msg"]
    await series_msg.delete_reply_markup()

    user_data.clear()

    await callback.answer("Готово")
