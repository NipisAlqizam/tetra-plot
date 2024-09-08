from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(F.text, StateFilter(None), Command("start"))
async def start(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Что сделано:"),
            "Работа с базой данных",
            "Создание серий",
            "Ввод данных",
        ),
        as_marked_section(
            Bold("Что планируется:"),
            "Отображение списка измерений",
            "Редактирование",
            "Экспорт",
            "Создание диаграмм",
            "Редактирование диаграмм",
            "Импорт",
            "Сохранение в pdf",
        ),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())


@router.message(F.text, Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data.get("button_msg"):
        await user_data["button_msg"].delete_reply_markup()
    await state.clear()
    await message.answer("Всё отменено")
