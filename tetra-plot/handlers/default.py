from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import Bold, as_list, as_marked_section, as_key_value

router = Router()


@router.message(F.text, Command("start"))
async def start(message: Message):
    content = as_list(
        as_marked_section(Bold("Что сделано:"), "Работа с базой данных"),
        as_marked_section(
            Bold("Что планируется:"),
            "Создание серий",
            "Ввод данных",
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
