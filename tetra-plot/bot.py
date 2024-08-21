import logging

import asyncio
from aiogram import Bot, Dispatcher

import config
from handlers import default, new_series, add_measurements
import db
from handlers import list


async def main():
    await db.init_db(config.DROP_DB_BEFORE_INIT)
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        default.router, new_series.router, add_measurements.router, list.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s %(levelname)s %(name)s] %(message)s", level=logging.INFO
    )
    asyncio.run(main())
