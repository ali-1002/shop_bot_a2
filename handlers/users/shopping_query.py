from aiogram.types import CallbackQuery, ShippingQuery
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from shopping_config.product_invoise import EXPRESS_SHIPPING, REGIONS_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING, generate_product_invoice

@dp.callback_query_handler(text='order')
async def send_product_invoice(call: CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    product_data = await state.get_data()
    if product_data:
        await bot.send_invoice(chat_id=chat_id, **generate_product_invoice(product_data).generate_invoice(), payload='shopbot')
    else:
        await call.answer("Savat bo'sh!")