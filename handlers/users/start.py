from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.inline_menu import main_menu
from loader import dp, db, bot
ADMIN = 7186021574

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    chat_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    await bot.send_message(
        ADMIN,
        f"🆕 Yangi foydalanuvchi /start bosdi\n\n"
        f"👤 Ismi: {full_name}\n"
        f"🔗 Username: @{username}\n"
        f"🆔 ID: {chat_id}"
    )
    await db.create_user(chat_id)
    user_status = await db.user_info(chat_id)
    if not user_status:
        await message.answer(
            "Assalomu alaykum, Online Do'konga xush kelibsiz!\n\n"
            "Ro'yxatdan o'tish uchun /registration komndasini bosing."
        )
    else:
        category_list = await db.get_category()
        btn = main_menu(category_list)
        await message.answer(
            f"Bo'limlardan birini tanlang: ", reply_markup=btn
        )