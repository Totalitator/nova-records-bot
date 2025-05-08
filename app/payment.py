from aiogram.types import LabeledPrice

async def set_price(hours):
    price = LabeledPrice(label='Оплата брони', amount=800*100*hours)
    return price