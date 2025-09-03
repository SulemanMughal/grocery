from dataclasses import dataclass
from apps.groceries.domain.repositories import GroceryRepositoryPort
from apps.groceries.domain.entities import GroceryEntity
from .validators import GroceryCreateDTO, GroceryUpdateDTO, validate_create, validate_update

@dataclass
class CreateGrocery:
    repo: GroceryRepositoryPort
    def __call__(self, dto: GroceryCreateDTO) -> GroceryEntity:
        validate_create(dto)
        return self.repo.create(name=dto.name.strip(), location=dto.location.strip())

@dataclass
class UpdateGrocery:
    repo: GroceryRepositoryPort
    def __call__(self, uid: str, dto: GroceryUpdateDTO) -> GroceryEntity:
        validate_update(dto)
        fields = {}
        if dto.name is not None: fields["name"] = dto.name.strip()
        if dto.location is not None: fields["location"] = dto.location.strip()
        return self.repo.update_fields(uid=uid, **fields)

@dataclass
class DeleteGrocery:
    repo: GroceryRepositoryPort
    def __call__(self, uid: str) -> None:
        self.repo.soft_delete(uid=uid)
