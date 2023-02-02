from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from db import db, config
from keyboards import get_kb_admin_complete_order, get_kb_admin_colors, get_kb_admin_types, get_kb_admin_layer_highs, get_kb_admin_nozzle_widths, get_kb_admin_start
from keyboards import kb_client
from create_bot import bot


class ChangeConfig(StatesGroup):
    plastic_type = State()
    plastic_color = State()
    layer_high = State()
    nozzle_width = State()


async def admin_get_first_order(callback_query: types.CallbackQuery):
    order = await db.get_first_order()
    user_name = await db.get_user_by_id(int(order['user_id']))
    order_text = f'Заказал {user_name} \nТип пластика: {order["plastic_type"]} \nЦвет пластика: {order["plastic_color"]} \nВысота слоя: {order["layer_high"]} \nТолщина сопла: {order["nozzle_width"]}'
    await bot.send_document(callback_query.from_user.id, order['file_id'], caption=order_text,\
                            reply_markup=await get_kb_admin_complete_order())


#@dp.callback_query_handler(func=lambda callback: callback.data and callback.data.startswith('color'))
async def admin_callback_order_complete(callback_query: types.CallbackQuery):
    order = await db.get_first_order()
    await bot.answer_callback_query(callback_query.id)

    await db.delete_order_first()
    await bot.send_message(int(order['user_id']), f'Ваш заказ выполнен', reply_markup=kb_client)
    await bot.send_message(callback_query.from_user.id, f'Заказ завершен', reply_markup=kb_client)


#@dp.callback_query_handler(func=lambda callback: callback.data and callback.data.startswith('color'))
async def admin_callback_delete_plastic_color(callback_query: types.CallbackQuery):
    color = callback_query.data.split()[-1]
    await bot.answer_callback_query(callback_query.id)

    if color == 'new':
        await bot.send_message(callback_query.from_user.id, f'Введите новый цвет пластика', reply_markup=kb_client)
        await ChangeConfig.plastic_color.set()
        return

    await config.delete_plastic_color(color)
    await bot.send_message(callback_query.from_user.id, f'Цвет {color} удален')


#@dp.callback_query_handler(func=lambda callback: callback.data and callback.data.startswith('type'))
async def admin_callback_delete_plastic_type(callback_query: types.CallbackQuery):
    typ = callback_query.data.split()[-1]
    await bot.answer_callback_query(callback_query.id)

    if typ == 'new':
        await bot.send_message(callback_query.from_user.id, f'Введите новый тип пластика', reply_markup=kb_client)
        await ChangeConfig.plastic_type.set()
        return

    await config.delete_plastic_type(typ)
    await bot.send_message(callback_query.from_user.id, f'Тип {typ} удален')


#@dp.callback_query_handler(func=lambda callback: callback.data and callback.data.startswith('layer_high'))
async def admin_callback_delete_layer_highs(callback_query: types.CallbackQuery):
    layer_high = callback_query.data.split()[-1]
    await bot.answer_callback_query(callback_query.id)
    
    if layer_high == 'new':
        await bot.send_message(callback_query.from_user.id, f'Введите новую высоту слоя в мм', reply_markup=kb_client)
        await ChangeConfig.layer_high.set()
        return

    await config.delete_layer_high(layer_high)
    await bot.send_message(callback_query.from_user.id, f'Высота {layer_high} удален')


#@dp.callback_query_handler(func=lambda callback: callback.data and callback.data.startswith('nozzle_width'))
async def admin_callback_delete_nozzle_widths(callback_query: types.CallbackQuery):
    nozzle_width = callback_query.data.split()[-1]
    await bot.answer_callback_query(callback_query.id)
    
    if nozzle_width == 'new':
        await bot.send_message(callback_query.from_user.id, f'Введите новую толщину сопла в мм', reply_markup=kb_client)
        await ChangeConfig.nozzle_width.set()
        return

    await config.delete_nozzle_width(nozzle_width)
    await bot.send_message(callback_query.from_user.id, f'Ширина {nozzle_width} удален')


#@dp.callback_query_handler(func=lambda callback: callback.data and callback.data.startswith('admin'))
async def admin_callback_start(callback_query: types.CallbackQuery):
    value = callback_query.data.split()[-1]
    await bot.answer_callback_query(callback_query.id)
    if value == 'plastic_colors':
        await bot.send_message(callback_query.from_user.id, f'Выберите цвет пластика, который вы хотите удалить \
                               или нажмите кнопку добавить, что бы добавить новый цвет.', reply_markup=await get_kb_admin_colors())
    if value == 'plastic_types':
        await bot.send_message(callback_query.from_user.id, f'Выберите тип пластика, который вы хотите удалить \
                               или нажмите кнопку добавить, что бы добавить новый тип.', reply_markup=await get_kb_admin_types())
    if value == 'layer_highs':
        await bot.send_message(callback_query.from_user.id, f'Выберите высоту слоя, которую вы хотите удалить \
                               или нажмите кнопку добавить, что бы добавить новую высоту в мм.', reply_markup=await get_kb_admin_layer_highs())
    if value == 'nozzle_widths':
        await bot.send_message(callback_query.from_user.id, f'Выберите ширину сопла, которую вы хотите удалить \
                               или нажмите кнопку добавить, что бы добавить новую ширину в мм.', reply_markup=await get_kb_admin_nozzle_widths())
    if value == 'get_first_order':
        await admin_get_first_order(callback_query)
    

# @dp.message_handler(state='ChangeConfig.plastic_color')
async def admin_add_plastic_color(message: types.Message, state: FSMContext):
    message.text = message.text.lower()
    if message.text in config.get_values()['plastic_colors']:
        await message.reply('Такой цвет пластика уже есть', reply_markup=kb_client)
    else:
        await config.insert_plastic_color(message.text)
        await message.reply('Цвет пластика успешно добавлен', reply_markup=kb_client)

    await state.finish()


# @dp.message_handler(state='ChangeConfig.plastic_type')
async def admin_add_plastic_type(message: types.Message, state: FSMContext):
    message.text = message.text.lower()
    if message.text in config.get_values()['plastic_types']:
        await message.reply('Такой тип пластика уже есть', reply_markup=kb_client)
    else:
        await config.insert_plastic_type(message.text)
        await message.reply('Тип пластика успешно добавлен', reply_markup=kb_client)

    await state.finish()


# @dp.message_handler(state='ChangeConfig.plastic_color')
async def admin_add_layer_high(message: types.Message, state: FSMContext):
    message.text = message.text.lower()
    try:
        if float(message.text) in config.get_values()['layer_highs']:
            await message.reply('Такая высота слоя уже есть', reply_markup=kb_client)
        else:
            await config.insert_layer_high(float(message.text))
            await message.reply('Высота слоя успешно добавлена', reply_markup=kb_client)

        await state.finish()

    except Exception:
        await message.reply('Введите высоту слоя нецелым числом с точкой в виде разделителя.', reply_markup=kb_client)


# @dp.message_handler(state='ChangeConfig.plastic_color')
async def admin_add_nozzle_width(message: types.Message, state: FSMContext):
    message.text = message.text.lower()
    try:
        if float(message.text) in config.get_values()['nozzle_widths']:
            await message.reply('Такая толщина сопла уже есть', reply_markup=kb_client)
        else:
            await config.insert_nozzle_width(float(message.text))
            await message.reply('Толщина сопла успешно добавлена', reply_markup=kb_client)

        await state.finish()

    except Exception:
        await message.reply('Введите толщину сопла нецелым числом с точкой в виде разделителя.', reply_markup=kb_client)


# @dp.message_handler(state='*', commands='cancel')
async def admin_add_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return

    await state.finish()
    await message.reply('Добавление отменено', reply_markup=kb_client)


#@dp.message_handler(commands=['admin'])
async def admin_start(message: types.Message):
    await message.reply("Что вы хотите отредактировать?", reply_markup=await get_kb_admin_start())


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_add_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(admin_add_plastic_color, state=ChangeConfig.plastic_color)
    dp.register_message_handler(admin_add_plastic_type, state=ChangeConfig.plastic_type)
    dp.register_message_handler(admin_add_layer_high, state=ChangeConfig.layer_high)
    dp.register_message_handler(admin_add_nozzle_width, state=ChangeConfig.nozzle_width)
    dp.register_callback_query_handler(admin_callback_order_complete, lambda callback: callback.data and callback.data.startswith('complete'))
    dp.register_callback_query_handler(admin_callback_delete_plastic_color, lambda callback: callback.data and callback.data.startswith('color'))
    dp.register_callback_query_handler(admin_callback_delete_plastic_type, lambda callback: callback.data and callback.data.startswith('type'))
    dp.register_callback_query_handler(admin_callback_delete_layer_highs, lambda callback: callback.data and callback.data.startswith('layer_high'))
    dp.register_callback_query_handler(admin_callback_delete_nozzle_widths, lambda callback: callback.data and callback.data.startswith('nozzle_width'))
    dp.register_callback_query_handler(admin_callback_start, lambda callback: callback.data and callback.data.startswith('admin'))
    dp.register_message_handler(admin_start, commands=['admin'])
