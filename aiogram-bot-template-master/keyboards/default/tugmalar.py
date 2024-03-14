from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Videolarni izlash"),KeyboardButton(text="Audiolar izlash")]
    ],resize_keyboard=True
)