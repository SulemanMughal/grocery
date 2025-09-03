from typing import Iterable, Optional
from neomodel import db
from apps.groceries.domain.entities import GroceryEntity, ItemEntity,DailyIncomeEntity
from apps.groceries.domain.repositories import GroceryRepositoryPort, ItemRepositoryPort, DailyIncomeRepositoryPort
from .models import GroceryNode, ItemNode,DailyIncomeNode


def _to_entity(n: GroceryNode) -> GroceryEntity:
    return GroceryEntity(
        id=n.uid, name=n.name, location=n.location,
        is_active=bool(n.is_active),
        created_at=n.created_at, updated_at=n.updated_at
    )

def _to_item_entity(n: ItemNode) -> ItemEntity:
    return ItemEntity(
        id=n.uid,
        name=n.name,
        item_type=n.item_type,
        item_location=n.item_location,
        price=n.price,
        is_deleted=bool(n.is_deleted),
        created_at=n.created_at,
        updated_at=n.updated_at,
    )

def _to_income_entity(n: DailyIncomeNode, grocery_uid: str | None = None) -> DailyIncomeEntity:
    return DailyIncomeEntity(
        id=n.uid,
        amount=n.amount,
        date=n.date,
        created_at=n.created_at,
        updated_at=n.updated_at,
    )


class Neo4jGroceryRepository(GroceryRepositoryPort):
    def create(self, *, name: str, location: str) -> GroceryEntity:
        g = GroceryNode(name=name, location=location)
        g.touch(); g.save()
        return _to_entity(g)

    def get_by_id(self, uid: str) -> Optional[GroceryEntity]:
        g = GroceryNode.nodes.get_or_none(uid=uid, is_active=True)
        return _to_entity(g) if g else None

    def list_active(self) -> Iterable[GroceryEntity]:
        # Simple scan; for big graphs, prefer a Cypher with WHERE is_active true
        for g in GroceryNode.nodes.filter(is_active=True):
            yield _to_entity(g)

    def update_fields(self, *, uid: str, **fields) -> GroceryEntity:
        g = GroceryNode.nodes.get(uid=uid)
        if not g.is_active:
            # optional: forbid updating inactive groceries
            pass
        for k, v in fields.items():
            setattr(g, k, v)
        g.touch(); g.save()
        return _to_entity(g)

    def soft_delete(self, *, uid: str) -> None:
        g = GroceryNode.nodes.get(uid=uid)
        g.is_active = False
        g.touch(); g.save()


class Neo4jItemRepository(ItemRepositoryPort):
    def create(self, *, grocery_uid: str, name: str, item_type: str,
               item_location: str, price: float) -> ItemEntity:
        g = GroceryNode.nodes.get(uid=grocery_uid, is_active=True)
        i = ItemNode(name=name, item_type=item_type,
                     item_location=item_location, price=float(price))
        i.touch(); i.save()
        g.sells.connect(i)
        return _to_item_entity(i)

    def get_by_id(self, uid: str) -> Optional[ItemEntity]:
        i = ItemNode.nodes.get_or_none(uid=uid, is_deleted=False)
        return _to_item_entity(i) if i else None

    def list_by_grocery(self, grocery_uid: str, include_deleted: bool=False) -> Iterable[ItemEntity]:
        q = """
        MATCH (g:Grocery {uid:$gid})-[:SELLS]->(i:Item)
        WHERE $include OR i.is_deleted = false
        RETURN i
        """
        res, _ = db.cypher_query(q, {"gid": grocery_uid, "include": include_deleted})
        for row in res:
            yield _to_item_entity(ItemNode.inflate(row[0]))

    def update_fields(self, *, uid: str, **fields) -> ItemEntity:
        i = ItemNode.nodes.get(uid=uid)
        for k, v in fields.items():
            setattr(i, k, v)
        i.touch(); i.save()
        return _to_item_entity(i)

    def soft_delete(self, *, uid: str) -> None:
        i = ItemNode.nodes.get(uid=uid)
        i.is_deleted = True
        i.touch(); i.save()

    def get_item_grocery_uid(self, *, item_uid: str) -> Optional[str]:
        q = """
        MATCH (g:Grocery)-[:SELLS]->(i:Item {uid:$item})
        RETURN g.uid LIMIT 1
        """
        res, _ = db.cypher_query(q, {"item": item_uid})
        return res[0][0] if res else None


class Neo4jDailyIncomeRepository(DailyIncomeRepositoryPort):
    def create(self, *, grocery_uid: str, amount: float, date: str) -> DailyIncomeEntity:
        g = GroceryNode.nodes.get(uid=grocery_uid, is_active=True)
        d = DailyIncomeNode(amount=float(amount), date=date)
        d.touch(); d.save()
        g.reports.connect(d)
        return _to_income_entity(d, grocery_uid)

    def list_by_grocery(self, grocery_uid: str, start: str | None = None, end: str | None = None) -> Iterable[DailyIncomeEntity]:
        q = """
        MATCH (g:Grocery {uid:$gid})-[:REPORTS]->(d:DailyIncome)
        WHERE ($start IS NULL OR date(d.date) >= date($start))
          AND ($end   IS NULL OR date(d.date) <= date($end))
        RETURN d ORDER BY d.date ASC
        """
        res, _ = db.cypher_query(q, {"gid": grocery_uid, "start": start, "end": end})
        for row in res:
            yield _to_income_entity(DailyIncomeNode.inflate(row[0]), grocery_uid)
