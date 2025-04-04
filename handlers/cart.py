from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Savatcha bo'limi"""
    try:
        # Savatcha mavjudligini tekshirish
        if 'cart' not in context.user_data or not context.user_data['cart']:
            text = "🛒 Sizning savatchangiz bo'sh"
            keyboard = [[InlineKeyboardButton("🚗 Mashinalarni ko'rish", callback_data="cars")]]
        else:
            cart = context.user_data['cart']
            total = sum(item['total'] for item in cart)
            text = "🛒 Sizning savatchangiz:\n\n" + \
                   "\n".join(f"{idx}. {item['name']} - {item['days']} kun - ${item['total']}" 
                            for idx, item in enumerate(cart, 1)) + \
                   f"\n\nJami: ${total}"
            keyboard = [
                [InlineKeyboardButton("✅ Buyurtma berish", callback_data="checkout")],
                [InlineKeyboardButton("🗑 Savatchani tozalash", callback_data="clear_cart")],
            ]
        
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await update.callback_query.answer()
        else:
            await update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(keyboard))
                
    except Exception as e:
        logger.error(f"Savatchani ko'rsatishda xato: {e}")
        if update.callback_query:
            await update.callback_query.answer("⚠️ Xato yuz berdi", show_alert=True)

async def checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Buyurtma berish"""
    query = update.callback_query
    await query.answer()
    
    # Savatchani tekshirish
    if not context.user_data.get('cart'):
        await query.edit_message_text("⚠️ Savatchangiz bo'sh!")
        return
    
    await query.edit_message_text(
        text="✅ Buyurtma muvaffaqiyatli qabul qilindi!\n"
             "Tez orada operator siz bilan bog'lanadi.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back")]
        ])
    )
    # Savatchani tozalash
    context.user_data['cart'] = []

async def clear_cart_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Savatchani tozalash"""
    try:
        query = update.callback_query
        await query.answer()
        
        # Savatcha mavjudligini tekshirish
        if 'cart' not in context.user_data:
            context.user_data['cart'] = []
        
        # Savatchani tozalash
        context.user_data['cart'] = []
        
        # Yangi xabar yuborish
        await query.edit_message_text(
            text="🗑 Savatcha muvaffaqiyatli tozalandi!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚗 Mashinalar", callback_data="cars"),
                 InlineKeyboardButton("🛒 Savatcha", callback_data="cart")],
                [InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back")]
            ])
        )
        
    except Exception as e:
        logger.error(f"Xato: {str(e)}")
        await query.answer("⚠️ Savatchani tozalashda xato yuz berdi", show_alert=True)