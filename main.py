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

# LANGUAGES

# =========================

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

```
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
        ]
    ],
    resize_keyboard=True
)
```

}

# =========================

# START

# =========================

@dp.message(CommandStart())
async def start_handler(message: Message):

```
await message.answer(
    "🌍 Tilni tanlang / Выберите язык / Choose language",
    reply_markup=language_keyboard
)
```

# =========================

# LANGUAGE SELECT

# =========================

@dp.message(F.text.in_(["🇺🇿 Uzbek", "🇷🇺 Русский", "🇬🇧 English"]))
async def language_handler(message: Message):

```
user_id = message.from_user.id

if message.text == "🇺🇿 Uzbek":

    user_languages[user_id] = "uz"

    await message.answer(
        """
```

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

```
elif message.text == "🇷🇺 Русский":

    user_languages[user_id] = "ru"

    await message.answer(
        """
```

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

```
elif message.text == "🇬🇧 English":

    user_languages[user_id] = "en"

    await message.answer(
        """
```

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

# PAYMENT

# =========================

@dp.message(F.text.in_(["💳 To'lov", "💳 Оплата", "💳 Payment"]))
async def payment_handler(message: Message):

```
user_id = message.from_user.id
lang = user_languages.get(user_id, "uz")

payment_texts = {

    "uz": """
```

💳 OBUNA REJALARI

💎 Oddiy To'lov
━━━━━━━━━━━━━━━

1 Oy — 34.999 so'm
3 Oy — 95.000 so'm

👇 To'lov qilish uchun tugmani bosing
""",

```
    "ru": """
```

💳 ПЛАНЫ ПОДПИСКИ

💎 Обычная оплата
━━━━━━━━━━━━━━━

1 Месяц — 34.999 сум
3 Месяца — 95.000 сум

👇 Нажмите кнопку для оплаты
""",

```
    "en": """
```

💳 SUBSCRIPTION PLANS

💎 Standard Payment
━━━━━━━━━━━━━━━

1 Month — 34.999 UZS
3 Months — 95.000 UZS

👇 Press the payment button
"""
}

```
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
                    url="https://v0-3d-assistant-ai.vercel.app/"
                )
            )
        ]
    ]
)

await message.answer(
    payment_texts[lang],
    reply_markup=keyboard
)
```

# =========================

# MAIN

# =========================

async def main():

```
logging.basicConfig(level=logging.INFO)

await dp.start_polling(bot)
```

if **name** == "**main**":
asyncio.run(main())

