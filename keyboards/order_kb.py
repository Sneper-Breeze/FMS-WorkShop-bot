from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db import config
# add insert row


#---------buttons color-----------
async def get_kb_order_colors():
	buttons_color = [KeyboardButton(color) for color in config.get_values()['plastic_colors']]
	kb_order_colors = ReplyKeyboardMarkup(resize_keyboard=True)

	return kb_order_colors.row(*buttons_color)
#---------------------------------


#---------buttons type------------
async def get_kb_order_types():
	buttons_type = [KeyboardButton(tyype) for tyype in config.get_values()['plastic_types']]
	kb_order_types = ReplyKeyboardMarkup(resize_keyboard=True)

	return kb_order_types.row(*buttons_type)
#---------------------------------

#-------buttons layer highs-------
async def get_kb_order_layer_highs():
	buttons_layer_high = [KeyboardButton(high) for high in config.get_values()['layer_highs']]
	kb_order_layer_highs = ReplyKeyboardMarkup(resize_keyboard=True)

	return kb_order_layer_highs.row(*buttons_layer_high)
#---------------------------------

#------buttons nozzle width-------
async def get_kb_order_nozzle_widths():
	buttons_nozzle_width = [KeyboardButton(width) for width in config.get_values()['nozzle_widths']]
	kb_order_nozzle_widths = ReplyKeyboardMarkup(resize_keyboard=True)

	return kb_order_nozzle_widths.row(*buttons_nozzle_width)
#---------------------------------

