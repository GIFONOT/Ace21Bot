import asyncio
import random
from random import randint
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup,\
    InlineKeyboardButton, BotCommand, \
    BotCommandScopeDefault
import os
from aiogram.dispatcher import FSMContext

from config import Card_deck, Masti
from keyboards import main, game

# Ининицилизация бота
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Переменные кастыли
global sumUser, sumAi
sumAi, sumUser = 0, 0
Card_deck_buf = Card_deck


class States:
    STARTED = 'started'


# Команды для пользователей
user_commands = [
    BotCommand("start", "Старт"),
    BotCommand("info", "Информация"),
]


async def set_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(user_commands,
                                 scope=BotCommandScopeDefault())


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name},'
                         f''f' сыграем?',
                         reply_markup=main)
    await state.set_state(States.STARTED)


@dp.message_handler(text='Выход', state=States.STARTED)
async def exit_game(message: types.Message, state: FSMContext):
    await message.answer(f'Пока {message.from_user.first_name}',
                         reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state()


@dp.message_handler()
async def handle_other_commands(message: types.Message):
    await message.answer('Я реагирую только на команду /start.')


@dp.message_handler(content_types=['sticker'], state=States.STARTED)
async def stic(message: types.Message):
    await message.answer(message.sticker.file_id)


@dp.message_handler(text='Старт', state=States.STARTED)
async def start_game(message: types.Message):
    global sumUser
    mast = randint(1, 4)
    rnd = random.choice(Card_deck_buf[mast])
    Card_deck_buf[mast].remove(rnd)

    sumUser += rnd

    await message.answer(f"Твои карты: {sumUser}", reply_markup=game)


@dp.message_handler(text='Ещё', state=States.STARTED)
async def start_game(message: types.Message):
    global sumUser
    mast = randint(1, 4)
    rnd = random.choice(Card_deck_buf[mast])
    Card_deck_buf[mast].remove(rnd)

    sumUser += rnd

    await message.answer(f"Твои карты: {sumUser}", reply_markup=game)


@dp.message_handler(text='Всё', state=States.STARTED)
async def start_game(message: types.Message):
    global sumUser, sumAi
    if randint(0, 100) > 51:
        sumAi = sumUser + 1
    else:
        sumAi = randint(10, 21)

    await message.answer(f"Твои карты: {sumUser}")
    await message.answer(f"Мои карты: {sumAi}")

    if sumUser > sumAi:
        await message.answer(f"Ты победил!")
    else:
        await message.answer(f"ты проебал)")
    sumUser = 0
    sumAi = 0
    Card_deck_buf = Card_deck


@dp.message_handler(state=States.STARTED)
async def errormessage(message: types.Message):
    #await message.answer(f"Нет такой команды {message.from_user.first_name}")
    pass


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_commands, skip_updates=True)
