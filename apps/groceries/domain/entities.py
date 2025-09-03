from dataclasses import dataclass
from datetime import datetime, date

@dataclass(frozen=True)
class GroceryEntity:
    id: str
    name: str
    location: str
    is_active: bool
    created_at: datetime
    updated_at: datetime



@dataclass(frozen=True)
class ItemEntity:
    id: str
    name: str
    item_type: str
    item_location: str
    price: float
    is_deleted: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class DailyIncomeEntity:
    id: str
    amount: float
    date: date
    created_at: datetime
    updated_at: datetime