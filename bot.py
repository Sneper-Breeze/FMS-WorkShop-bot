from aiogram.utils import executor
from create_bot import dp
from handlers import client, other, order, admin


async def on_startup(_):
    print('Бот запущен')


client.register_handlers_client(dp)
order.register_handlers_order(dp)
admin.register_handlers_admin(dp)
#other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)