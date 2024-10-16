from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import config
from aiogram import Bot
from states import *
from text import *

router = Router()
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer("Введи команду /task")


import kb


@router.message(Command('task'))
async def cmd_task(msg: Message):
    await msg.answer("Введи текст задачи, а затем выбери время", reply_markup=kb.cancel_keyboard)


@router.message(Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите блюдо:",
        reply_markup=kb.make_row_keyboard(available_food_names)
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(OrderFood.choosing_food_name)


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=kb.make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)


@router.callback_query(lambda c: c.data == 'cancel_task')
async def cancel_task(callback_query: CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    await callback_query.answer("Задача отменена")