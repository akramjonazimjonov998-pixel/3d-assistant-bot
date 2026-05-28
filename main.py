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

from openai import OpenAI

import asyncio
import logging
import os
import base64

# =========================
# TOKENS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

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
💳 PREMIUM OBUNA

1 Oy — 34.999 so'm
3 Oy — 95.000 so'm
""",

        "ru": """
💳 PREMIUM ПОДПИСКА

1 Месяц — 34.999 сум
3 Месяца — 95.000 сум
""",

        "en": """
💳 PREMIUM SUBSCRIPTION

1 Month — 34.999 UZS
3 Months — 95.000 UZS
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
# MODES
# =========================

@dp.message(F.text.in_(["🔎 Model Izlash", "🔎 Поиск Моделей", "🔎 Find Models"]))
async def model_mode(message: Message):

    user_id = message.from_user.id

    user_modes[user_id] = "model"

    user_stats.setdefault(user_id, {
        "models": 0,
        "renders": 0,
        "feedbacks": 0,
        "textures": 0
    })

    user_stats[user_id]["models"] += 1

    await message.answer(
        "📸 Model rasmini yuboring yoki model nomini yozing"
    )

@dp.message(F.text.in_(["📸 Render Feedback", "📸 Анализ Рендера"]))
async def render_mode(message: Message):

    user_id = message.from_user.id

    user_modes[user_id] = "render"

    user_stats.setdefault(user_id, {
        "models": 0,
        "renders": 0,
        "feedbacks": 0,
        "textures": 0
    })

    user_stats[user_id]["renders"] += 1

    await message.answer(
        "📸 Render rasmini yuboring"
    )

@dp.message(F.text.in_(["🧠 Model Feedback", "🧠 Feedback Модели"]))
async def feedback_mode(message: Message):

    user_id = message.from_user.id

    user_modes[user_id] = "feedback"

    user_stats.setdefault(user_id, {
        "models": 0,
        "renders": 0,
        "feedbacks": 0,
        "textures": 0
    })

    user_stats[user_id]["feedbacks"] += 1

    await message.answer(
        "🧠 Model screenshot yuboring"
    )

@dp.message(F.text.in_(["🎨 Texture Yaratish", "🎨 Создать Текстуру", "🎨 Create Texture"]))
async def texture_mode(message: Message):

    user_id = message.from_user.id

    user_modes[user_id] = "texture"

    user_stats.setdefault(user_id, {
        "models": 0,
        "renders": 0,
        "feedbacks": 0,
        "textures": 0
    })

    user_stats[user_id]["textures"] += 1

    await message.answer(
        "🎨 Texture rasmini yuboring"
    )

# =========================
# PHOTO AI SYSTEM
# =========================

@dp.message(F.photo)
async def image_handler(message: Message):

    user_id = message.from_user.id
    mode = user_modes.get(user_id)

    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    file_path = file.file_path

    downloaded_file = await bot.download_file(file_path)

    image_path = f"temp_{user_id}.jpg"

    with open(image_path, "wb") as f:
        f.write(downloaded_file.read())

    await message.answer("🤖 AI analiz qilmoqda...")

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # =========================
    # MODEL SEARCH
    # =========================

    if mode == "model":

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What 3D object is this? Answer very short only."
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
            max_tokens=30
        )

        detected_model = response.choices[0].message.content

        await message.answer(
            f"""
🤖 AI DETECTED:

{detected_model}

🔎 AI MODEL SEARCH RESULTS

💎 PRO MODELS
━━━━━━━━━━━━━━━

🌐 https://3ddd.ru/search?query={detected_model}

🌐 https://greatcatalog.net/?s={detected_model}

🌐 https://www.turbosquid.com/Search/3D-Models/{detected_model}

🌐 https://www.cgtrader.com/3d-models?keywords={detected_model}

🌐 https://cgmood.com/search/{detected_model}

🌐 https://sketchfab.com/search?q={detected_model}&type=models


🆓 FREE MODELS
━━━━━━━━━━━━━━━

🌐 https://t.me/s/free3dsky?q={detected_model}

🌐 https://t.me/s/Free3dmodels?q={detected_model}

🌐 https://t.me/s/free_3dsky?q={detected_model}

🌐 https://t.me/s/FREE_3DSMAX_MODELS?q={detected_model}

🌐 https://t.me/s/models_for_3dmax?q={detected_model}

🌐 https://t.me/s/model_3dsmax?q={detected_model}

🌐 https://t.me/s/CG_Game_Models?q={detected_model}

🌐 https://t.me/s/arxitek03?q={detected_model}
"""
        )

    # =========================
    # RENDER FEEDBACK
    # =========================

    elif mode == "render":

        await message.answer(
            """
📸 RENDER FEEDBACK

✅ Lighting yaxshi
✅ Material realistic
⚠️ Shadow kuchsiz
⚠️ AO yetishmaydi
"""
        )

    # =========================
    # MODEL FEEDBACK
    # =========================

    elif mode == "feedback":

        await message.answer(
            """
🧠 MODEL FEEDBACK

✅ Topology yaxshi
✅ Mesh clean
⚠️ UV improve kerak
"""
        )

    # =========================
    # TEXTURE SEARCH
    # =========================

    elif mode == "texture":

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What texture or material is this? Answer short only."
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
            max_tokens=30
        )

        detected_texture = response.choices[0].message.content

        await message.answer(
            f"""
🎨 AI TEXTURE DETECTED:

{detected_texture}

🌐 https://polyhaven.com/textures?q={detected_texture}

🌐 https://ambientcg.com/list?search={detected_texture}
"""
        )

# =========================
# TEXT SEARCH
# =========================

@dp.message(F.text)
async def text_search(message: Message):

    text = message.text
    user_id = message.from_user.id
    mode = user_modes.get(user_id)

    if mode == "model":

        await message.answer(
            f"""
🔎 AI MODEL SEARCH RESULTS

🌐 https://3ddd.ru/search?query={text}

🌐 https://greatcatalog.net/?s={text}

🌐 https://www.turbosquid.com/Search/3D-Models/{text}

🌐 https://www.cgtrader.com/3d-models?keywords={text}

🌐 https://cgmood.com/search/{text}

🌐 https://sketchfab.com/search?q={text}&type=models
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

@dp.message(F.text.in_(["📊 Statistika", "📊 Statistics", "📊 Статистика"]))
async def statistics(message: Message):

    user_id = message.from_user.id

    user_stats.setdefault(user_id, {
        "models": 0,
        "renders": 0,
        "feedbacks": 0,
        "textures": 0
    })

    stats = user_stats[user_id]

    await message.answer(
        f"""
📊 YOUR STATISTICS

🔎 Model search: {stats['models']}
📸 Render feedback: {stats['renders']}
🧠 Model feedback: {stats['feedbacks']}
🎨 Texture search: {stats['textures']}
"""
    )

# =========================
# MAIN
# =========================

async def main():

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```
