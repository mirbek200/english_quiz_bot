
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from key.buttons import main_menu
import handlers.quiz as quiz_test


class FSMChatGPT(StatesGroup):
    poll = State()
    question = 0
    ls = 0
    result = 0


async def cm_start(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Привет! Проверим твой уровень по английскому.')
    async with state.proxy() as data:
        data['ls'] = 0
        data['result'] = 0

    await show_poll(message, state)


async def show_poll(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ls = data['ls']

    if ls < len(quiz_test.quiz_test):
        question = quiz_test.quiz_test[ls]['question']
        options = quiz_test.quiz_test[ls]['options']

        poll_options = []
        for i, option in enumerate(options):
            button = types.InlineKeyboardButton(text=option, callback_data=f'answer_{i}')
            poll_options.append([button])

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=poll_options)

        await bot.send_message(message.from_user.id, question, reply_markup=reply_markup)

        async with state.proxy() as data:
            data['ls'] += 1

        await FSMChatGPT.poll.set()

    else:
        async with state.proxy() as data:
            result = data['result']
        await bot.send_message(message.from_user.id, f"Опрос завершен. {result}")
        await state.finish()


async def process_poll_answer(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        ls = data['ls']-1
        correct_answer = quiz_test.quiz_test[ls]['correct_answer']
        if str(correct_answer) == callback_query.data.replace("answer_", ""):
            data['result'] += 1
    await show_poll(callback_query, state)


def register_quiz(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['start'])
    dp.register_callback_query_handler(process_poll_answer, state=FSMChatGPT.poll)
