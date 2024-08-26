from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from models import Series

def get_finish_keyboard() -> InlineKeyboardMarkup:
    """Returns keyboard with finish button"""
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Закончить", callback_data="finish"))
    return kb.as_markup()


class PagesCallbackFactory(CallbackData, prefix="pages"):
    series_id: int


def get_pages_keyboard(series_list: list[Series]
) -> InlineKeyboardMarkup:
    """
    Returns keyboard with up to 5 page numbers with specified first and maximum page number.

    Displays 5 pages if doesn't reach the `max_num` page. Displays only pages up to `max_num` otherwise.

    :param first_num: first displayed page
    :param max_num: biggest possible page number
    """
    kb = InlineKeyboardBuilder()
    for i, s in enumerate(series_list, start=1):
        kb.button(
            text=str(i),
            callback_data=PagesCallbackFactory(series_id=s.id),
        )
    kb.adjust(5, repeat=True)
    return kb.as_markup()
