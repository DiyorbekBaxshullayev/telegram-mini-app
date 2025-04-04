from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botni ishga tushirish"""
    menu_buttons = [
        ["🚗 Mashinalar", "📅 Bron qilish"],
        ["👤 Profil", "🛒 Savatcha"],
        ["ℹ️ Yordam"]  # Yangi qo'shilgan
    ]
    
    reply_markup = ReplyKeyboardMarkup(
        menu_buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await update.message.reply_text(
        "🚖 Rent-a-Car botiga xush kelibsiz!\n"
        "Quyidagi menyudan kerakli bo'limni tanlang yoki /yordam buyrug'ini yuboring.",
        reply_markup=reply_markup
    )