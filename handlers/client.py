from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from db import db
from keyboards import kb_client


class Registration(StatesGroup):
    user_id = None
    first_name = State()
    last_name = State()


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Hello', reply_markup=kb_client)
        await message.delete()
    except:
        await bot.reply(f'Общение с ботом только через ЛС, напишите ему: {"link"}')


# @dp.message_handler(commands=['joke'])
async def command_joke(message: types.Message):
    try:
        if not await db.is_registered(message.from_id):
            await bot.send_message(message.from_user.id, 'для общения с ботом нужно пройти регистрацию, \
                                                          для регистрации введите /register', reply_markup=kb_client)
        else:
            await bot.send_message(message.from_user.id, 'колобок повесился', reply_markup=kb_client)
        await message.delete()
    except:
        await bot.reply(f'Общение с ботом только через ЛС, напишите ему: {"link"}')


# @dp.message_handler(commands=['register'], state=none)
async def cm_register(message: types.Message, state: FSMContext):
    try:
        if await db.is_registered(message.from_user.id):
            await bot.send_message(message.from_user.id, 'вы уже зарегистрированы')
        else:
            await Registration.first_name.set()
            await message.reply('Введите имя')
    except:
        await bot.reply(f'Общение с ботом только через ЛС, напишите ему: {"link"}')


# @dp.message_handler(commands=['register'], state=Registration.first_name)
async def load_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_id
        data['first_name'] = message.text

    await Registration.next()
    await message.reply('Введите фамилию')


# @dp.message_handler(commands=['register'], state=Registration.last_name)
async def load_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

        await db.insert_user({"user_id": data["user_id"], \
                        "first_name": data["first_name"], \
                        "last_name": data["last_name"]})
    await message.reply('Вы успешно зарегестрированы')

    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_joke, commands=['joke'])
    dp.register_message_handler(cm_register, commands=['register'], state=None)
    dp.register_message_handler(load_first_name, state=Registration.first_name)
    dp.register_message_handler(load_last_name, state=Registration.last_name)
