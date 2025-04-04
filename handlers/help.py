from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchiga yordam ko'rsatish"""
    help_text = (
        "🤖 *Botdan foydalanish qo'llanmasi*\n\n"
        "*/start* - Asosiy menyuni ko'rsatish\n"
        "*/profil* - Profil ma'lumotlari\n"
        "*/mashinalar* - Mashinalar ro'yxati\n"
        "*/bron* - Mashina bron qilish\n"
        "*/savatcha* - Savatchangizdagi mahsulotlar\n"
        "*/yordam* - Bu qo'llanma\n\n"
        "ℹ️ Qo'shimcha savollar uchun @admin ga murojaat qiling."
    )
    
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(help_text, parse_mode="Markdown")