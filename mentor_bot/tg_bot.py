import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from mentor_core import generate_response
from config import BOT_TOKEN

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Привет 🌿 Я ментор, который поможет мягко разобраться в ситуациях с командой.\n"
        "Опиши, пожалуйста, что случилось 👇"
    )


@dp.message()
async def situation_handler(message: Message):
    user_text = message.text.strip()

    await message.answer("Секунду, думаю над ответом 🍃...")

    #!!!!!!!!!!!!!!!!
    response = generate_response(user_text) # заглушка для будущего аи ответа
    #!!!!!!!!!!!!!!!!

    await message.answer(response)


async def main():
    print("🤖 Ментор-бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())