from aiogram.types import CallbackQuery
from loader import db, dp
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_menu import main_menu

@dp.callback_query_handler(text='clear_product')
async def clear_product(call: CallbackQuery, state: FSMContext):
    await state.update_data(cart={})
    await state.finish()
    category_list = await db.get_category()
    btn = main_menu(category_list)
    await call.message.edit_text("Bo'limlardan birini tanlang:", reply_markup=btn)
    await call.answer("Savat bo'shlandi!")
