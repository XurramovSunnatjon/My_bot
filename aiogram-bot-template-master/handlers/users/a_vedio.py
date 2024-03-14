from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from states.vedio_state import admin_video
from loader import dp, db, bot
import sqlite3
from data.config import ADMINS
from aiogram.dispatcher import FSMContext


@dp.message_handler(Text('on_click'))
async def bot_s(message:types.Message):
    chat=str(message.from_user.id)
    if chat==str(ADMINS[0]):
        await message.answer('Video kodini kiriting: ')
        await admin_video.kodlarim.set()

@dp.message_handler(state=admin_video.kodlarim)
async def bot_s(message:types.Message,state:FSMContext):
    kod=message.text
    await state.update_data(
        {"kod":kod}
    )

    await message.answer('Video havolasini kiriting: ')
    await admin_video.next()

@dp.message_handler(state=admin_video.urllar)
async def bot_s(message:types.Message,state:FSMContext):
    url=message.text
    await state.update_data(
        {"url":url}
    )
    await message.answer("Video ma'lumotini kiriting: ")
    await admin_video.next()

@dp.message_handler(state=admin_video.malumotlar)
async def bot_s(message:types.Message,state:FSMContext):
    malumot=message.text
    await state.update_data(
        {"malumot":malumot}
    )
    data = await state.get_data()
    kod= data.get("kod")
    url= data.get("url")
    malumot=data.get("malumot")
    try:
        db.add_video(id=kod,url=url,malumot=malumot)
        await message.answer('Qaytadan komandani bosing')
    except  sqlite3.IntegrityError as err:
        await bot.send_message(chat_id=ADMINS[0], text=err)
        await message.answer('Qaytadan komandani bosing')


    await state.finish()

