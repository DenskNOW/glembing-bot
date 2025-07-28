from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from storage import save_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username)

    keyboard = [[InlineKeyboardButton("📥 Получить стратегию", callback_data="get_strategy")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Ты на пути к $100,000 через Glembing 💸\n\nХочешь получить стартовую стратегию?",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_strategy":
        await query.edit_message_text("🎯 Стратегия отправлена! Следи за обновлениями в канале.")