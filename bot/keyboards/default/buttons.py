from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="📃katalog"),
            KeyboardButton(text="🛒корзина"),
            KeyboardButton(text="⏳история заказов"),
        ]
    ],
    resize_keyboard=True
)


async def category_buttons(categories):
    keyboard = [
        [],
    ]

    for i in categories:
        if len(keyboard[-1]) < 2:
            keyboard[-1].append(KeyboardButton(f'🌀 {i[1]}'))
        else:
            keyboard.append([KeyboardButton(f'🌀 {i[1]}')])
        
    keyboard.append([
         KeyboardButton("◀️ Назад")
    ])

    cats = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    return cats