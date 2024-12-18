from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Вставь сюда токен
API_TOKEN = '7986428820:AAHgPe3l-Ruj5DhHzjUiF_JEUCV4-Pb1b6I'

# Создаём бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Состояния
STATE_SELECTING = 'SELECTING'  # Состояние выбора блюда
STATE_CONFIRMING = 'CONFIRMING'  # Состояние подтверждения заказа
STATE_COLLECTING_INFO = 'COLLECTING_INFO'  # Состояние сбора информации
STATE_THANKS = 'THANKS'  # Состояние благодарности

# Словарь для хранения состояния пользователей
user_states = {}

# Пример меню ресторана
menu = {
    'Пицца Маргарита': 500,
    'Суши сет': 600,
    'Бургер с картошкой фри': 350,
    'Цезарь': 400
}

# Пример дополнительных услуг
extra_services = {
    'Десерт': 150,
    'Напитки': 100
}

# Обработчик команды /start
@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    user_states[message.from_user.id] = {'state': STATE_SELECTING, 'order': [], 'user_info': {}}
    await message.answer(
        'Добро пожаловать в наш ресторан! Выберите блюда из меню ниже:',
        reply_markup=await get_menu_keyboard()
    )


# Функция для создания клавиатуры с блюдами
async def get_menu_keyboard():
    inline_buttons = []
    for dish, price in menu.items():
        button = InlineKeyboardButton(text=f'{dish} - {price}₽', callback_data=dish)
        inline_buttons.append(button)

    # Создаём InlineKeyboardMarkup с нужной структурой
    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_buttons], row_width=2)
    return keyboard


# Функция для создания клавиатуры с дополнительными услугами
async def get_extra_services_keyboard():
    inline_buttons = []
    for service, price in extra_services.items():
        button = InlineKeyboardButton(text=f'{service} - {price}₽', callback_data=service)
        inline_buttons.append(button)

    # Кнопка «Нет» для отказа от услуг
    inline_buttons.append(InlineKeyboardButton(text='Нет, не хочу дополнительные услуги', callback_data='no_extra'))

    # Создаём InlineKeyboardMarkup с нужной структурой
    keyboard = InlineKeyboardMarkup(inline_keyboard=[inline_buttons], row_width=2)
    return keyboard


# Функция для создания инлайн-клавиатуры с подтверждением заказа
async def get_confirm_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить заказ', callback_data='confirm_order'),
            InlineKeyboardButton(text='Изменить заказ', callback_data='change_order')
        ]
    ])
    return keyboard

# Обработка инлайн-кнопок с выбором блюд
@dp.callback_query(F.data.in_(menu.keys()))
async def handle_dish_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    dish = callback_query.data

    # Проверяем, есть ли выбранное блюдо в меню
    if dish in menu:
        if 'order' not in user_states[user_id]:
            user_states[user_id]['order'] = []
        user_states[user_id]['order'].append(dish)
        await callback_query.answer(f'Вы добавили в заказ: {dish}')

    # После того как выбрали блюдо, предложим выбрать дополнительные услуги
    keyboard = await get_extra_services_keyboard()
    await callback_query.message.answer(
        'Выберите дополнительные услуги (десерт, напитки и т. д.):',
        reply_markup=keyboard
    )
    user_states[user_id]['state'] = STATE_SELECTING


# Обработка инлайн-кнопок для дополнительных услуг
@dp.callback_query(F.data.in_(extra_services.keys()))
async def handle_extra_service_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    service = callback_query.data

    # Проверяем, есть ли выбранная услуга в extra_services
    if service in extra_services:
        if 'extra_services' not in user_states[user_id]:
            user_states[user_id]['extra_services'] = []
        user_states[user_id]['extra_services'].append(service)
        await callback_query.answer(f'Вы добавили в заказ: {service}')

    # После добавления всех услуг предложим выбрать, подтвердить заказ или изменить его
    keyboard = await get_confirm_keyboard()
    await callback_query.message.answer(
        'Ваши дополнительные услуги добавлены. Вы хотите подтвердить заказ или изменить его?',
        reply_markup=keyboard
    )
    user_states[user_id]['state'] = STATE_CONFIRMING


# Обработка отказа от дополнительных услуг (кнопка «Нет»)
@dp.callback_query(F.data == 'no_extra')
async def handle_no_extra_services(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await callback_query.answer('Вы отказались от дополнительных услуг.')

    # После отказа предложим выбрать, подтвердить заказ или изменить его
    keyboard = await get_confirm_keyboard()
    await callback_query.message.answer(
        'Вы хотите подтвердить заказ или изменить его?',
        reply_markup=keyboard
    )
    user_states[user_id]['state'] = STATE_CONFIRMING


# Обработка кнопки «Подтвердить заказ»
@dp.callback_query(F.data == 'confirm_order')
async def confirm_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Проверка на наличие заказов
    if user_id in user_states and len(user_states[user_id]['order']) > 0:
        order_list = '\n'.join(user_states[user_id]['order'])
        extra_services_list = '\n'.join(user_states[user_id].get('extra_services', []))
        total_price = sum(menu[dish] for dish in user_states[user_id]['order']) + sum(
            extra_services[service] for service in user_states[user_id].get('extra_services', []))

        # Информация о заказе
        await callback_query.message.answer(
            f'Ваш заказ: \n{order_list}\nДополнительные услуги: \n{extra_services_list}\n\nИтого: {total_price}₽\nСпасибо за заказ! Мы скоро свяжемся с вами.'
        )

        # Завершаем заказ
        user_states[user_id]['state'] = STATE_THANKS
        user_states[user_id]['order'] = []  # очищаем заказ
        user_states[user_id]['extra_services'] = []  # очищаем дополнительные услуги

    else:
        await callback_query.message.answer('Вы не выбрали блюда для заказа.')


# Обработка кнопки «Изменить заказ»
@dp.callback_query(F.data == 'change_order')
async def change_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Сброс состояния и предложение выбрать блюдо заново
    user_states[user_id] = {'state': STATE_SELECTING, 'order': [], 'user_info': {}}
    await callback_query.message.answer(
        'Выберите блюда из меню ниже:',
        reply_markup=await get_menu_keyboard()
    )


# Обработка других сообщений
@dp.message()
async def handle_unknown_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос. Пожалуйста, выберите команду или кнопку.')


# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')