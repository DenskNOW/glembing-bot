from telegram import Bot
import schedule
import time
import os
from config import BOT_TOKEN, CHANNEL_USERNAME
from gpt import generate_post
from media_manager import get_random_media
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from funnel import start, button_callback

bot = Bot(token=BOT_TOKEN)

def post_to_channel():
    try:
        message = generate_post()
        media_path = get_random_media()

        if media_path:
            ext = os.path.splitext(media_path)[-1].lower()
            if ext in [".jpg", ".jpeg", ".png"]:
                bot.send_photo(chat_id=CHANNEL_USERNAME, photo=open(media_path, "rb"), caption=message)
            elif ext in [".mp4", ".mov"]:
                bot.send_video(chat_id=CHANNEL_USERNAME, video=open(media_path, "rb"), caption=message)
            else:
                bot.send_message(chat_id=CHANNEL_USERNAME, text=message)
        else:
            bot.send_message(chat_id=CHANNEL_USERNAME, text=message)

        print("Пост отправлен!")

    except Exception as e:
        print("Ошибка при отправке:", e)

schedule.every().day.at("10:00").do(post_to_channel)

def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.run_polling()

import threading

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()

    while True:
        schedule.run_pending()
        time.sleep(1)