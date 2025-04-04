import logging
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xatolarni qayta ishlash"""
    logger.error(msg="Xato yuz berdi:", exc_info=context.error)
    
    if hasattr(update, 'callback_query'):
        await update.callback_query.answer("⚠️ Xato yuz berdi. Iltimos, qayta urinib ko'ring.")
    elif hasattr(update, 'message'):
        await update.message.reply_text("⚠️ Xato yuz berdi. Iltimos, qayta urinib ko'ring.")