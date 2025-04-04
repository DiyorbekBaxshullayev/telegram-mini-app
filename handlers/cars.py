from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

# Mashinalar ro'yxati
CARS = [
    {"id": 1, "name": "Chevrolet Spark", "price": 30, "desc": "Iqtisodiy va qulay"},
    {"id": 2, "name": "Gentra", "price": 40, "desc": "Zamonaviy va qulay sedan"},
    {"id": 3, "name": "Cobalt", "price": 50, "desc": "Keng salonli"},
    {"id": 4, "name": "Malibu", "price": 80, "desc": "Biznes klass"},
]

async def cars_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mashinalar ro'yxatini ko'rsatish"""
    try:
        # Mashinalar ro'yxatini tayyorlash
        text = "🚗 Mashinalar ro'yxati:\n\n"
        for car in CARS:
            text += f"{car['id']}. {car['name']} - ${car['price']}/kun\n"
            text += f"   {car['desc']}\n\n"
        
        # Tugmalar yaratish
        buttons = [
            [InlineKeyboardButton(f"{car['id']}. {car['name']}", callback_data=f"car_{car['id']}")]
            for car in CARS
        ]
        buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
        
        # Xabarni yuborish
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(buttons))
            await update.callback_query.answer()
        else:
            await update.message.reply_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(buttons))
    
    except Exception as e:
        logger.error(f"Mashinalar ro'yxatida xato: {e}")
        error_msg = "⚠️ Mashinalar ro'yxatini yuklab bo'lmadi"
        if update.callback_query:
            await update.callback_query.answer(error_msg, show_alert=True)
        else:
            await update.message.reply_text(error_msg)

async def car_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mashina haqida batafsil ma'lumot"""
    try:
        query = update.callback_query
        await query.answer()
        
        car_id = int(query.data.split('_')[1])
        car = next((c for c in CARS if c['id'] == car_id), None)
        
        if not car:
            await query.edit_message_text("⚠️ Mashina topilmadi")
            return
        
        text = (f"🚗 {car['name']}\n\n"
                f"💰 Narxi: ${car['price']}/kun\n"
                f"📝 Tavsifi: {car['desc']}\n\n"
                f"Bron qilish uchun kunlar sonini tanlang:")
        
        # Kunlar uchun tugmalar
        days_buttons = [
            InlineKeyboardButton(f"{i} kun", callback_data=f"rent_{car_id}_{i}")
            for i in [1, 2, 3, 5, 7]
        ]
        
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([
                days_buttons,
                [InlineKeyboardButton("🔙 Orqaga", callback_data="cars")]
            ]))
    
    except Exception as e:
        logger.error(f"Mashina detallarida xato: {e}")
        await query.answer("⚠️ Xato yuz berdi", show_alert=True)