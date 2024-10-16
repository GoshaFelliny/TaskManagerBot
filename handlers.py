from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import config
from aiogram import Bot

router = Router()
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer("Привет я бот который поможет с заметками")


import kb


@router.message(Command('task'))
async def new_task_handler(msg: Message):
    await msg.answer("Введи текст задачи, а затем выбери время", reply_markup=kb.cancel_keyboard)


@router.callback_query(lambda c: c.data == 'cancel_task')
async def cancel_task(callback_query: CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    await callback_query.answer("Задача отменена")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой id: {msg.from_user.id}")
