from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


import app.assets.texts as text
import app.assets.photos as photo
import app.keyboards as kb
import app.sheets as sheets
import app.payment as pay

from config import PAYMENT_TOKEN
from aiogram.types import PreCheckoutQuery
from aiogram.types.message import ContentType


router = Router()

class User(StatesGroup):
    date = State()
    start = State()
    hours = State()
    date_row = State()
    start_col = State()
    end_col = State()
    

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=text.start_text, reply_markup=kb.main)
    await message.answer(f'{message.message_thread_id}')
    await message.delete()

@router.callback_query(F.data == 'main')
async def start(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(text=text.start_text, reply_markup=kb.main)
    await callback.message.delete()

@router.callback_query(F.data == 'address')
async def address(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text=f'Наша студия находится в Черниковке, по адресу Льва Толстого, 21! Третий этаж, офис первый', reply_markup=kb.address)

@router.callback_query(F.data == 'services')
async def address(callback: CallbackQuery):
    await callback.answer('')
    media = InputMediaPhoto(media=photo.headphones_01, caption = f'{text.services_text}')
    await callback.message.edit_media(media = media, reply_markup=kb.services)

@router.callback_query(F.data == 'booking_time')
async def booking_time(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text=text.booking_text, reply_markup=kb.booking_time)

@router.callback_query(F.data == 'meeting')
async def meeting(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(text='Какой день хотите забронировать?')
    await state.set_state(User.date)

@router.message(User.date)
async def date_time(message: Message, state: FSMContext):

    response_Date = await sheets.check_date(message.text)
    if response_Date is not None:
        await message.answer(f'{response_Date}\nВыберите другой день.')
        await state.set_state(User.date)
    else:
        await state.update_data(date = message.text)
        await message.answer('На какое время?')
        await state.set_state(User.start)

@router.message(User.start)
async def start_time(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = user_data.get('date')
    response_Start = await sheets.check_time(date, message.text)
    if response_Start is not None:
        await message.answer(f'{response_Start}\nВыберите другое время.')
        await state.set_state(User.start)
    else:
        await state.update_data(start = message.text)
        await message.answer("На сколько часов?")
        await state.set_state(User.hours)

@router.message(User.hours)
async def add_hours(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date = user_data.get('date')
    start = user_data.get('start')
    response_Hours, date_row, start_col, end_col = await sheets.check_hours(date, start, message.text)

    if response_Hours is not None:
        await message.answer(f'{response_Hours}')
        await state.set_state(User.hours)

    else:
        await state.update_data(hours = message.text, date_row = date_row, start_col=start_col, end_col=end_col)
        await message.answer('Часы свободны, переходим к оплате?', reply_markup=kb.payment_ready)
        await state.set_state(None)

@router.callback_query(F.data == 'go_payment')
async def buy(callback: CallbackQuery, state: FSMContext):
    if PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await callback.message.answer("Тестовый платеж!!!")
    
    user_data = await state.get_data()
    hours = user_data.get('hours')
    price = await pay.set_price(int(hours))

    await callback.message.answer_invoice(
                           title="Запись",
                           description="800 руб/час",
                           provider_token=PAYMENT_TOKEN,
                           currency="rub",
                           photo_url="https://sun21-2.userapi.com/impg/gff_kVrWldEeMeIaNfcE_BCNxR1KgVN_JNqOrQ/2qiBUvXYfms.jpg?size=2560x1440&quality=95&sign=a570a1652a73c643c2157edb13b01da5&type=album",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[price],
                           start_parameter="booking",
                           payload="invoice-payload")

# pre checkout  (must be answered in 10 seconds)
@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)
    print('ебаный насрал')

# successful payment
@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext):
    user_data = await state.get_data()
    date_row = int(user_data.get('date_row'))
    start_col = int(user_data.get('start_col'))
    end_col = int(user_data.get('end_col'))

    await sheets.booking_cells(date_row, start_col, end_col)

    await message.answer(f'{date_row}{start_col}{end_col}')

    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")

    await message.bot.send_message(chat_id=-1002494435087,text=f'@{message.from_user.username} забронировал время', message_thread_id=76)
