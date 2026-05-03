from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_phone_number_btn = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Telfon raqam", request_contact=True)
    ],
],
    resize_keyboard=True
)
