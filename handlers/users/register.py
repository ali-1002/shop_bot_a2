from aiogram.dispatcher import FSMContext
from aiogram.types import Message, Contact
from aiogram.dispatcher.filters import Command, RegexpCommandsFilter
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.menu import get_phone_number_btn
from keyboards.inline.inline_menu import main_menu
from loader import dp, db
from states.register_state import Register
import re

@dp.message_handler(Command('registration'), state=None)
async def start_register(msg: Message):
    chat_id = msg.from_user.id
    user_status = await db.user_info(chat_id)
    if not user_status:
        await msg.answer("Ro'yxatdan o'tishingiz uchun ism va familiyangizni kiriting: ")
        await Register.full_name.set()
    else:
        await msg.answer(f"Assalomu alaykum, Siz avval ro'yxatdan o'tgansiz!"
                         f"Ma'lumotlaringizni o'zgartirmoqchi bo'lsangiz /update bo'yrug'ini bosing!")



@dp.message_handler(state=Register.full_name)
async def register2(msg: Message, state: FSMContext):
    full_name = msg.text
    await state.update_data({'full_name': full_name})
    await msg.answer("Telefon raqamingizni jo'nating❗️", reply_markup=get_phone_number_btn)
    await Register.phone_number.set()

REGEXP_NUMBER = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

@dp.message_handler(content_types='contact', state=Register.phone_number)
async def end_register(msg: Message, state: FSMContext):
    chat_id = msg.from_user.id
    data = await state.get_data()
    full_name = data["full_name"]
    if msg.contact:
        phone_number = msg.contact.phone_number
    else:
        phone_number = msg.text.strip()
        if not re.match(REGEXP_NUMBER, phone_number):
            await msg.answer("Iltimos, to'g'ri telefon raqamini yuboring❗️")
            return
    category_list = await db.get_category()
    btn = main_menu(category_list)
    await db.update_user(full_name, phone_number, chat_id)
    await msg.answer("Ro'yxatdan muvoffaqqiyatli o'tdingiz", reply_markup=ReplyKeyboardRemove())
    await msg.answer(f"Bo'limlardan birini tanlang: ", reply_markup=btn)
    await state.finish()

