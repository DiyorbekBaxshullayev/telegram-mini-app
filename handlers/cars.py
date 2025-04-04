from telegram import Update
from telegram.ext import ContextTypes

async def cars_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mashinalar bo'limi"""
    await update.message.reply_text(
        text="Mashinalar ro'yxati:\n\n"
             "1. Chevrolet Spark - $30/kun\n"
             "2. Gentra - $40/kun\n"
             "3. Cobalt - $50/kun\n"
             "4. Malibu - $80/kun\n\n"
             "Bron qilish uchun mashinani tanlang."
    )