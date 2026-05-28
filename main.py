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
import base64

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
# USER MODES
# =========================

user_modes = {}

# =========================
# FREE CHANNELS
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
        [KeyboardButton(text="🧠 Model Feedback")]
    ],
    resize_keyboard=True
)

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

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
        "🎨 Texture rasmini yoki nomini yuboring"
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
# IMAGE ANALYZE
# =========================

async def detect_object(base64_image):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Detect the object in image. Return ONLY one keyword. Example: sofa, lamp, chair, tractor."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=20
    )

    result = response.choices[0].message.content.strip()

    result = result.split(",")[0]
    result = result.split(".")[0]

    return result.lower().strip()

# =========================
# IMAGE HANDLER
# =========================

@dp.message(F.photo)
async def image_handler(message: Message):

    user_id = message.from_user.id

    mode = user_modes.get(user_id)

    await message.answer(
        "🤖 AI analiz qilmoqda..."
    )

    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    file_path = file.file_path

    downloaded_file = await bot.download_file(file_path)

    image_path = f"{user_id}.jpg"

    with open(image_path, "wb") as f:
        f.write(downloaded_file.read())

    with open(image_path, "rb") as image_file:

        base64_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    # =========================
    # MODEL SEARCH
    # =========================

    if mode == "model":

        detected_model = await detect_object(base64_image)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📦 PRO MODELS",
                        callback_data=f"pro_{detected_model}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆓 FREE MODELS",
                        callback_data=f"free_{detected_model}"
                    )
                ]
            ]
        )

        await message.answer(
            f"""
🤖 AI DETECTED:

{detected_model}

Kerakli bo‘limni tanlang 👇
""",
            reply_markup=keyboard
        )

    # =========================
    # TEXTURE
    # =========================

    elif mode == "texture":

        detected_texture = await detect_object(base64_image)

        await message.answer(
            f"""
🎨 TEXTURE:

{detected_texture}
"""
        )

    # =========================
    # RENDER FEEDBACK
    # =========================

    elif mode == "render":

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this render professionally and give short feedback."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        feedback = response.choices[0].message.content

        await message.answer(
            f"""
📸 RENDER FEEDBACK

{feedback}
"""
        )

    # =========================
    # MODEL FEEDBACK
    # =========================

    elif mode == "feedback":

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this 3D model professionally and give short feedback."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        feedback = response.choices[0].message.content

        await message.answer(
            f"""
🧠 MODEL FEEDBACK

{feedback}
"""
        )

# =========================
# TEXT SEARCH
# =========================

@dp.message(F.text)
async def text_handler(message: Message):

    text = message.text.lower().strip()

    user_id = message.from_user.id

    mode = user_modes.get(user_id)

    if mode == "model":

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
# CALLBACKS
# =========================

@dp.callback_query()
async def callbacks(callback: CallbackQuery):

    data = callback.data

    # =========================
    # PRO MODELS
    # =========================

    if data.startswith("pro_"):

        query = data.replace("pro_", "")

        text = f"""
📦 PRO MODELS

🌐 https://3ddd.ru/search?query={query}

🌐 https://greatcatalog.net/?s={query}

🌐 https://www.turbosquid.com/Search/3D-Models/{query}

🌐 https://www.cgtrader.com/3d-models?keywords={query}

🌐 https://cgmood.com/search/{query}

🌐 https://sketchfab.com/search?q={query}&type=models
"""

        await callback.message.answer(text)

    # =========================
    # FREE MODELS
    # =========================

    elif data.startswith("free_"):

        query = data.replace("free_", "")

        await callback.message.answer(
            "🔎 Telegram kanallardan qidirilmoqda..."
        )

        telegram_results = await telegram_search(query)

        if telegram_results:

            await callback.message.answer(
                f"✅ {len(telegram_results)} ta model topildi"
            )

            sent_count = 0

            for result in telegram_results:

                try:

                    file_path = await tg_client.download_media(result)

                    if file_path:

                        file = FSInputFile(file_path)

                        await bot.send_document(
                            chat_id=callback.message.chat.id,
                            document=file,
                            caption=f"📦 FREE MODEL: {query}"
                        )

                        sent_count += 1

                    if sent_count >= 5:
                        break

                except Exception as e:

                    print(e)

        else:

            await callback.message.answer(
                "❌ Telegramda model topilmadi"
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