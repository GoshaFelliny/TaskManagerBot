from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import config
from aiogram import Bot
from states import *
from text import *
import kb
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import pytz

router = Router()
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
scheduler = AsyncIOScheduler()


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(start_text)


@router.message(StateFilter(None), Command('task'))
async def cmd_task(msg: Message, state: FSMContext):
    await msg.answer(text=chosen_task_text,
                     reply_markup=kb.cancel_keyboard)

    await state.set_state(UserTask.chosen_task)


@router.message(UserTask.chosen_task, F.text)
async def chosen_task(message: Message, state: FSMContext):
    await state.update_data(chosen_task=message.text)
    await message.answer(
        text=chosen_time_text
    )
    await state.set_state(UserTask.chosen_time)


async def send_scheduled_message(chat_id: int, task:str):
    await bot.send_message(chat_id, f"Напоминание: {task}")


@router.message(UserTask.chosen_time, F.text)
async def chosen_time(message: Message, state: FSMContext):
    await state.update_data(chosen_time=message.text)
    user_data = await state.get_data()

    try:
        await message.answer(
            text=f"Уведомление поставлено на {user_data['chosen_time']}"
        )

        local_timezone = pytz.timezone('Europe/Moscow')
        now = datetime.now(local_timezone)

        h, m = map(int, user_data['chosen_time'].split(':'))

        scheduled_time = local_timezone.localize(datetime(now.year, now.month, now.day, h, m))

        if scheduled_time < now:
            scheduled_time += timedelta(days=1)

        trigger = DateTrigger(run_date=scheduled_time)

        scheduler.add_job(send_scheduled_message, trigger, args=[message.chat.id, f"{user_data['chosen_task']}"], )
        scheduler.start()
        await state.clear()

    except ValueError:
        await message.answer(text=warning_time_text)
        await state.clear()


@router.callback_query(lambda c: c.data == 'cancel_task')
async def cancel_task(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await state.clear()

