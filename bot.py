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
    ContextTypes,
    MessageHandler,
    filters
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
    """Profil ma'lumotlari va tahrirlash imkoniyati"""
    query = update.callback_query
    await query.answer()
    
    # Foydalanuvchi ma'lumotlarini olish yoki boshlang'ich qiymatlar bilan ishga tushirish
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
        parse_mode='HTML'
    )

async def edit_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ismni tahrirlash uchun so'rov"""
    query = update.callback_query
    await query.answer()
    context.user_data['editing'] = 'name'  # Qaysi maydon tahrirlanayotganligini saqlaymiz
    await query.edit_message_text(
        text="Yangi ismingizni kiriting:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Bekor qilish", callback_data="profile")]
        ])
    )

async def edit_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Telefon raqamini tahrirlash uchun so'rov"""
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
    """Guvohnoma ma'lumotlarini tahrirlash uchun so'rov"""
    query = update.callback_query
    await query.answer()
    context.user_data['editing'] = 'license'
    await query.edit_message_text(
        text="Haydovchilik guvohnomangiz toifasini kiriting (A, B, C yoki D):",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Bekor qilish", callback_data="profile")]
        ])
    )

async def save_profile_changes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi kiritgan ma'lumotlarni saqlaymiz"""
    if 'editing' not in context.user_data:
        await update.message.reply_text("Iltimos, profil menyusidan tahrirlash tugmasini bosing!")
        return
    
    field = context.user_data['editing']
    new_value = update.message.text
    
    # Ma'lumotlarni tekshirish
    if field == 'phone' and not new_value.startswith('+998') and len(new_value) != 12:
        await update.message.reply_text("❗ Noto'g'ri telefon raqam formati. Iltimos, +998XXXXXXXXX formatida kiriting.")
        return
    elif field == 'license' and new_value.upper() not in ['A', 'B', 'C', 'D']:
        await update.message.reply_text("❗ Noto'g'ri guvohnoma toifasi. Iltimos, A, B, C yoki D kiriting.")
        return
    
    # Profil ma'lumotlarini ishga tushirish (agar mavjud bo'lmasa)
    if 'profile' not in context.user_data:
        context.user_data['profile'] = {
            'name': 'Ism kiritilmagan',
            'phone': 'Telefon kiritilmagan',
            'license': 'Guvohnoma kiritilmagan'
        }
    
    # Yangi qiymatni saqlash
    context.user_data['profile'][field] = new_value
    del context.user_data['editing']  # Tahrirlash holatini olib tashlaymiz
    
    await update.message.reply_text("✅ Ma'lumotlar muvaffaqiyatli saqlandi!")
    await profile_handler(update, context)  # Profil menyusiga qaytamiz

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchi kiritgan ma'lumotlarni qayta ishlash"""
    # Bu yerda foydalanuvchi kiritgan ma'lumotni saqlash va profilga qaytish kerak
    await update.message.reply_text("Ma'lumotlar saqlandi!")
    await profile_handler(update, context)

def main() -> None:
    """Dasturni ishga tushirish"""
    application = Application.builder().token(TOKEN).build()
    
    # Oldingi handlerlar...
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    
    application.run_polling()

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Orqaga qaytish - faqat asosiy menyuga qaytaradi"""
    query = update.callback_query
    await query.answer()
    
    # Asosiy menyuni qayta yuborish
    keyboard = [
        [
            InlineKeyboardButton("🚗 Mashinalar", callback_data="cars"),
            InlineKeyboardButton("📅 Bron qilish", web_app=WebAppInfo(url="https://your-web-app-url.com"))
        ],
        [InlineKeyboardButton("👤 Profil", callback_data="profile")]
    ]
    
    await query.edit_message_text(
        text="Rent-a-Car botiga xush kelibsiz!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Xatolarni qayta ishlash"""
    logger.error(msg="Xato yuz berdi:", exc_info=context.error)
    
    if update.callback_query:
        await update.callback_query.answer("⚠️ Xato yuz berdi. Iltimos, qayta urinib ko'ring.")
    elif update.message:
        await update.message.reply_text("⚠️ Xato yuz berdi. Iltimos, qayta urinib ko'ring.")

def main() -> None:
    """Dasturni ishga tushirish"""
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(cars_handler, pattern="^cars$"))
    application.add_handler(CallbackQueryHandler(profile_handler, pattern="^profile$"))
    application.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))
    application.add_handler(CallbackQueryHandler(edit_name_handler, pattern="^edit_name$"))
    application.add_handler(CallbackQueryHandler(edit_phone_handler, pattern="^edit_phone$"))
    application.add_handler(CallbackQueryHandler(edit_license_handler, pattern="^edit_license$"))
    application.add_error_handler(error_handler)
    
    # MessageHandler ni qo'shamiz
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, save_profile_changes)
    )
    
    application.run_polling()

if __name__ == "__main__":
    main() 