from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bosh menyu handleri"""
    user = update.effective_user
    web_app_url = "https://your-web-app-url.com"
    
    keyboard = [
        [
            InlineKeyboardButton("🚗 Mashinalar", callback_data="cars"),
            InlineKeyboardButton("📅 Bron qilish", web_app=WebAppInfo(url=web_app_url))
        ],
        [InlineKeyboardButton("👤 Profil", callback_data="profile")]
    ]
    
    await update.message.reply_html(
        rf"Salom {user.mention_html()}! Rent-a-Car botiga xush kelibsiz!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )