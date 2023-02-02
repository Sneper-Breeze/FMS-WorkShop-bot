from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/register')
b2 = KeyboardButton('/joke')
b3 = KeyboardButton('/order')
b4 = KeyboardButton('/cancel')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# add insert row
kb_client.row(b1, b2).row(b3, b4)
