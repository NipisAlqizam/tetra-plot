from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from db.initialize_db import get_mysql_connection
from aiomysql import Connection
from aiogram.types import TelegramObject


class DbConnectionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        connection = await get_mysql_connection('tetraplot')
        data["connection"] = connection
        result = await handler(event, data)
        connection.close()
        return result
