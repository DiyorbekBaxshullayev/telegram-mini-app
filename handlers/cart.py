from telegram import Update
from telegram.ext import ContextTypes

async def cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Savatcha bo'limi"""
    await update.message.reply_text(
        text="🛒 Sizning savatchangiz:\n\n"
             "1. Chevrolet Spark - 3 kun - $90\n"
             "2. Gentra - 2 kun - $80\n\n"
             "Jami: $170\n\n"
             "Buyurtma berish uchun /checkout buyrug'ini yuboring"
    )