from dataclasses import dataclass
from datetime import datetime

ROLE_ADMIN = "ADMIN"
ROLE_SUPPLIER = "SUPPLIER"

@dataclass(frozen=True)
class UserEntity:
    id: str
    name: str
    email: str
    role: str                 # ADMIN | SUPPLIER
    is_active: bool           # soft-delete flag
    created_at: datetime
    updated_at: datetime
