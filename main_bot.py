import os.path

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from handlers import router
import asyncio
from get_weather_api import get_forecast_weather, get_forecast_weather_gor_n_days
from data_for_plot import get_data_for_plot
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


API_TOKEN = '7986428820:AAHgPe3l-Ruj5DhHzjUiF_JEUCV4-Pb1b6I'


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)




if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')