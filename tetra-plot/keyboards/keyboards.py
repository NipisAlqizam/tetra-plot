from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_finish_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Закончить", callback_data="finish"))
    return kb.as_markup()


def get_pages_keyboard(
    first_num: int = 1, max_num: int | None = None
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if max_num:
        number_of_displayed_pages = min(5, max_num - first_num + 1)
    else:
        number_of_displayed_pages = 5
    for i in range(first_num, first_num + number_of_displayed_pages):
        kb.button(text=str(i), callback_data="pages" + str(i))
    kb.button(text="<", callback_data="pages_back")
    kb.button(text="Отмена", callback_data="pages_cancel")
    kb.button(text=">", callback_data="pages_forward")
    kb.adjust(number_of_displayed_pages, 3)
    return kb.as_markup()
