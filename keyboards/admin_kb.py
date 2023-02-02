from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import config


#--------buttons admin-----------
async def get_kb_admin_start():
	buttons_admin = [InlineKeyboardButton(text=value, callback_data=f'admin {value}') for value in config.get_values()]
	kb_admin_start = InlineKeyboardMarkup(row_width=2)
	kb_admin_start.add(*buttons_admin)
	kb_admin_start.add(InlineKeyboardButton(text='Первый заказ в очереди', callback_data=f'admin get_first_order'))

	return kb_admin_start
#---------------------------------

#---------buttons color-----------
async def get_kb_admin_colors():
	buttons_color = [InlineKeyboardButton(text=value, callback_data=f'color {value}') for value in config.get_values()['plastic_colors']]
	kb_admin_colors = InlineKeyboardMarkup(row_width=3)

	kb_admin_colors.add(*buttons_color)
	return kb_admin_colors.add(InlineKeyboardButton(text='Добавить значение', callback_data=f'color new'))
#---------------------------------

#---------buttons type------------
async def get_kb_admin_types():
	buttons_type = [InlineKeyboardButton(text=value, callback_data=f'type {value}') for value in config.get_values()['plastic_types']]
	kb_admin_types = InlineKeyboardMarkup(row_width=3)

	kb_admin_types.add(*buttons_type)
	return kb_admin_types.add(InlineKeyboardButton(text='Добавить значение', callback_data=f'type new'))
#---------------------------------

#-------buttons layer highs--------
async def get_kb_admin_layer_highs():
	buttons_layer_high = [InlineKeyboardButton(text=value, callback_data=f'layer_high {value}') for value in config.get_values()['layer_highs']]
	kb_admin_layer_highs = InlineKeyboardMarkup(row_width=3)

	kb_admin_layer_highs.add(*buttons_layer_high)
	return kb_admin_layer_highs.add(InlineKeyboardButton(text='Добавить значение', callback_data=f'layer_high new'))
#---------------------------------

#------buttons nozzle width-------
async def get_kb_admin_nozzle_widths():
	buttons_nozzle_width = [InlineKeyboardButton(text=value, callback_data=f'nozzle_width {value}') for value in config.get_values()['nozzle_widths']]
	kb_admin_nozzle_widths = InlineKeyboardMarkup(row_width=3)

	kb_admin_nozzle_widths.add(*buttons_nozzle_width)
	return kb_admin_nozzle_widths.add(InlineKeyboardButton(text='Добавить значение', callback_data=f'nozzle_width new'))
#---------------------------------

#------button complete order------
async def get_kb_admin_complete_order():
	button_complete_order = InlineKeyboardButton(text='Удалить заказ из очереди', callback_data=f'complete')
	kb_admin_complete_order = InlineKeyboardMarkup()

	kb_admin_complete_order.add(button_complete_order)
	return kb_admin_complete_order
#---------------------------------
