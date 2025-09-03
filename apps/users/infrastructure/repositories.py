from datetime import datetime
from typing import Iterable, Optional
from .models import UserNode
from apps.groceries.infrastructure.models import GroceryNode
from apps.users.domain.entities import UserEntity
from apps.users.domain.repositories import UserRepositoryPort

def _to_entity(n: UserNode) -> UserEntity:
    return UserEntity(
        id=n.uid, name=n.name, email=n.email, role=n.role,
        is_active=bool(n.is_active),
        created_at=n.created_at, updated_at=n.updated_at
    )

class Neo4jUserRepository(UserRepositoryPort):
    # create supplier + assign (used earlier)
    def create_supplier_and_assign(self, *, name: str, email: str,
                                   password_hash: str, grocery_uid: str) -> UserEntity:
        g = GroceryNode.nodes.get_or_none(uid=grocery_uid, is_active=True)
        if not g: raise ValueError("Grocery not found.")
        u = UserNode(name=name, email=email, password=password_hash, role="SUPPLIER")
        u.touch(); u.save()
        u.responsible_for.connect(g)
        return _to_entity(u)


    def create(self, *, name: str, email: str, password_hash: str, role: str) -> UserEntity:
        node = UserNode(name=name, email=email, password=password_hash, role=role)
        node.touch()
        node.save()
        return _to_entity(node)

    def get_by_id(self, user_id: str) -> Optional[UserEntity]:
        n = UserNode.nodes.get_or_none(uid=user_id)
        return _to_entity(n) if n else None

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        n = UserNode.nodes.first_or_none(email=email)
        return _to_entity(n) if n else None

    def list(self) -> Iterable[UserEntity]:
        for n in UserNode.nodes:
            yield _to_entity(n)

    def update(self, user_id: str, **fields) -> UserEntity:
        n = UserNode.nodes.get(uid=user_id)
        for k, v in fields.items():
            setattr(n, k, v)
        n.touch()
        n.save()
        return _to_entity(n)

    def soft_delete(self, user_id: str) -> None:
        n = UserNode.nodes.get(uid=user_id)
        n.is_active = False
        n.touch()
        n.save()
