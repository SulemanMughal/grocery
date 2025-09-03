from dataclasses import dataclass
from django.contrib.auth.hashers import make_password
from apps.users.domain.repositories import UserRepositoryPort
from apps.users.domain.entities import UserEntity
from .validators import UserCreateDTO, validate_user_create


@dataclass
class CreateUser:
    repo: UserRepositoryPort
    def __call__(self, dto: UserCreateDTO) -> UserEntity:
        validate_user_create(dto)
        if self.repo.get_by_email(dto.email.lower().strip()):
            raise ValueError("Email already exists")
        return self.repo.create(
            name=dto.name.strip(),
            email=dto.email.lower().strip(),
            password_hash=make_password(dto.password),
            role=dto.role
        )


@dataclass
class CreateSupplierAndAssign:
    repo: UserRepositoryPort
    def __call__(self, *, name: str, email: str, password: str, grocery_uid: str) -> UserEntity:
        if len(password) < 8: raise ValueError("Password too short (min 8).")
        if self.repo.get_by_email(email.lower().strip()):
            raise ValueError("Email already exists.")
        return self.repo.create_supplier_and_assign(
            name=name.strip(), email=email.lower().strip(),
            password_hash=make_password(password),
            grocery_uid=grocery_uid
        )


@dataclass
class UpdateUser:
    repo: UserRepositoryPort
    def __call__(self, user_id: str, *, name: str | None = None, role: str | None = None) -> UserEntity:
        fields = {}
        if name: fields["name"] = name.strip()
        if role:
            if role not in ("ADMIN", "SUPPLIER"):
                raise ValueError("Invalid role")
            fields["role"] = role
        if not fields:
            raise ValueError("Nothing to update")
        return self.repo.update(user_id, **fields)

@dataclass
class SoftDeleteUser:
    repo: UserRepositoryPort
    def __call__(self, user_id: str) -> None:
        self.repo.soft_delete(user_id)
