from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
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
# DATABASE
# =========================

user_modes = {}

# =========================
# CHANNELS
# =========================

FREE_CHANNELS = [
    "free3dsky",
    "Free3dmodels",
    "free_3dsky",
    "FREE_3DSMAX_MODELS",
    "models_for_3dmax",
    "model_3dsmax",
    "CG_Game_Models",
    "arxitek03"
]

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        """
🔥 3D ASSISTANT AI

Buyruqlar:

🔎 Model Izlash
📸 Render Feedback
🧠 Model Feedback
🎨 Texture Yaratish
"""
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
        "🧠 Model screenshot yuboring"
    )

@dp.message(F.text == "🎨 Texture Yaratish")
async def texture_mode(message: Message):

    user_modes[message.from_user.id] = "texture"

    await message.answer(
        "🎨 Texture rasmi yoki nom yuboring"
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
                limit=3,
                search=query
            )

            for msg in messages:

                if msg.file:

                    results.append(msg)

        except:
            pass

    return results

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

    await message.answer(
        "🤖 AI analiz qilmoqda..."
    )

    with open(image_path, "rb") as image_file:

        base64_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

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
                            "text": "What 3D object is this? Answer short only."
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

🔎 PRO SEARCH

🌐 https://3ddd.ru/search?query={detected_model}

🌐 https://www.cgtrader.com/3d-models?keywords={detected_model}

🌐 https://sketchfab.com/search?q={detected_model}&type=models
"""
        )

        telegram_results = await telegram_search(
            detected_model
        )

        if telegram_results:

            await message.answer(
                "📦 FREE MODELS TOPILDI"
            )

            for result in telegram_results[:3]:

                await bot.forward_message(
                    chat_id=message.chat.id,
                    from_chat_id=result.chat_id,
                    message_id=result.id
                )

        else:

            await message.answer(
                "❌ Telegramda model topilmadi"
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
                            "text": "Analyze this 3D render professionally. Tell lighting, realism, composition and weak points."
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
                            "text": "Analyze this 3D model professionally. Tell topology, mesh quality, UV and modeling problems."
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
    # TEXTURE AI
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
            max_tokens=50
        )

        detected_texture = response.choices[0].message.content

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=f"Ultra realistic seamless {detected_texture} texture, PBR material, high quality"
        )

        texture_url = image_response.data[0].url

        await message.answer(
            f"""
🎨 AI TEXTURE CREATED

Texture:
{detected_texture}

🖼 {texture_url}
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
🔎 PRO SEARCH

🌐 https://3ddd.ru/search?query={text}

🌐 https://www.cgtrader.com/3d-models?keywords={text}

🌐 https://sketchfab.com/search?q={text}&type=models
"""
        )

        telegram_results = await telegram_search(
            text
        )

        if telegram_results:

            await message.answer(
                "📦 FREE MODELS TOPILDI"
            )

            for result in telegram_results[:3]:

                await bot.forward_message(
                    chat_id=message.chat.id,
                    from_chat_id=result.chat_id,
                    message_id=result.id
                )

        else:

            await message.answer(
                "❌ Telegramda model topilmadi"
            )

    elif mode == "texture":

        image_response = client.images.generate(
            model="gpt-image-1",
            prompt=f"Ultra realistic seamless {text} texture, PBR material, high quality"
        )

        texture_url = image_response.data[0].url

        await message.answer(
            f"""
🎨 AI TEXTURE CREATED

🖼 {texture_url}
"""
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
