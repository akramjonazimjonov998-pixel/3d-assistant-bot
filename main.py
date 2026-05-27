from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from aiogram.filters import CommandStart

import asyncio
import logging
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_languages = {}

# =========================
# LANGUAGE KEYBOARD
# =========================

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿 Uzbek"),
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇬🇧 English")
        ]
    ],
    resize_keyboard=True
)

# =========================
# MENUS
# =========================

menus = {

    "uz": ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔎 Model Izlash"),
                KeyboardButton(text="📸 Render Feedback")
            ],
            [
                KeyboardButton(text="🧠 Model Feedback"),
                KeyboardButton(text="🎨 Texture Yaratish")
            ],
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="💳 To'lov")
            ],
            [
                KeyboardButton(text="🌍 Tilni O'zgartirish")
            ]
        ],
        resize_keyboard=True
    ),

    "ru": ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔎 Поиск Моделей"),
                KeyboardButton(text="📸 Анализ Рендера")
            ],
            [
                KeyboardButton(text="🧠 Feedback Модели"),
                KeyboardButton(text="🎨 Создать Текстуру")
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="💳 Оплата")
            ],
            [
                KeyboardButton(text="🌍 Сменить Язык")
            ]
        ],
        resize_keyboard=True
    ),

    "en": ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔎 Find Models"),
                KeyboardButton(text="📸 Render Feedback")
            ],
            [
                KeyboardButton(text="🧠 Model Feedback"),
                KeyboardButton(text="🎨 Create Texture")
            ],
            [
                KeyboardButton(text="📊 Statistics"),
                KeyboardButton(text="💳 Payment")
            ],
            [
                KeyboardButton(text="🌍 Change Language")
            ]
        ],
        resize_keyboard=True
    )
}

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start_handler(message: Message):

    await message.answer(
        "🌍 Tilni tanlang / Выберите язык / Choose language",
        reply_markup=language_keyboard
    )

# =========================
# LANGUAGE SELECT
# =========================

@dp.message(F.text.in_(["🇺🇿 Uzbek", "🇷🇺 Русский", "🇬🇧 English"]))
async def language_handler(message: Message):

    user_id = message.from_user.id

    if message.text == "🇺🇿 Uzbek":

        user_languages[user_id] = "uz"

        await message.answer(
            """
🔥 3D ASSISTANT AI

Yordamida:

• 3D model toping
• Render analiz qiling
• Texture yarating
• Professional feedback oling

👇 Kerakli bo'limni tanlang
""",
            reply_markup=menus["uz"]
        )

    elif message.text == "🇷🇺 Русский":

        user_languages[user_id] = "ru"

        await message.answer(
            """
🔥 3D ASSISTANT AI

С помощью:

• Найти 3D модели
• Анализировать рендер
• Создавать текстуры
• Получать feedback

👇 Выберите раздел
""",
            reply_markup=menus["ru"]
        )

    elif message.text == "🇬🇧 English":

        user_languages[user_id] = "en"

        await message.answer(
            """
🔥 3D ASSISTANT AI

With this bot you can:

• Find 3D models
• Analyze renders
• Create textures
• Get professional feedback

👇 Choose a section
""",
            reply_markup=menus["en"]
        )

# =========================
# CHANGE LANGUAGE
# =========================

@dp.message(F.text.in_([
    "🌍 Tilni O'zgartirish",
    "🌍 Сменить Язык",
    "🌍 Change Language"
]))
async def change_language(message: Message):

    await message.answer(
        "🌍 Tilni tanlang / Выберите язык / Choose language",
        reply_markup=language_keyboard
    )

# =========================
# PAYMENT
# =========================

@dp.message(F.text.in_(["💳 To'lov", "💳 Оплата", "💳 Payment"]))
async def payment_handler(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    payment_texts = {

        "uz": """
💳 OBUNA REJALARI

💎 Oddiy To'lov
━━━━━━━━━━━━━━━

1 Oy — 34.999 so'm
3 Oy — 95.000 so'm

👇 To'lov qilish uchun tugmani bosing
""",

        "ru": """
💳 ПЛАНЫ ПОДПИСКИ

💎 Обычная оплата
━━━━━━━━━━━━━━━

1 Месяц — 34.999 сум
3 Месяца — 95.000 сум

👇 Нажмите кнопку для оплаты
""",

        "en": """
💳 SUBSCRIPTION PLANS

💎 Standard Payment
━━━━━━━━━━━━━━━

1 Month — 34.999 UZS
3 Months — 95.000 UZS

👇 Press the payment button
"""
    }

    button_texts = {
        "uz": "💳 To'lov Qilish",
        "ru": "💳 Оплатить",
        "en": "💳 Pay Now"
    }

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_texts[lang],
                    web_app=WebAppInfo(
                        url="https://premium-jj9q6ofor-3-d-assistant-ai.vercel.app"
                    )
                )
            ]
        ]
    )

    await message.answer(
        payment_texts[lang],
        reply_markup=keyboard
    )

# =========================
# FIND MODELS
# =========================

@dp.message(F.text.in_(["🔎 Model Izlash", "🔎 Поиск Моделей", "🔎 Find Models"]))
async def find_models(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    texts = {
        "uz": "🔎 Model nomini yuboring",
        "ru": "🔎 Отправьте название модели",
        "en": "🔎 Send model name"
    }

    await message.answer(texts[lang])

# =========================
# RENDER FEEDBACK
# =========================

@dp.message(F.text.in_(["📸 Render Feedback", "📸 Анализ Рендера"]))
async def render_feedback(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    texts = {
        "uz": "📸 Render rasmini yuboring",
        "ru": "📸 Отправьте render изображение",
        "en": "📸 Send your render image"
    }

    await message.answer(texts[lang])

# =========================
# MODEL FEEDBACK
# =========================

@dp.message(F.text.in_(["🧠 Model Feedback", "🧠 Feedback Модели"]))
async def model_feedback(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    texts = {
        "uz": "🧠 3D model screenshotlarini yuboring",
        "ru": "🧠 Отправьте скриншоты 3D модели",
        "en": "🧠 Send your 3D model screenshots"
    }

    await message.answer(texts[lang])

# =========================
# CREATE TEXTURE
# =========================

@dp.message(F.text.in_(["🎨 Texture Yaratish", "🎨 Создать Текстуру", "🎨 Create Texture"]))
async def create_texture(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    texts = {
        "uz": "🎨 Texture nomini yozing",
        "ru": "🎨 Напишите название текстуры",
        "en": "🎨 Describe texture"
    }

    await message.answer(texts[lang])

# =========================
# STATISTICS
# =========================

@dp.message(F.text.in_(["📊 Statistika", "📊 Статистика", "📊 Statistics"]))
async def statistics(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    texts = {
        "uz": "📊 Bot statistikasi\n\n👥 Users: 24K\n💎 Premium: 2.1K",
        "ru": "📊 Статистика бота\n\n👥 Пользователи: 24K\n💎 Premium: 2.1K",
        "en": "📊 Bot statistics\n\n👥 Users: 24K\n💎 Premium: 2.1K"
    }

    await message.answer(texts[lang])

# =========================
# MAIN
# =========================

async def main():

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())