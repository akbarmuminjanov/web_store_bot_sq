from aiogram import types
from loader import db, dp, bot
from keyboards.default.buttons import category_buttons, menu
from keyboards.inline.products_buttons import (subcategories_keyboard, sub_category_callback, products_keyboard,
            product_callback, shopping_callback, shopping_keyboard, buy_product_callback, buy_product, back_button, back_callback)
from aiogram.dispatcher.filters.builtin import Text
import asyncio
from aiogram.types import LabeledPrice
from utils.misc.product import Product
from data.shipping_methods import *
from data.config import ADMINS


@dp.message_handler(text="📃katalog")
async def show_category(message: types.Message):
    categories = db.select_all_categories()
    button = await category_buttons(categories)

    await message.delete()
    await message.answer(f"kategoriya tanglang ⬇️", reply_markup=button)

@dp.message_handler(Text(startswith="🌀"))
async def show_subcategory(message: types.Message):
    category_name = message.text[1:].split()
    try:
        category = db.select_category(name=category_name[0])

        subcategories = db.select_subcategories(category_id=str(category[0]))

        button = await subcategories_keyboard(subcategories)

        await message.delete()
        await message.answer("Kategoriya tanlang ⬇️", reply_markup=button)

    except Exception as err:
        print(err)
        await message.answer("Noto'g'ri kategoriya")
    

@dp.message_handler(Text(equals='◀️ Orqaga'))
async def back_catalog(message: types.Message):
    await message.delete()
    await message.answer(f"Siz bosh menyudasiz ⬇️", reply_markup=menu)

#===============================================================================

# @dp.callback_query_handler(Text(startswith="back:"))
# async def back_menu(call: types.CallbackQuery):
#      await call.message.delete()

#================================================================================

@dp.callback_query_handler(sub_category_callback.filter())
async def back_menu(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.answer(cache_time=60)

    subcategory_id = str(callback_data['id'])
    subcat = db.select_subcategory(id=subcategory_id)

    products = db.select_products(sub_category_id=subcategory_id)
    button =  products_keyboard(products, category_id=subcat[2])
    await call.message.answer(text="Mahsulot tanlang:", reply_markup=button, )

#==================================================================================


@dp.callback_query_handler(product_callback.filter())
async def show_products(call: types.CallbackQuery, callback_data: dict):
    await call.answer()

    product = db.select_product(id=str(callback_data['id']))

    text = f"<b>📍nomi: {product[1]}</b>\n\n"
    text +=f"<b>📔mahsulot haqida: {product[2]}</b>\n\n"
    text +=f"<b>💸mahsulot narxi: {product[3]} ming so'm</b>\n\n"

    if product[4] == True:
        text +=f"<b>✅mahsulot bor</b>"
    elif product[4] == False:
        text +=f"<b>❌mahsulot tugadi</b>"

    keyboard =  shopping_keyboard(product[0], call.from_user.id, subcategory_id=product[5])
    await call.message.delete()

    product_image = product[-1]

    product_url = "http://webstorebot.pythonanywhere.com/media/" + str(product_image)

    if product[4] == True:
        await call.message.answer_photo(product[-1], caption=text, reply_markup=keyboard)
    elif product[4] == False:
        bot = await call.message.answer_photo(product[-1], caption=text)
        await asyncio.sleep(60)
        await bot.delete()

    try:
        await call.message.answer_photo(product_url, caption=text, reply_markup=keyboard)
    except:
        await call.message.answer_photo(product_image,caption=text, reply_markup=keyboard)

@dp.callback_query_handler(shopping_callback.filter())
async def add_to_cart(call: types.CallbackQuery, callback_data: dict):
    product_id = callback_data['product_id']
    user_id = callback_data['user_id']

    status = db.add_product_to_cart(user_id, product_id)
    if status == "error":
        await call.answer("🚫 Mahsulot qo'shib bo'lmadi")

    elif status == "added-before":
        await call.answer("‼️ Mahsulot oldin qo'shilgan")

    await call.answer(" ✅ Mahsulot savatga qo'shidi ")
    await call.message.delete()
    await call.message.answer("Menyu tanlang", reply_markup=menu)

@dp.message_handler(Text(equals='🛒savatcha'))
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    await message.delete()

    products = db.select_user_products(user_id=str(user_id))
    main_text = f"<b>Savatdagi tovarlar: </b>\n\n"
    text = ""
    counter = 1
    total_price = 0

    for product in products:
        pr = db.select_product(id=str(product[2]))
        text += f"<b>{counter}.📍Nomi: {pr[2]}</b>\n"
        text += f"<b>  💸Narxi: {pr[4]} ming so'm</b>\n\n"
        counter += 1
        total_price += pr[4]

    text += "Jami:  \n"
    text += f"Mahsulotlar soni: {counter -1}\n"
    text += f"Jami: {total_price} ming so'm"


    button = await buy_product(total_price, "This is our products")
    
    await message.answer(main_text + text, reply_markup=button)

@dp.callback_query_handler(buy_product_callback.filter())
async def send_invoice(call: types.CallbackQuery, callback_data:dict):
    await call.answer()

    product = Product(
        title="Savatchadagi mahsulotlar ro'yhati",
        description=callback_data['description'],
        currency="UZS",
        prices=[
            LabeledPrice(
                label='Mahsulotlar',
                amount=int(callback_data['total_price']+"00")
            ),
            LabeledPrice(
                label='Yetkazib berish (20-25 kun)',
                amount=1000000, #10.000 so'm
            ),
        ],
        start_parameter="products_cart_invoice",
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True, #Foydalanuvchi manzilini kiritishi shart
        is_flexible=True
    )


    await bot.send_invoice(chat_id=call.from_user.id, **product.generate_invoice(), payload="cart_shop")


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UZ":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Chet elga yetkazib berolmaymiz")
        
    elif query.shipping_address.city.lower() == "fergana":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[FAST_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)
        
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGULAR_SHIPPING],
                                        ok=True)
        
@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):

    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)

    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Xaridingiz uchun rahmat!")

    await bot.send_message(chat_id=ADMINS[0],
                           text=f"Quyidagi mahsulot sotildi: {pre_checkout_query.invoice_payload}\n"
                                f"ID: {pre_checkout_query.id}\n"
                                f"Telegram user: {pre_checkout_query.from_user.first_name}\n"
                                f"Xaridor: {pre_checkout_query.order_info.name}, tel: {pre_checkout_query.order_info.phone_number}\n"
                                f"Address: {pre_checkout_query.order_info.shipping_address.state}\n"
                                f"Address: {pre_checkout_query.order_info.shipping_address.street_line1}\n"
                                f"Address: {pre_checkout_query.order_info.shipping_address.street_line2}\n") 
    

    db.clear_user_cart(pre_checkout_query.from_user.id)

@dp.message_handler(Text(equals="⏳mening buyurtmalarim"))
async def show_history(message: types.Message):
    await message.delete()
    histories = db.select_user_histories(user_id=message.from_user.id)

    text = "<b>Sizning buyurmalar tarxingiz</b>\n\n"
    
    for i in histories:
        text += f"Buyurtma vaqti: {i[1]}\nStatus: {i[2]}\n\n"

    await message.answer(text, reply_markup=back_button)


@dp.callback_query_handler(back_callback.filter())
async def hendler_back_buttons(call: types.CallbackQuery, callback_data:dict):
    category_id = int(callback_data['category_id'])
    subcategory_id = int(callback_data['subcategory_id'])

    if category_id == 0 and subcategory_id == 0 :
        await call.message.delete()

    elif category_id != 0:
        subcategories = db.select_subcategories(category_id=str(category_id))

        button = await subcategories_keyboard(subcategories)

        await call.message.edit_text("Kategoriya tanlang ⬇️", reply_markup=button)

    elif subcategory_id != 0:
        products = db.select_products(sub_category_id=str(subcategory_id))
        subcat = db.select_subcategory(id=subcategory_id)

        button =  products_keyboard(products, category_id=subcat[2])

        await call.message.delete()
        await call.message.answer("Mahsulot tanlang ⬇️", reply_markup=button)