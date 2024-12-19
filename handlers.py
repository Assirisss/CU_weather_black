import os.path
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio
from get_weather_api import get_forecast_weather, get_forecast_weather_gor_n_days
from data_for_plot import get_data_for_plot, create_photo_weather, create_map_for_trip
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from check_city import check_city

CITY_FORECAST = 'Moscow'
DAYS_FORECAST = 3
START_CITY = 'Moscow'
END_CITY = 'Saint Petersburg'
CITY_POINTS = []

router = Router()


class ChangeValues(StatesGroup):
    city = State()
    days = State()


class mode_of_trip(StatesGroup):
    start = State()
    end = State()
    add_point = State()


@router.message(F.text == '/start')
async def start_command(message: types.Message):
    await message.answer(
        'Добро пожаловать в бота погоды!',
        reply_markup=kb.main
    )


@router.message(F.text == '/weather')
async def send_weather(message: types.Message):
    create_photo_weather(CITY_FORECAST, DAYS_FORECAST)
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
    if check_city(message.text, 'ru' ) or check_city(message.text, 'en'):
        await state.update_data(city=message.text)
        CITY_FORECAST = message.text
        await state.clear()

        await message.answer('Город изменен!\n'
                             'Выбранные условия:\n'
                             f'Город -- {CITY_FORECAST} \n'
                             f'Период --  {DAYS_FORECAST} days'
                             f'\n'
                             f'Измените данные', reply_markup=kb.chose_city_or_days)
    else:
        await message.answer('Похоже такого города не существует.')
        await message.answer('Введите новый город')


@router.callback_query(F.data == 'change_days')
async def change_days(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите новый период')
    await state.set_state(ChangeValues.days)


@router.message(ChangeValues.days)
async def get_days(message: types.Message, state: FSMContext):
    global DAYS_FORECAST
    await state.update_data(days=message.text)
    if message.text.isdigit():
        DAYS_FORECAST = int(message.text)
        if 1 <= DAYS_FORECAST <= 5:
            await state.clear()
            await message.answer('Период изменен!\n'
                                 'Выбранные условия:\n'
                                 f'Город -- {CITY_FORECAST} \n'
                                 f'Период --  {DAYS_FORECAST} days'
                                 f'\n'
                                 f'Измените данные', reply_markup=kb.chose_city_or_days)
        else:
            await message.answer('Введите число от 1 до 5')
    else:
        await message.answer('Введите только число от 1 до 5')


@router.callback_query(F.data == 'confirm')
async def change_city(call: types.CallbackQuery):
    create_photo_weather(CITY_FORECAST, DAYS_FORECAST)
    path = os.path.dirname(os.path.abspath(__file__))
    await call.answer()
    await call.message.answer_photo(photo=types.FSInputFile(path=os.path.join(path, 'photos/subplot_layout.png')))


@router.message(F.text == 'Режим маршрута')
async def message_for_start_city(message: types.Message, state: FSMContext):
    await message.answer('Введите начальный город')
    await state.set_state(mode_of_trip.start)


@router.message(mode_of_trip.start)
async def get_start_city(message: types.Message, state: FSMContext):
    global START_CITY
    if check_city(message.text, 'ru' ) or check_city(message.text, 'en'):
        await state.update_data(start=message.text)
        START_CITY = message.text
        await state.clear()
        await message.answer('Введите конечный город')
        await state.set_state(mode_of_trip.end)
    else:
        await message.answer('Похоже такого города не существует.')
        await message.answer('Введите начальный город')


@router.message(mode_of_trip.end)
async def get_end_city(message: types.Message, state: FSMContext):
    global END_CITY
    if check_city(message.text, 'ru' ) or check_city(message.text, 'en'):
        await state.update_data(end=message.text)
        END_CITY = message.text
        await state.clear()
        await message.answer('Введите промежуточные города, если они есть', reply_markup=kb.add_city_poins)
        await state.set_state(mode_of_trip.add_point)
    else:
        await message.answer('Похоже такого города не существует.')
        await message.answer('Введите конечный город')


@router.callback_query(F.data == 'add_point')
async def add_point(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите промежуточный город')
    await state.set_state(mode_of_trip.add_point)


@router.message(mode_of_trip.add_point)
async def get_point(message: types.Message, state: FSMContext):
    global CITY_POINTS
    if check_city(message.text, 'ru' ) or check_city(message.text, 'en'):
        CITY_POINTS.append(message.text)
        await message.answer('Город добавлен!')
        await message.answer('Введите промежуточные города, если они есть', reply_markup=kb.add_city_poins)
    else:
        await message.answer('Похоже такого города не существует.')
        await message.answer('Введите промежуточный город')



@router.callback_query(F.data == 'confirm_points')
async def confirm_points(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer('Маршрут подтвержден! Выберите тип экспорта:', reply_markup=kb.type_map_export)


@router.callback_query(F.data == 'png')
async def create_map(call: types.CallbackQuery):
    path = os.path.dirname(os.path.abspath(__file__))
    await call.answer()
    try:
        create_map_for_trip(START_CITY, END_CITY, CITY_POINTS, 'png')
        await call.message.answer_photo(photo=types.FSInputFile(path=os.path.join(path, 'photos/map_layout.png')))
        mes = 'Погода на маршруте:\n'
        for city in [START_CITY] + CITY_POINTS + [END_CITY]:
            data = get_data_for_plot(city, 1).iloc[0]
            mes += f'{city}:\n' \
                   f'                          \n' \
                   f'Температура: {data["temp"]} °C\n' \
                   f'Влажность: {data["humidity"]} %\n' \
                   f'Скорость ветра: {data["speed_wind"]} м/с\n' \
                   f'Осадки: {data["rain"]} %\n' \
                   f'                          \n'
        await call.message.answer(mes)
    except Exception as e:
        await call.message.answer('Ошибка при создании карты. Скорее всего вы города, которые не существуют')


@router.callback_query(F.data == 'html')
async def create_map(call: types.CallbackQuery):
    path = os.path.dirname(os.path.abspath(__file__))
    await call.answer()
    try:
        create_map_for_trip(START_CITY, END_CITY, CITY_POINTS, 'html')
        await call.message.answer_document(document=types.FSInputFile(path=os.path.join(path, 'photos/map_layout.html')))
    except Exception as e:
        await call.message.answer('Ошибка при создании карты. Скорее всего вы города, которые не существуют2')
