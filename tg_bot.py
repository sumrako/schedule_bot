from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from config import token
from main import get_schedule

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Расписание"))
async def get_fresh_news(message: types.Message):
    schedule = get_schedule()

    if len(schedule) >= 1:
        for k, v in sorted(schedule.items()):
            new = f"Сегодня у вас {v['title']} у {v['teacher']} в {v['time']}, место: {v['place']}"
            await message.answer(new)

    else:
        await message.answer("пу пуппу")

