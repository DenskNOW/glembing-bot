import asyncio
import os
import time
import schedule
from telegram import Bot
from config import BOT_TOKEN, CHANNEL_USERNAME
from gpt import generate_post
from media_manager import get_random_media
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from funnel import start, button_callback

bot = Bot(token=BOT_TOKEN)

def post_to_channel_sync():
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

# Планировщик будет работать в отдельной async-задаче
async def scheduler_loop():
    schedule.every().day.at("10:00").do(post_to_channel_sync)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Запуск Telegram-поллинга и планировщика одновременно
    await asyncio.gather(
        app.run_polling(),
        scheduler_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
