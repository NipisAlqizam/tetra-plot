import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiomysql import Connection

from states import NewSeries, AddMeasurements
import db
import models
from keyboards import get_pages_keyboard
from texts import get_measurement_adding_text

router = Router()
router.message.filter(F.text)

@router.message(StateFilter(None), Command("list"))
async def list(message: Message, state: FSMContext, connection: Connection):
    series_by = await db.measuring.get_series_by_user_id(connection, message.chat.id)
    series_list = [] 
    series_list.append(f"Выберите серию измерений: ")
    for i, series in enumerate(series_by, start=1):
        series_list.append(f"{i}. {series.title} с осями {series.x_name} и {series.y_name}")
    await message.answer('\n'.join(series_list), 
    reply_markup = get_pages_keyboard(series_by))

@dp.callback_query