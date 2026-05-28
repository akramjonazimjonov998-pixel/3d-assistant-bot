from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile
)
from aiogram.filters import CommandStart

from telethon import TelegramClient
from openai import OpenAI

import asyncio
import logging
import os

# =========================
# TOKENS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# =========================
# CLIENTS
# =========================

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

client = OpenAI(
    api_key=OPENAI_API_KEY
)

tg_client = TelegramClient(
    "session",
    API_ID,
    API_HASH
)

# =========================
# DATABASE
# =========================

user_modes = {}
user_languages = {}
stats = {
    "users": 0,
    "searches": 0,
    "downloads": 0,
    "textures": 0
}

# =========================
# CHANNELS
# =========================

FREE_CHANNELS = [
    "free3dsky",
    "Free3dmodels",
    "free_3dsky",
    "FREE_3DSMAX_MODELS"
]

# =========================
# KEYBOARD
# =========================

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔎 Model Izlash")],
        [KeyboardButton(text="🎨 Texture Yaratish")],
        [KeyboardButton(text="📸 Render Feedback")],
        [KeyboardButton(text="🧠 Model Feedback")],
        [KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="🌍 Tilni O‘zgartirish")]
    ],
    resize_keyboard=True
)

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    stats["users"] += 1

    await message.answer(
        """
🔥 3D ASSISTANT AI

Kerakli bo‘limni tanlang 👇
""",
        reply_markup=main_keyboard
    )

# =========================
# MODES
# =========================

@dp.message(F.text == "🔎 Model Izlash")
async def model_mode(message: Message):

    user_modes[message.from_user.id] = "model"

    await message.answer(
        "📸 Rasm yuboring yoki model nomini yozing"
    )

@dp.message(F.text == "🎨 Texture Yaratish")
async def texture_mode(message: Message):

    user_modes[message.from_user.id] = "texture"

    await message.answer(
        "🎨 Texture nomini yozing"
    )

@dp.message(F.text == "📸 Render Feedback")
async def render_mode(message: Message):

    user_modes[message.from_user.id] = "render"

    await message.answer(
        "📸 Render rasmini yuboring"
    )

@dp.message(F.text == "🧠 Model Feedback")
async def feedback_mode(message: Message):

    user_modes[message.from_user.id] = "feedback"

    await message.answer(
        "🧠 Model rasmini yuboring"
    )

# =========================
# STATISTICS
# =========================

@dp.message(F.text == "📊 Statistika")
async def statistics(message: Message):

    await message.answer(
        f"""
📊 BOT STATISTICS

👤 Users: {stats["users"]}
🔎 Searches: {stats["searches"]}
📦 Downloads: {stats["downloads"]}
🎨 Textures: {stats["textures"]}
"""
    )

# =========================
# LANGUAGE
# =========================

@dp.message(F.text == "🌍 Tilni O‘zgartirish")
async def language(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇿 Uzbek",
                    callback_data="lang_uz"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇷🇺 Русский",
                    callback_data="lang_ru"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🇺🇸 English",
                    callback_data="lang_en"
                )
            ]
        ]
    )

    await message.answer(
        "🌍 Tilni tanlang",
        reply_markup=keyboard
    )

# =========================
# TEXT SEARCH
# =========================

@dp.message(F.text)
async def text_search(message: Message):

    text = message.text.lower()

    user_id = message.from_user.id

    mode = user_modes.get(user_id)

    if mode == "model":

        stats["searches"] += 1

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📦 PRO MODELS",
                        callback_data=f"pro_{text}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆓 FREE MODELS",
                        callback_data=f"free_{text}"
                    )
                ]
            ]
        )

        await message.answer(
            f"""
🔎 SEARCH:

{text}

Kerakli bo‘limni tanlang 👇
""",
            reply_markup=keyboard
        )

# =========================
# TELEGRAM SEARCH
# =========================

async def telegram_search(query):

    results = []

    for channel in FREE_CHANNELS:

        try:

            messages = await tg_client.get_messages(
                channel,
                limit=20,
                search=query
            )

            for msg in messages:

                if msg.file:
                    results.append(msg)

        except Exception as e:

            print(e)

    return results

# =========================
# CALLBACKS
# =========================

@dp.callback_query()
async def callbacks(callback: CallbackQuery):

    data = callback.data

    # =========================
    # LANGUAGE
    # =========================

    if data.startswith("lang_"):

        lang = data.replace("lang_", "")

        user_languages[callback.from_user.id] = lang

        await callback.message.answer(
            f"✅ Til o‘zgartirildi: {lang}"
        )

    # =========================
    # PRO MODELS
    # =========================

    elif data.startswith("pro_"):

        query = data.replace("pro_", "")

        await callback.message.answer(
            f"""
📦 PRO MODELS

🌐 https://3ddd.ru/search?query={query}

🌐 https://www.cgtrader.com/3d-models?keywords={query}

🌐 https://www.turbosquid.com/Search/3D-Models/{query}

🌐 https://sketchfab.com/search?q={query}&type=models
"""
        )

    # =========================
    # FREE MODELS
    # =========================

    elif data.startswith("free_"):

        query = data.replace("free_", "")

        await callback.message.answer(
            "🔎 Telegramdan qidirilmoqda..."
        )

        telegram_results = await telegram_search(query)

        if telegram_results:

            await callback.message.answer(
                f"✅ {len(telegram_results)} ta model topildi"
            )

            count = 0

            for result in telegram_results:

                try:

                    file_path = await tg_client.download_media(result)

                    if file_path:

                        file = FSInputFile(file_path)

                        await bot.send_document(
                            chat_id=callback.message.chat.id,
                            document=file,
                            caption=f"📦 MODEL: {query}"
                        )

                        stats["downloads"] += 1

                        count += 1

                    if count >= 5:
                        break

                except Exception as e:

                    print(e)

        else:

            await callback.message.answer(
                "❌ Model topilmadi"
            )

# =========================
# MAIN
# =========================

async def main():

    logging.basicConfig(level=logging.INFO)

    await tg_client.start()

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())