from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()
