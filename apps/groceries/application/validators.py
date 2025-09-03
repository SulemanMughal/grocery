from dataclasses import dataclass

@dataclass
class GroceryCreateDTO:
    name: str
    location: str

@dataclass
class GroceryUpdateDTO:
    name: str | None = None
    location: str | None = None

def validate_create(dto: GroceryCreateDTO):
    if not dto.name or len(dto.name.strip()) < 2:
        raise ValueError("Grocery name too short.")
    if not dto.location or len(dto.location.strip()) < 2:
        raise ValueError("Grocery location too short.")

def validate_update(dto: GroceryUpdateDTO):
    if dto.name is None and dto.location is None:
        raise ValueError("Nothing to update.")
    if dto.name is not None and len(dto.name.strip()) < 2:
        raise ValueError("Grocery name too short.")
    if dto.location is not None and len(dto.location.strip()) < 2:
        raise ValueError("Grocery location too short.")
