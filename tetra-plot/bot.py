import logging

import asyncio
from aiogram import Bot, Dispatcher

import config
from handlers import default

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(default.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s %(levelname)s %(name)s] %(message)s', level=logging.INFO)
    asyncio.run(main())