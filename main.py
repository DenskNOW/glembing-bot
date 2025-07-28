import asyncio
import os
import schedule
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN, CHANNEL_USERNAME
from funnel import start, button_callback
from gpt import generate_post
from media_manager import get_random_media

async def post_to_channel(app):
    try:
        message = generate_post()
        media_path = get_random_media()
        bot = app.bot

        if media_path:
            ext = os.path.splitext(media_path)[-1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                with open(media_path, "rb") as photo:
                    await bot.send_photo(chat_id=CHANNEL_USERNAME, photo=photo, caption=message)
            elif ext in [".mp4", ".mov"]:
                with open(media_path, "rb") as video:
                    await bot.send_video(chat_id=CHANNEL_USERNAME, video=video, caption=message)
            else:
                await bot.send_message(chat_id=CHANNEL_USERNAME, text=message)
        else:
            await bot.send_message(chat_id=CHANNEL_USERNAME, text=message)

        print("✅ Пост отправлен!")

    except Exception as e:
        print("❌ Ошибка при отправке:", e)

async def sched
