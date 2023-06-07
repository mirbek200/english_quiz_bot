
from create_bot import dp
from aiogram.utils import executor
from handlers import commands, user

# commands.register_commands(dp)
user.register_quiz(dp)
executor.start_polling(dp, skip_updates=True)