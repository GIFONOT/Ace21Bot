from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('Старт'))
main.add(KeyboardButton('Выход'))

game = ReplyKeyboardMarkup(resize_keyboard=True)
game.add('Всё', 'Ещё', 'Выход')



