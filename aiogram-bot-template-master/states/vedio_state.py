from aiogram.dispatcher.filters.state import State,StatesGroup

class videos(StatesGroup):
    video=State()
class admin_video(StatesGroup):
    kodlarim=State()
    urllar=State()
    malumotlar=State()