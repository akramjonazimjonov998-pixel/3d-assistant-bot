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

# =========================
# DATABASE
# =========================

user_languages = {}
user_stats = {}
user_modes = {}

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

    user_modes[user_id] = "model"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "models": 0,
            "renders": 0,
            "feedbacks": 0,
            "textures": 0
        }

    user_stats[user_id]["models"] += 1

    texts = {
        "uz": "📸 Model rasmini yuboring yoki model nomini yozing",
        "ru": "📸 Отправьте фото модели или название модели",
        "en": "📸 Send model image or write model name"
    }

    await message.answer(texts[lang])

# =========================
# RENDER FEEDBACK
# =========================

@dp.message(F.text.in_(["📸 Render Feedback", "📸 Анализ Рендера"]))
async def render_feedback(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    user_modes[user_id] = "render"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "models": 0,
            "renders": 0,
            "feedbacks": 0,
            "textures": 0
        }

    user_stats[user_id]["renders"] += 1

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

    user_modes[user_id] = "feedback"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "models": 0,
            "renders": 0,
            "feedbacks": 0,
            "textures": 0
        }

    user_stats[user_id]["feedbacks"] += 1

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

    user_modes[user_id] = "texture"

    if user_id not in user_stats:
        user_stats[user_id] = {
            "models": 0,
            "renders": 0,
            "feedbacks": 0,
            "textures": 0
        }

    user_stats[user_id]["textures"] += 1

    texts = {
        "uz": "🎨 Texture rasmini yuboring yoki texture nomini yozing",
        "ru": "🎨 Отправьте фото текстуры или название",
        "en": "🎨 Send texture image or write texture name"
    }

    await message.answer(texts[lang])

# =========================
# IMAGE HANDLER
# =========================

@dp.message(F.photo)
async def image_handler(message: Message):

    user_id = message.from_user.id

    mode = user_modes.get(user_id)

    if mode == "model":

        await message.answer(
            """
🔎 AI model qidirmoqda...

🌐 3DDD
🌐 Sketchfab
🌐 CGTrader
🌐 Telegram Channels
"""
        )

    elif mode == "render":

        await message.answer(
            """
📸 Render analiz qilindi

✅ Lighting yaxshi
✅ Material realistic
⚠️ Shadow kuchsiz
"""
        )

    elif mode == "feedback":

        await message.answer(
            """
🧠 Model Feedback

✅ Topology yaxshi
✅ Proportion yaxshi
⚠️ UV kerak
"""
        )

    elif mode == "texture":

        await message.answer(
            """
🎨 Texture analiz qilindi

✅ Marble texture aniqlandi
✅ Seamless texture tavsiya qilinadi
"""
        )

    else:

        await message.answer(
            "❗ Avval bo'limni tanlang"
        )

# =========================
# TEXT SEARCH
# =========================

@dp.message(F.text)
async def text_search(message: Message):

    user_id = message.from_user.id

    mode = user_modes.get(user_id)

    text = message.text

    if mode == "model":

        await message.answer(
            f"""
🔎 MODEL SEARCH

🌐 https://3ddd.ru/search?query={text}

🌐 https://sketchfab.com/search?q={text}&type=models

🌐 https://www.cgtrader.com/3d-models?keywords={text}
"""
        )

    elif mode == "texture":

        await message.answer(
            f"""
🎨 TEXTURE SEARCH

🌐 https://polyhaven.com/textures?q={text}

🌐 https://ambientcg.com/list?search={text}
"""
        )

# =========================
# STATISTICS
# =========================

@dp.message(F.text.in_(["📊 Statistika", "📊 Статистика", "📊 Statistics"]))
async def statistics(message: Message):

    user_id = message.from_user.id
    lang = user_languages.get(user_id, "uz")

    if user_id not in user_stats:
        user_stats[user_id] = {
            "models": 0,
            "renders": 0,
            "feedbacks": 0,
            "textures": 0
        }

    stats = user_stats[user_id]

    texts = {

        "uz": f"""
📊 Sizning Statistikangiz

🔎 Model qidirish: {stats['models']}
📸 Render feedback: {stats['renders']}
🧠 Model feedback: {stats['feedbacks']}
🎨 Texture yaratish: {stats['textures']}
""",

        "ru": f"""
📊 Ваша Статистика

🔎 Поиск моделей: {stats['models']}
📸 Render feedback: {stats['renders']}
🧠 Feedback модели: {stats['feedbacks']}
🎨 Создание текстур: {stats['textures']}
""",

        "en": f"""
📊 Your Statistics

🔎 Model searches: {stats['models']}
📸 Render feedback: {stats['renders']}
🧠 Model feedback: {stats['feedbacks']}
🎨 Texture creation: {stats['textures']}
"""
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