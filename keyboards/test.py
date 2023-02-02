from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


b1 = InlineKeyboardButton(text='Желтый', callback_data='color yellow')

kb_order = InlineKeyboardMarkup()

# add insert row
kb_order.add(b1)
