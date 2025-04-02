import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async def create_pool():
    """Ma'lumotlar bazasi ulanishini yaratish"""
    return await asyncpg.create_pool(DATABASE_URL)

async def get_cars(pool):
    """Mashinalar ro'yxatini olish"""
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT * FROM cars WHERE available = TRUE")

async def book_car(pool, car_id, user_id, start_time, end_time):
    """Mashinani bron qilish"""
    async with pool.acquire() as conn:
        # Bron qilish logikasi
        pass