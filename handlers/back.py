from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

from handlers.start import start

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Orqaga qaytish"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🚗 Mashinalar", callback_data="cars"),
            InlineKeyboardButton("📅 Bron qilish", web_app=WebAppInfo(url="https://your-web-app-url.com"))
        ],
        [InlineKeyboardButton("👤 Profil", callback_data="profile")]
    ]
    
    await query.edit_message_text(
        text="Rent-a-Car botiga xush kelibsiz!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )