from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer("Привет я бот который поможет с заметками!")


from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder, InlineKeyboardMarkup


@router.message(Command('task'))
async def new_task_handler(msg: Message):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_task")]
    ])

    await msg.answer("Введи текст задачи, а затем выбери время", reply_markup=keyboard)

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой id: {msg.from_user.id}")
