from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import asyncio
import logging
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# =========================
# LANGUAGES
# =========================

user_languages = {}

texts = {

    "uz": {

        "welcome":
"""🔥 <b>3D ASSISTANT AI</b>

Yordamida:

• 3D model toping
• Render analiz qiling
• Texture yarating
• Professional feedback oling

👇 Kerakli bo'limni tanlang""",

        "payment_text":
"""💳 <b>OBUNA REJALARI</b>

💎 Oddiy To'lov
━━━━━━━━━━━━━━

1 Oy — 34.999 so'm
3 Oy — 95.000 so'm

👇 To'lov qilish uchun tugmani bosing""",

        "payment_button": "💳 To'lov Qilish",

        "model_search": "🔎 Model Izlash",
        "render_feedback": "📸 Render Feedback",
        "model_feedback": "🧠 Model Feedback",
        "texture": "🎨 Texture Yaratish",
        "stats": "📊 Statistika",
        "payment": "💳 To'lov"
    },

    "ru": {

        "welcome":
"""🔥 <b>3D ASSISTANT AI</b>

С помощью:

• Найти 3D модели
• Анализировать рендер
• Создавать текстуры
• Получить профессиональный feedback

👇 Выберите нужный раздел""",

        "payment_text":
"""💳 <b>ТАРИФЫ ПОДПИСКИ</b>

💎 Обычная оплата
━━━━━━━━━━━━━━

1 Месяц — 34.999 сум
3 Месяца — 95.000 сум

👇 Нажмите кнопку для оплаты""",

        "payment_button": "💳 Оплатить",

        "model_search": "🔎 Поиск Модели",
        "render_feedback": "📸 Анализ Рендера",
        "model_feedback": "🧠 Анализ Модели",
        "texture": "🎨 Создать Текстуру",
        "stats": "📊 Статистика",
        "payment": "💳 Оплата"
    },

    "en": {

        "welcome":
"""🔥 <b>3D ASSISTANT AI</b>

With this bot you can:

• Find 3D models
• Analyze renders
• Create textures
• Get professional feedback

👇 Choose a section below""",

        "payment_text":
"""💳 <b>SUBSCRIPTION PLANS</b>

💎 Standard Payment
━━━━━━━━━━━━━━

1 Month — 34.999 uzs
3 Months — 95.000 uzs

👇 Click the button below to pay""",

        "payment_button": "💳 Pay Now",

        "model_search": "🔎 Model Search",
        "render_feedback": "📸 Render Feedback",
        "model_feedback": "🧠 Model Feedback",
        "texture": "🎨 Create Texture",
        "stats": "📊 Statistics",
        "payment": "💳 Payment"
    }
}


# =========================
# KEYBOARD
# =========================

def get_main_keyboard(lang):

    return ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(text=texts[lang]["model_search"])
            ],

            [
                KeyboardButton(text=texts[lang]["render_feedback"]),
                KeyboardButton(text=texts[lang]["model_feedback"])
            ],

            [
                KeyboardButton(text=texts[lang]["texture"])
            ],

            [
                KeyboardButton(text=texts[lang]["stats"]),
                KeyboardButton(text=texts[lang]["payment"])
            ]
        ],
        resize_keyboard=True
    )


# =========================
# START
# =========================

@dp.message(F.text == "/start")
async def start(message: Message):

    language_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇺🇿 Uzbek"),
                KeyboardButton(text="🇷🇺 Русский"),
                KeyboardButton(text="🇺🇸 English")
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🌍 Tilni tanlang / Выберите язык / Choose language",
        reply_markup=language_keyboard
    )


# =========================
# UZBEK
# =========================

@dp.message(F.text == "🇺🇿 Uzbek")
async def uzbek_language(message: Message):

    user_languages[message.from_user.id] = "uz"

    await message.answer(
        texts["uz"]["welcome"],
        reply_markup=get_main_keyboard("uz")
    )


# =========================
# RUSSIAN
# =========================

@dp.message(F.text == "🇷🇺 Русский")
async def russian_language(message: Message):

    user_languages[message.from_user.id] = "ru"

    await message.answer(
        texts["ru"]["welcome"],
        reply_markup=get_main_keyboard("ru")
    )


# =========================
# ENGLISH
# =========================

@dp.message(F.text == "🇺🇸 English")
async def english_language(message: Message):

    user_languages[message.from_user.id] = "en"

    await message.answer(
        texts["en"]["welcome"],
        reply_markup=get_main_keyboard("en")
    )


# =========================
# PAYMENT
# =========================

@dp.message(F.text.in_([
    "💳 To'lov",
    "💳 Оплата",
    "💳 Payment"
]))
async def payment(message: Message):

    lang = user_languages.get(message.from_user.id, "uz")

    payment_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=texts[lang]["payment_button"]
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        texts[lang]["payment_text"],
        reply_markup=payment_keyboard
    )


# =========================
# MAIN
# =========================

async def main():

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())