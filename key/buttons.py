from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton

b1 = KeyboardButton('Начать тест')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(b1)