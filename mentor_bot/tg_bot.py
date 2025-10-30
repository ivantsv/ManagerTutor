import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from llm_agents.mentor_agent import MentorAgent
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

user_mentors: dict[int, MentorAgent] = {}

main_reply_keyboard_buttons = [
        ["🌿 Открыть меню", "🧹 Очистить память ментора"],
        ["❌ Закрыть меню"]
    ]
main_reply_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text=btn) for btn in row] for row in main_reply_keyboard_buttons],
    resize_keyboard=True
)

def get_or_create_mentor(user_id: int) -> MentorAgent:
    """Возвращает личного ментора пользователя, создаёт нового при необходимости"""
    if user_id not in user_mentors:
        user_mentors[user_id] = MentorAgent(os.getenv("MISTRAL_API_KEY"))
        logger.info(f"Создан новый ментор для пользователя {user_id}")
    return user_mentors[user_id]

@dp.message(Command("start"))
async def start_handler(message: Message):
    get_or_create_mentor(message.from_user.id)
    await message.answer(
        "Привет 🌿 Я ментор, который поможет мягко разобраться в ситуациях с командой.\n"
        "Опиши, пожалуйста, что случилось 👇",
        reply_markup=main_reply_keyboard
    )

@dp.message(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите нужное:", reply_markup=main_reply_keyboard)

@dp.message(F.text == "❌ Закрыть меню")
async def close_menu(message: Message):
    await message.answer("Меню закрыто.", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text == "🧹 Очистить память ментора")
async def clear_history(message: Message):
    mentor = get_or_create_mentor(message.from_user.id)
    mentor.clear_memory()
    await message.answer("Память ментора очищена.", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text == "🌿 Открыть меню")
async def show_inline_keyboard(message: Message):
    buttons = [[types.InlineKeyboardButton(
        text="🌐 Перейти на сайт",
        url="https://managertutor.streamlit.app/")
    ]]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Выберите то, что вам нужно", reply_markup=keyboard)

@dp.message()
async def situation_handler(message: Message):
    user_text = message.text.strip()

    await message.answer("Секунду, думаю над ответом 🍃...")

    mentor = get_or_create_mentor(message.from_user.id)

    response = None
    while True:
        try:
            response = mentor.answer(user_message=user_text)
            break
        except:
            continue

    await message.answer(response)

async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())