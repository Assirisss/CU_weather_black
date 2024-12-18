from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio

API_TOKEN = '7986428820:AAHgPe3l-Ruj5DhHzjUiF_JEUCV4-Pb1b6I'


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    await message.answer(
        'Добро пожаловать в бота погоды!'
    )



if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')