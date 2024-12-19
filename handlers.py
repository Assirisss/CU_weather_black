import os.path
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio
from get_weather_api import get_forecast_weather, get_forecast_weather_gor_n_days
from data_for_plot import get_data_for_plot, create_photo
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

CITY_FORECAST = 'Moscow'
DAYS_FORECAST = 3


router = Router()

class ChangeValues(StatesGroup):
    city = State()
    days = State()






@router.message(F.text == '/start')
async def start_command(message: types.Message):
    await message.answer(
        'Добро пожаловать в бота погоды!',
        reply_markup=kb.main
    )

@router.message(F.text == '/weather')
async def send_weather(message: types.Message):
    create_photo(CITY_FORECAST, DAYS_FORECAST)
    path = os.path.dirname(os.path.abspath(__file__))
    await message.answer_photo(photo=types.FSInputFile(path=os.path.join(path, 'photos/subplot_layout.png')))

@router.message(F.text == 'Режим прогноза погоды')
async def send_edit_values_forecast(message: types.Message):
    await message.answer('Выбранные условия:\n'
                         f'Город -- {CITY_FORECAST} \n'
                         f'Период --  {DAYS_FORECAST} days'
                         f'\n'
                         f'Измените данные', reply_markup=kb.chose_city_or_days)

@router.callback_query(F.data == 'change_city')
async def change_city(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите новый город')
    await state.set_state(ChangeValues.city)

@router.message(ChangeValues.city)
async def get_city(message: types.Message, state: FSMContext):
    global CITY_FORECAST
    await state.update_data(city=message.text)
    CITY_FORECAST = message.text
    await state.clear()

    await message.answer('Город изменен!\n'
                         'Выбранные условия:\n'
                         f'Город -- {CITY_FORECAST} \n'
                         f'Период --  {DAYS_FORECAST} days'
                         f'\n'
                         f'Измените данные', reply_markup=kb.chose_city_or_days)

@router.callback_query(F.data == 'change_days')
async def change_days(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите новый период')
    await state.set_state(ChangeValues.days)

@router.message(ChangeValues.days)
async def get_days(message: types.Message, state: FSMContext):
    global DAYS_FORECAST
    await state.update_data(days=message.text)
    DAYS_FORECAST = int(message.text)
    await state.clear()
    await message.answer('Период изменен!\n'
                         'Выбранные условия:\n'
                         f'Город -- {CITY_FORECAST} \n'
                         f'Период --  {DAYS_FORECAST} days'
                         f'\n'
                         f'Измените данные', reply_markup=kb.chose_city_or_days)


@router.callback_query(F.data == 'confirm')
async def change_city(call: types.CallbackQuery):
    create_photo(CITY_FORECAST, DAYS_FORECAST)
    path = os.path.dirname(os.path.abspath(__file__))
    await call.answer()
    await call.message.answer_photo(photo=types.FSInputFile(path=os.path.join(path, 'photos/subplot_layout.png')))
