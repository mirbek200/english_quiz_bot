
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from key.buttons import main_menu
import handlers.quiz as quiz


class FSMChatGPT(StatesGroup):
    start = State()
    poll = State()
    question = 0
    ls = 0


async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Проверим твои уровен по англискому')
    await FSMChatGPT.start.set()


async def cm_start(message: types.Message, state=FSMChatGPT):
    state = FSMChatGPT()
    poll = types.Poll(
        type=types.PollType.REGULAR,
        question=quiz.quiz_test[state.ls]["question"],
        options=quiz.quiz_test[state.ls]["options"],
    )
    await bot.send_poll(message.chat.id, poll.question, poll.options)
    await FSMChatGPT.poll.set()


async def process_poll_answer(poll_answer: types.PollAnswer, state=FSMChatGPT):
    user_id = poll_answer.user.id
    selected_option = poll_answer.option_ids[0]
    await bot.send_message(user_id, f"Вы выбрали опцию {selected_option}")
    await state.start.set()


def register_quiz(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(cm_start, state=FSMChatGPT.start)
    dp.register_message_handler(process_poll_answer, state=FSMChatGPT.poll)
