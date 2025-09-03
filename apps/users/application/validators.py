import re
from dataclasses import dataclass

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@dataclass
class UserCreateDTO:
    name: str
    email: str
    password: str
    role: str

def validate_user_create(d: UserCreateDTO):
    if not d.name or len(d.name) < 2:
        raise ValueError("Name too short")
    if not EMAIL_RE.match(d.email.lower().strip()):
        raise ValueError("Invalid email")
    if len(d.password) < 8:
        raise ValueError("Password too short (min 8)")
    if d.role not in ("ADMIN", "SUPPLIER"):
        raise ValueError("Invalid role")
