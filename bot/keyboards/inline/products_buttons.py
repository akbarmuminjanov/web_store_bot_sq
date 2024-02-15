from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


back_callback = CallbackData("back", "category_id", "subcategory_id")
sub_category_callback = CallbackData("subcategory", "category", "id")
product_callback = CallbackData("product", "subcategory", "id")
shopping_callback = CallbackData("shop", "product_id", "user_id")
buy_product_callback=CallbackData("buy", "total_price", "description")

async def subcategories_keyboard(subcategories):
    markup = InlineKeyboardMarkup(row_width=2)

    for i in subcategories:
        button_text = i[1]

        callback_data = sub_category_callback.new(category=i[1], id=i[0])
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    
    markup.row(
        InlineKeyboardButton(
            text="⬅️Orqaga", callback_data=back_callback.new(category_id=0, subcategory_id=0))
        )
    return markup

def products_keyboard(products, category_id):
    markup = InlineKeyboardMarkup(row_width=2)

    for i in products:
        button_text = i[2]

        callback_data = product_callback.new(subcategory=i[5], id=i[0])

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="⬅️Orqaga", callback_data=back_callback.new(category_id=category_id, subcategory_id=0))
        )
    return markup

def shopping_keyboard(product_id, user_id, subcategory_id):
    markup = InlineKeyboardMarkup(row_width=1)

    callback_data = shopping_callback.new(product_id=product_id, user_id=user_id)

    markup.insert(
        InlineKeyboardButton("Savatga qo'shish 🛒", callback_data=callback_data)
    )

    markup.row(
        InlineKeyboardButton(
            text="⬅️Orqaga", callback_data=back_callback.new(category_id=0, subcategory_id=subcategory_id))
        )
    return markup

async def buy_product(total_price, description):
    markup = InlineKeyboardMarkup(row_width=1)

    callback_data = buy_product_callback.new(total_price=total_price, description=description)

    markup.insert(
        InlineKeyboardButton(text="Xarid qilish", callback_data=callback_data)
    )

    markup.insert(
        InlineKeyboardButton(
            text="⬅️Orqaga", callback_data=back_callback.new(category_id=0, subcategory_id=0))
    )

    return markup


back_button = InlineKeyboardMarkup(row_width=1)

back_button.insert(
    InlineKeyboardButton(
        text="⬅️Orqaga", callback_data=back_callback.new(category_id=0, subcategory_id=0))
)