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

@router.message(StateFilter(None), Command("list"))
async def list(message: Message, state: FSMContext):
    await message.answer(
        "Выберите серию измерений"
    )