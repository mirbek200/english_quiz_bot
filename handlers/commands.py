# import aiohttp
# from aiogram import types, Dispatcher
# from create_bot import dp, bot
# from key.buttons import main_menu
#
#
# async def start(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Привет! Проверим твои уровен по англискому', reply_markup=main_menu)
#
#
# def register_commands(dp : Dispatcher):
#     dp.register_message_handler(start, commands=['start'])