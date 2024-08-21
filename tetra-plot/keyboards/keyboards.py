from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


def get_finish_keyboard() -> InlineKeyboardMarkup:
    """Returns keyboard with finish button"""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Закончить", callback_data="finish"))
    return kb.as_markup()


class PagesCallbackFactory(CallbackData, prefix="pages"):
    action: str
    page_number: Optional[int] = None


def get_pages_keyboard(
    first_num: int = 1, max_num: int | None = None
) -> InlineKeyboardMarkup:
    """
    Returns keyboard with up to 5 page numbers with specified first and maximum page number.

    Displays 5 pages if doesn't reach the `max_num` page. Displays only pages up to `max_num` otherwise.

    :param first_num: first displayed page
    :param max_num: biggest possible page number
    """
    kb = InlineKeyboardBuilder()
    if max_num:
        number_of_displayed_pages = min(5, max_num - first_num + 1)
    else:
        number_of_displayed_pages = 5
    for i in range(first_num, first_num + number_of_displayed_pages):
        kb.button(
            text=str(i),
            callback_data=PagesCallbackFactory(action="select", page_number=i),
        )
    kb.button(text="<", callback_data=PagesCallbackFactory(action="previous"))
    kb.button(text="Отмена", callback_data=PagesCallbackFactory(action="cancel"))
    kb.button(text=">", callback_data=PagesCallbackFactory(action="next"))
    kb.adjust(number_of_displayed_pages, 3)
    return kb.as_markup()
