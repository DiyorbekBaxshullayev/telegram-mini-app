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
from handlers.cars import cars_handler
from handlers.profile import (
    profile_handler,
    edit_name_handler,
    edit_phone_handler,
    edit_license_handler,
    save_profile_changes
)
from handlers.back import back_handler
from handlers.error import error_handler

load_dotenv()

def setup_handlers(app):
    """Barcha handlerlarni ulash"""
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Callback handlers
    app.add_handler(CallbackQueryHandler(cars_handler, pattern="^cars$"))
    app.add_handler(CallbackQueryHandler(profile_handler, pattern="^profile$"))
    app.add_handler(CallbackQueryHandler(edit_name_handler, pattern="^edit_name$"))
    app.add_handler(CallbackQueryHandler(edit_phone_handler, pattern="^edit_phone$"))
    app.add_handler(CallbackQueryHandler(edit_license_handler, pattern="^edit_license$"))
    app.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))
    
    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_profile_changes))
    
    # Error handler
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