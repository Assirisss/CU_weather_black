from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Режим прогноза погоды'),
        KeyboardButton(text='Режим маршрута'),

    ]
], resize_keyboard=True)

chose_city_or_days = InlineKeyboardMarkup(inline_keyboard=
                                          [
                                                [
                                                    InlineKeyboardButton(text='Изменить город', callback_data='change_city'),
                                                    InlineKeyboardButton(text='Изменить период', callback_data='change_days'),
                                                ],
                                              [InlineKeyboardButton(text='Подтвердить', callback_data='confirm')]
                                          ]
                                          )

# chose_city = InlineKeyboardMarkup(inline_keyboard=
#                                           [
#                                                 [
#                                                     InlineKeyboardButton(text='Moscow', callback_data='Moscow'),
#                                                     InlineKeyboardButton(text='Sochi', callback_data='Sochi'),
#                                                     InlineKeyboardButton(text='Rostov-on-Don', callback_data='Rostov-on-Don'),
#                                                 ],
#                                               [InlineKeyboardButton(text='Подтвердить', callback_data='confirm')]
#                                           ]
#                                           )