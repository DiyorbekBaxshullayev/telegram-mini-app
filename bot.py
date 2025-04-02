import logging
import os
from typing import Optional

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from dotenv import load_dotenv

# Konfiguratsiya
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botni ishga tushirish"""
    user = update.effective_user
    web_app_url = "https://your-web-app-url.com"  # Web App manzilingiz
    
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

async def cars_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mashinalar ro'yxati"""
    query = update.callback_query
    await query.answer()
    
    # Bu joyda ma'lumotlar bazasidan mashinalar olinadi
    cars = [
        {"id": 1, "model": "Cobalt", "price": 150000},
        {"id": 2, "model": "Gentra", "price": 180000},
        {"id": 3, "model": "Malibu", "price": 250000}
    ]
    
    buttons = []
    for car in cars:
        buttons.append(
            [InlineKeyboardButton(
                f"{car['model']} - {car['price']:,} so'm/soat",
                callback_data=f"car_{car['id']}")]
        )
    
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
    
    await query.edit_message_text(
        text="🏎 Mavjud mashinalar:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Profil ma'lumotlari"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text="👤 Profil ma'lumotlari:\n\n"
             "Ism: Foydalanuvchi\n"
             "Telefon: +9989XXXXXXXX\n"
             "Haydovchilik guvohnomasi: B toifa",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Tahrirlash", callback_data="edit_profile")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back")]
        ])
    )

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Orqaga qaytish"""
    query = update.callback_query
    await query.answer()
    await start(update, context)

def main() -> None:
    """Dasturni ishga tushirish"""
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(cars_handler, pattern="^cars$"))
    application.add_handler(CallbackQueryHandler(profile_handler, pattern="^profile$"))
    application.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))
    
    # Ishga tushirish
    application.run_polling()

if __name__ == "__main__":
    main()