from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Profil ma'lumotlari handleri"""
    query = update.callback_query
    await query.answer()
    
    user_data = context.user_data.setdefault('profile', {
        'name': 'Ism kiritilmagan',
        'phone': 'Telefon kiritilmagan',
        'license': 'Guvohnoma kiritilmagan'
    })
    
    await query.edit_message_text(
        text=f"👤 <b>Profil ma'lumotlari</b>\n\n"
             f"🏷 Ism: {user_data['name']}\n"
             f"📱 Telefon: {user_data['phone']}\n"
             f"📜 Guvohnoma: {user_data['license']}\n\n"
             f"Quyidagilardan birini tahrirlashingiz mumkin:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Ismni o'zgartirish", callback_data="edit_name")],
            [InlineKeyboardButton("📱 Telefon raqamni o'zgartirish", callback_data="edit_phone")],
            [InlineKeyboardButton("📜 Guvohnoma ma'lumotlari", callback_data="edit_license")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back")]
        ]),
        parse_mode='HTML')

async def edit_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ism tahrirlash handleri"""
    query = update.callback_query
    await query.answer()
    context.user_data['editing'] = 'name'
    await query.edit_message_text(
        text="Yangi ismingizni kiriting:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Bekor qilish", callback_data="profile")]
        ]))

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
        ]))

async def save_profile_changes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Profil o'zgarishlarini saqlash handleri"""
    if 'editing' not in context.user_data:
        await update.message.reply_text("Iltimos, profil menyusidan tahrirlash tugmasini bosing!")
        return
    
    field = context.user_data['editing']
    new_value = update.message.text
    
    if field == 'phone' and not new_value.startswith('+998') and len(new_value) != 12:
        await update.message.reply_text("❗ Noto'g'ri telefon raqam formati. Iltimos, +998XXXXXXXXX formatida kiriting.")
        return
    elif field == 'license' and new_value.upper() not in ['A', 'B', 'C', 'D']:
        await update.message.reply_text("❗ Noto'g'ri guvohnoma toifasi. Iltimos, A, B, C yoki D kiriting.")
        return
    
    if 'profile' not in context.user_data:
        context.user_data['profile'] = {
            'name': 'Ism kiritilmagan',
            'phone': 'Telefon kiritilmagan',
            'license': 'Guvohnoma kiritilmagan'
        }
    
    context.user_data['profile'][field] = new_value
    del context.user_data['editing']
    
    await update.message.reply_text("✅ Ma'lumotlar muvaffaqiyatli saqlandi!")
    await profile_handler(update, context)