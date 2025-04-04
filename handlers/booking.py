from telegram import Update
from telegram.ext import ContextTypes

async def booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bron qilish bo'limi"""
    await update.message.reply_text(
        text="Bron qilish uchun quyidagilardan birini tanlang:\n\n"
             "1. Mashina bron qilish\n"
             "2. Mening bronlarim\n"
             "3. Bronni bekor qilish"
    )