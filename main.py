import asyncio
import random
from random import randint
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
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


def reset_card_deck():
    return Card_deck.copy()


async def reset_game_state(state: FSMContext):
    Card_deck_buf = reset_card_deck()
    await state.update_data(card_deck=Card_deck_buf, sumAi=0, sumUser=0)


async def get_card(message: types.Message, Card_deck_buf, sumUser, state: FSMContext):
    mast = random.randint(1, 4)
    rnd = random.choice(Card_deck_buf[mast])
    Card_deck_buf[mast].remove(rnd)
    sumUser += rnd

    await state.update_data(card_deck=Card_deck_buf, sumUser=sumUser)

    if sumUser == 21:
        await message.answer(f"Сумма твоих карт: {sumUser}", reply_markup=game)
        await message.answer(f"Ты победил!")

        await reset_game_state(state)

    elif sumUser > 21:
        await message.answer(f"Сумма твоих карт: {sumUser}", reply_markup=game)
        await message.answer(f"ты проебал)")

        await reset_game_state(state)
    else:
        await message.answer(f"Сумма твоих карт: {sumUser}\n{Masti[mast]}: {rnd}", reply_markup=game)
    print(len(Card_deck_buf[1]), len(Card_deck_buf[2]), len(Card_deck_buf[3]), len(Card_deck_buf[4]))


async def end_game(message: types.Message, sumUser, state: FSMContext):
    if random.randint(0, 100) > 51:
        sumAi = sumUser + 1
    else:
        sumAi = random.randint(10, 21)

    await message.answer(f"Сумма твоих карт: {sumUser}")
    await message.answer(f"Сумма моих карт: {sumAi}")

    if sumUser > sumAi:
        await message.answer(f"Ты победил!")
    else:
        await message.answer(f"ты проебал)")
    await reset_game_state(state)


async def start_ace(message: types.Message, Card_deck_buf, sumUser, state):
    mast = randint(1, 4)
    rnd = random.choice(Card_deck_buf[mast])
    Card_deck_buf[mast].remove(rnd)
    sumUser += rnd

    await state.update_data(card_deck=Card_deck_buf, sumUser=sumUser)

    await message.answer(f"Сумма твоих карт: {sumUser}\n{Masti[mast]}: {rnd}", reply_markup=game)


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


# Старт бота
@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name},'
                         f''f' сыграем?',
                         reply_markup=main)

    await reset_game_state(state)
    await state.set_state(States.STARTED)


# Команда выход
@dp.message_handler(text='Выход', state=States.STARTED)
async def exit_game(message: types.Message, state: FSMContext):
    await message.answer(f'Пока {message.from_user.first_name}',
                         reply_markup=types.ReplyKeyboardRemove())
    await state.reset_state()


# Обработка исключений
@dp.message_handler()
async def handle_other_commands(message: types.Message):
    await message.answer('Я реагирую только на команду /start.')


@dp.message_handler(content_types=['sticker'], state=States.STARTED)
async def stic(message: types.Message):
    await message.answer(message.sticker.file_id)


# Инициализация игры
@dp.message_handler(text='Старт', state=States.STARTED)
async def start_game(message: types.Message, state: FSMContext):
    data = await state.get_data()
    Card_deck_buf = data.get('card_deck')
    sumUser = data.get('sumUser')
    await start_ace(message, Card_deck_buf, sumUser, state)


# Обработка кнопок (ещё, всё)
@dp.message_handler(lambda message: message.text.lower() in ['ещё', 'всё'], state=States.STARTED)
async def handle_game_actions(message: types.Message, state: FSMContext):
    data = await state.get_data()
    Card_deck_buf = data.get('card_deck')
    sumUser = data.get('sumUser')

    if message.text.lower() == 'ещё':
        await get_card(message, Card_deck_buf, sumUser, state)

    elif message.text.lower() == 'всё':
        await end_game(message, sumUser, state)


# Обработка исключений
@dp.message_handler(state=States.STARTED)
async def errormessage(message: types.Message):
    await message.answer(f"Нет такой команды {message.from_user.first_name}")
    pass


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=set_commands, skip_updates=True)
