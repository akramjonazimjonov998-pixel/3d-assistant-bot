import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from aiogram.filters import CommandStart
from dotenv import load_dotenv


# ENV
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# BOT
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# USER LANGUAGES
user_languages = {}


# LANGUAGE MENU
language_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 Uzbek")],
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇺🇸 English")]
    ],
    resize_keyboard=True
)


# MAIN MENU
def get_menu():

    return ReplyKeyboardMarkup(
        keyboard=[

            [KeyboardButton(text="🔍 Model Izlash")],

            [KeyboardButton(text="📸 Render Feedback"),
             KeyboardButton(text="🧠 Model Feedback")],

            [KeyboardButton(text="🎨 Texture Yaratish")],

            [KeyboardButton(text="📊 Statistika"),
             KeyboardButton(text="💳 To'lov")],

            [KeyboardButton(text="🌍 Tilni O'zgartirish")],

            [KeyboardButton(text="📚 Qo'llanma")]

        ],
        resize_keyboard=True
    )


# START
@dp.message(CommandStart())
async def start_handler(message: Message):

    await message.answer(
        "🌍 Tilni tanlang",
        reply_markup=language_menu
    )


# UZBEK LANGUAGE
@dp.message(lambda message: message.text == "🇺🇿 Uzbek")
async def uzbek_language(message: Message):

    user_languages[message.from_user.id] = "uz"

    await message.answer(

        "🔥 3D ASSISTANT AI\n\n"

        "• 3D model toping\n"
        "• Render analiz qiling\n"
        "• Texture yarating\n"
        "• Professional feedback oling",

        reply_markup=get_menu()
    )


# RUSSIAN LANGUAGE
@dp.message(lambda message: message.text == "🇷🇺 Русский")
async def russian_language(message: Message):

    await message.answer(

        "🔥 3D ASSISTANT AI\n\n"

        "• Поиск 3D моделей\n"
        "• Анализ рендера\n"
        "• Создание текстур\n"
        "• Professional feedback",

        reply_markup=get_menu()
    )


# ENGLISH LANGUAGE
@dp.message(lambda message: message.text == "🇺🇸 English")
async def english_language(message: Message):

    await message.answer(

        "🔥 3D ASSISTANT AI\n\n"

        "• Find 3D models\n"
        "• Analyze renders\n"
        "• Generate textures\n"
        "• Professional feedback",

        reply_markup=get_menu()
    )


# MODEL SEARCH
@dp.message(lambda message:
            message.text == "🔍 Model Izlash")
async def model_search(message: Message):

    await message.answer(
        "📸 Model rasmini yuboring."
    )


# RENDER FEEDBACK
@dp.message(lambda message:
            message.text == "📸 Render Feedback")
async def render_feedback(message: Message):

    await message.answer(
        "🖼 Render rasmini yuboring."
    )


# MODEL FEEDBACK
@dp.message(lambda message:
            message.text == "🧠 Model Feedback")
async def model_feedback(message: Message):

    await message.answer(
        "📸 Model rasmini yuboring."
    )


# TEXTURE
@dp.message(lambda message:
            message.text == "🎨 Texture Yaratish")
async def texture(message: Message):

    await message.answer(

        "✍️ Referens yoki texture nomini yozing.\n\n"

        "Misol:\n"
        "White Marble Texture"
    )


# STATISTICS
@dp.message(lambda message:
            message.text == "📊 Statistika")
async def statistics(message: Message):

    await message.answer(

        "📊 Sizning Statistikangiz\n\n"

        "🔍 Model Search: 0\n"
        "📸 Render Feedback: 0\n"
        "🧠 Model Feedback: 0\n"
        "🎨 Texture Generation: 0\n\n"

        "💎 Obuna: Bepul Reja"
    )


# PAYMENT
@dp.message(lambda message:
            message.text == "💳 To'lov")
async def payment(message: Message):

    payment_button = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="💳 To'lov Qilish",

                    web_app=WebAppInfo(
                        url="https://v0-3d-assistant-ai.vercel.app/"
                    )
                )
            ]

        ]
    )

    await message.answer(

        "💳 OBUNA REJALARI\n\n"

        "💎 Oddiy To'lov\n"
        "━━━━━━━━━━━\n"
        "1 Oy — 34.999 so'm\n"
        "3 Oy — 95.000 so'm\n\n"

        "👇 To'lov qilish uchun tugmani bosing",

        reply_markup=payment_button
    )


# GUIDE
@dp.message(lambda message:
            message.text == "📚 Qo'llanma")
async def guide(message: Message):

    await message.answer(

        "📚 QO'LLANMA\n\n"

        "1️⃣ Kerakli bo'limni tanlang\n"
        "2️⃣ Rasm yoki prompt yuboring\n"
        "3️⃣ AI sizga yordam beradi"
    )


# CHANGE LANGUAGE
@dp.message(lambda message:
            message.text == "🌍 Tilni O'zgartirish")
async def change_language(message: Message):

    await message.answer(
        "🌍 Tilni tanlang",
        reply_markup=language_menu
    )


# MAIN
async def main():

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())