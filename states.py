from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class UserTask(StatesGroup):
    chosen_task = State()
    chosen_time = State()
