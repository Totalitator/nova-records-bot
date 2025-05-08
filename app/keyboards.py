from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⏳ Забронировать время', callback_data='booking_time')],
    [InlineKeyboardButton(text='📕 Посмотреть услуги', callback_data = 'services')],
    [InlineKeyboardButton(text='🏰 Как до нас добраться?', callback_data = 'address')],
])

address = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='main')],
])

services = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data='main')],
])

booking_time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💻 Посмотреть свободные часы', url='https://docs.google.com/spreadsheets/d/1p0egVXmqEi6MQfKnvTpmC_hmwUKf5nkZ31y5NZckeQk/edit?usp=sharing')],
    [InlineKeyboardButton(text='🔔 Записаться', callback_data = 'meeting')],
    [InlineKeyboardButton(text='⬅️ Назад в меню', callback_data = 'main')],
])

payment_ready = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆗 Перейти к оплате', callback_data = 'go_payment')],
    [InlineKeyboardButton(text='🚫 Назад в меню', callback_data = 'main')],
])
