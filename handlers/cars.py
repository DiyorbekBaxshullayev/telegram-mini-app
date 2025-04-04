from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def cars_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mashinalar ro'yxati handleri"""
    query = update.callback_query
    await query.answer()
    
    cars = [
        {"id": 1, "model": "Cobalt", "price": 150000},
        {"id": 2, "model": "Gentra", "price": 180000},
        {"id": 3, "model": "Malibu", "price": 250000}
    ]
    
    buttons = [
        [InlineKeyboardButton(f"{car['model']} - {car['price']:,} so'm/soat", 
        callback_data=f"car_{car['id']}")] for car in cars
    ]
    buttons.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back")])
    
    await query.edit_message_text(
        text="🏎 Mavjud mashinalar:",
        reply_markup=InlineKeyboardMarkup(buttons))