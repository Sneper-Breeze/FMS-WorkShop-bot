from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp
from db import db
from create_bot import bot
from keyboards import get_kb_order_colors, get_kb_order_types, get_kb_order_layer_highs, get_kb_order_nozzle_widths
from keyboards import kb_client
from db import config


class Order(StatesGroup):
    file = State()
    plastic_type = State()
    plastic_color = State()
    layer_high = State()
    nozzle_width = State()


# @dp.message_handler(commands='Загрузить', state=None)
async def order_start(message: types.Message, state: FSMContext):
    if not await db.is_registered(message.from_id):
        await bot.send_message(message.from_user.id, 'для общения с ботом нужно пройти регистрацию, \
                                                      для регистрации введите /register', reply_markup=kb_client)
        return

    await Order.file.set()
    await message.reply('Загрузите файл типа stl или obj')


# @dp.message_handler(content_types=['file'], state=Order.file)
async def order_file(message: types.Message, state: FSMContext):
    if message.document.file_name.split('.')[-1] not in ['stl', 'obj']:
        await message.reply('Неправильный формат файла \nЗагрузите файл типа stl или obj')
        return

    async with state.proxy() as data:
        data['file'] = message.document.file_id
        #await bot.send_document(message.chat.id, data['file'])
    await Order.next()
    await message.reply('Введите тип пластика из предложенных', reply_markup=await get_kb_order_types())


# @dp.message_handler(state=Order.name)
async def order_plastic_type(message: types.Message, state: FSMContext):
    if message.text not in config.get_values()['plastic_types']:
        await message.reply('Типы пластика указаны в кнопках', reply_markup=await get_kb_order_types())
        return

    async with state.proxy() as data:
        data['plastic_type'] = message.text
    await Order.next()
    await message.reply('Теперь введите цвет пластика', reply_markup=await get_kb_order_colors())


#@dp.message_handler(state=Order.price)
async def order_plastic_color(message: types.Message, state: FSMContext):
    if message.text not in config.get_values()['plastic_colors']:
        await message.reply('Цвета пластика указаны в кнопках', reply_markup=await get_kb_order_colors())
        return

    async with state.proxy() as data:
        data['plastic_color'] = message.text
    await Order.next()
    await message.reply('Теперь введите толщину слоя в мм', reply_markup=await get_kb_order_layer_highs())


# @dp.message_handler(state=Order.price)
async def order_layer_high(message: types.Message, state: FSMContext):
    try:
        if float(message.text) not in config.get_values()['layer_highs']:
            await message.reply('Высоты слоя указаны в кнопках', reply_markup=await get_kb_order_layer_highs())
            return
    except Exception:
        await message.reply('Высоты слоя указаны в кнопках', reply_markup=await get_kb_order_layer_highs())
        return

    async with state.proxy() as data:
        data['layer_high'] = float(message.text)
    await Order.next()
    await message.reply('И наконец, введите толщину сопла в мм', reply_markup=await get_kb_order_nozzle_widths())


# @dp.message_handler(state=Order.price)
async def order_nozzle_width(message: types.Message, state: FSMContext):
    try:
        if float(message.text) not in config.get_values()['nozzle_widths']:
            await message.reply('Ширины сопла указаны в кнопках', reply_markup=await get_kb_order_nozzle_widths())
            return
    except Exception:
        await message.reply('Ширины сопла указаны в кнопках', reply_markup=await get_kb_order_nozzle_widths())
        return

    async with state.proxy() as data:
        data['nozzle_width'] = float(message.text)
        await db.insert_order({"user_id": message.from_id, \
                        "plastic_type": data["plastic_type"], \
                        "plastic_color": data["plastic_color"], \
                        "layer_high": data["layer_high"], \
                        "nozzle_width": data["nozzle_width"], \
                        "file_id": data["file"]})
    
    await message.reply("Заказ успешно отправлен", reply_markup=kb_client)
    await state.finish()


# @dp.message_handler(state='*', commands='cancel')
async def order_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return

    await state.finish()
    await message.reply('Заказ отменён', reply_markup=kb_client)


def register_handlers_order(dp: Dispatcher):
    dp.register_message_handler(order_cancel, commands=['cancel'], state='*')
    dp.register_message_handler(order_start, commands=['order'], state=None)
    dp.register_message_handler(order_file, content_types=['document'], state=Order.file)
    dp.register_message_handler(order_plastic_type, state=Order.plastic_type)
    dp.register_message_handler(order_plastic_color, state=Order.plastic_color)
    dp.register_message_handler(order_layer_high, state=Order.layer_high)
    dp.register_message_handler(order_nozzle_width, state=Order.nozzle_width)
