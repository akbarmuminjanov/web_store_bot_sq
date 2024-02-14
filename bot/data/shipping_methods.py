from aiogram import types
from aiogram.types import LabeledPrice

REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title='Fargo (3 kun)',
    prices=[
        LabeledPrice(
            'Maxsus quti', 1000000),
        LabeledPrice(
            '3 ish kunida yetkazish', 1000000),
    ]
)

FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Exspress pochta (1 kun)',
    prices=[
        LabeledPrice(
            '1 kunda yetkazib berish', 1000000),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(id='pickup',
                                       title="Do'kondan olib ketish",
                                       prices=[
                                           LabeledPrice("Yetkazib berishsiz", -1000000)
                                       ])