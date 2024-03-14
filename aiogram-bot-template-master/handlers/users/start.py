from aiogram import types
import sqlite3
from data.config import ADMINS
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from keyboards.default.tugmalar import menu
from states.vedio_state import videos
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loader import dp,db,bot



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,
                    name=name)
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\nXush kelibsiz botdan foydalanish uchun pastdagi tugmalardan foydalaning",reply_markup=menu)
    count = db.count_users()[0]
    msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)

@dp.message_handler(Text('Videolarni izlash'))
async def bot_video(message:types.Message):
    await message.answer("Video ko'dini kiriting",reply_markup=ReplyKeyboardRemove())
    await videos.video.set()

@dp.message_handler(state=videos.video)
async def video(message: types.Message,state:FSMContext):
    a=message.text
    kods = db.select_all_videos()
    for kod in kods:
        if kod[0]==a:
            await message.answer_video(kod[1],caption=kod[2])
    await message.answer('Tugmani bosib qaytadan qidiring',reply_markup=menu)
    await state.finish()
