import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN_API
from app.handlers import router


 
bot = Bot(token=TOKEN_API, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)) 
dp=Dispatcher()



async def main():
    dp.include_router(router)
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')