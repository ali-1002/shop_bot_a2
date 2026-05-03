from aiogram.dispatcher import FSMContext
from aiogram.types import ShippingQuery, PreCheckoutQuery
from loader import dp, bot, db
from shopping_config.product_invoise import EXPRESS_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING, REGIONS_SHIPPING
from aiogram.types import ContentType
from aiogram import types
from aiogram.types import Message


@dp.shipping_query_handler()
async def choose_shipping(query: ShippingQuery):
    if query.shipping_address.country_code != 'UZ':
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                         ok=True,
                                         error_message="Yetkazib berish xizmati faqat O'zbekiston bo'ylab")
    elif query.shipping_address.city.lower() in ['toshkent', 'tashkent', 'Ташкент', 'Тошкент']:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[EXPRESS_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)

    elif query.shipping_address.city.lower() not in ['toshkent', 'tashkent', 'Ташкент', 'Тошкент']:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[REGIONS_SHIPPING],
                                        ok=True)

@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Test ko'rinishidagi to'lov tugallandi")
    await bot.send_message(chat_id=pre_checkout_query.from_user.id, text="Xaridingiz uchun raxmat 😊")
    data = await state.get_data()
    chat_id = pre_checkout_query.from_user.id
    customer_full_name = await db.user_info(chat_id=chat_id)
    created_order = await db.create_order(customer_full_name)
    order_id = created_order
    data_order_item = [
        (
            product,
            data[product]['quantity'],
            int(float(data[product]['price'])),
            data[product]['total'],
            order_id
        )
        for product in data
    ]
    await db.create_order_item(data_order_item)
    await state.finish()


# @dp.pre_checkout_query_handler(lambda query: True)
# async def checkout(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#     data = await state.get_data()
#     print(data)
#     chat_id = pre_checkout_query.from_user.id
#     customer_full_name = await db.user_info(chat_id=chat_id)
#     order_id = await db.create_order(customer_full_name)
#     cart = data.get('cart', {})
#     print(cart)
#     data_order_item = [
#         (
#             product,
#             cart[product]['quantity'],
#             int(float(cart[product]['price'])),
#             cart[product]['total'],
#             order_id
#         )
#         for product in cart
#     ]
#     await db.create_order_item(data_order_item)
#     await state.finish()