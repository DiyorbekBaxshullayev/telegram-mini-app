from dataclasses import dataclass
from datetime import datetime

@dataclass
class Car:
    id: int
    model: str
    price: int
    available: bool

@dataclass
class Booking:
    id: int
    car_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    status: str  # "pending", "confirmed", "cancelled"