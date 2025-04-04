import logging
import os
from dotenv import load_dotenv
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler,
    filters,
    ContextTypes
)

# Handlerlarni import qilish
from handlers.start import start
from handlers.profile import (
    profile_handler,
    profile_button_handler,
    edit_name_handler,
    edit_phone_handler,
    edit_license_handler,
    save_profile_changes
)
from handlers.cars import cars_handler
from handlers.booking import booking_handler
from handlers.cart import (
    cart_handler,
    checkout_handler,
    clear_cart_handler
)
from handlers.back import back_handler
from handlers.help import help_handler  # Yangi qo'shilgan
from handlers.error import error_handler

load_dotenv()

def setup_handlers(app):
    """Barcha handlerlarni ulash"""
    # 1. Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profil", profile_handler))
    app.add_handler(CommandHandler("mashinalar", cars_handler))
    app.add_handler(CommandHandler("bron", booking_handler))
    app.add_handler(CommandHandler("savatcha", cart_handler))
    app.add_handler(CommandHandler("yordam", help_handler))  # Yangi

    # 2. Menu button handlers
    app.add_handler(MessageHandler(filters.Regex("^🚗 Mashinalar$"), cars_handler))
    app.add_handler(MessageHandler(filters.Regex("^📅 Bron qilish$"), booking_handler))
    app.add_handler(MessageHandler(filters.Regex(r"^(👤 Profil|Profil)$"), profile_button_handler))
    app.add_handler(MessageHandler(filters.Regex(r"^(🛒 Savatcha|Savatcha)$"), cart_handler))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Yordam$"), help_handler))  # Yangi
    
    # 3. Callback query handlers
    app.add_handler(CallbackQueryHandler(cars_handler, pattern="^cars$"))
    app.add_handler(CallbackQueryHandler(profile_handler, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(edit_name_handler, pattern="^edit_name$"))
    app.add_handler(CallbackQueryHandler(edit_phone_handler, pattern="^edit_phone$"))
    app.add_handler(CallbackQueryHandler(edit_license_handler, pattern="^edit_license$"))
    app.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))
    app.add_handler(CallbackQueryHandler(cart_handler, pattern="^cart$"))
    app.add_handler(CallbackQueryHandler(cart_handler, pattern="^checkout$"))
    app.add_handler(CallbackQueryHandler(cart_handler, pattern="^clear_cart$"))
    app.add_handler(CallbackQueryHandler(checkout_handler, pattern="^checkout$"))
    app.add_handler(CallbackQueryHandler(clear_cart_handler, pattern="^clear_cart$"))
    
    
    # 4. Profile edit handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_profile_changes))
    
    # 5. Error handler
    app.add_error_handler(error_handler)

def main():
    """Asosiy ishga tushirish funksiyasi"""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    setup_handlers(app)
    app.run_polling()

if __name__ == "__main__":
    main()