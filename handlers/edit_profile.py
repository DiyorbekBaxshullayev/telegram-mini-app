from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def edit_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ismni tahrirlash"""
    query = update.callback_query
    await query.answer()
    context.user_data['editing'] = 'name'
    
    await query.edit_message_text(
        text="Yangi ismingizni kiriting:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Bekor qilish", callback_data="profile")]
        ])
    )

async def edit_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Telefon raqamini tahrirlash"""
    query = update.callback_query
    await query.answer()
    context.user_data['editing'] = 'phone'
    
    await query.edit_message_text(
        text="Yangi telefon raqamingizni kiriting (+998XXXXXXXXX formatida):",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Bekor qilish", callback_data="profile")]
        ])
    )

async def edit_license_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Guvohnoma ma'lumotlarini tahrirlash"""
    query = update.callback_query
    await query.answer()
    context.user_data['editing'] = 'license'
    
    await query.edit_message_text(
        text="Haydovchilik guvohnomangiz toifasini kiriting (A, B, C yoki D):",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Bekor qilish", callback_data="profile")]
        ])
    )