from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'go'])
async def echo(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}, сыграем?')


@dp.message_handler()
async def errormessage(message: types.Message):
    await message.answer(f"Нет такой команды {message.from_user.first_name}")

if __name__ == '__main__':
    executor.start_polling(dp)





