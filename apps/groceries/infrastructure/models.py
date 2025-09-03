from datetime import datetime, timezone
from neomodel import (
    StructuredNode, UniqueIdProperty, StringProperty,
    BooleanProperty, DateTimeProperty, RelationshipFrom, RelationshipTo,
    FloatProperty,
    DateProperty
)

class GroceryNode(StructuredNode):
    # ⚠️ don't use "id" (reserved by neomodel for element id)
    uid = UniqueIdProperty()                         # app PK (UUID string)
    name = StringProperty(required=True, index=True)
    location = StringProperty(required=True)
    is_active = BooleanProperty(default=True)        # soft-delete flag

    created_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))

    # Relationships (direction is a design choice; these are convenient):
    managed_by = RelationshipFrom("apps.users.infrastructure.models.UserNode", "MANAGES")
    suppliers  = RelationshipFrom("apps.users.infrastructure.models.UserNode", "RESPONSIBLE_FOR")
    sells      = RelationshipTo("apps.groceries.infrastructure.models.ItemNode", "SELLS")
    reports    = RelationshipTo("apps.groceries.infrastructure.models.DailyIncomeNode", "REPORTS")

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)



class ItemNode(StructuredNode):
    uid = UniqueIdProperty()                         # app PK (UUID string)
    name = StringProperty(required=True, index=True)
    item_type = StringProperty(required=True)        # e.g. food, game
    item_location = StringProperty(required=True)    # e.g. first roof, shelf 2
    price = FloatProperty(required=True)             # item price
    is_deleted = BooleanProperty(default=False)      # soft-delete flag

    created_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))

    # Belongs to a Grocery
    belongs_to = RelationshipFrom("apps.groceries.infrastructure.models.GroceryNode", "SELLS")

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)



class DailyIncomeNode(StructuredNode):
    uid = UniqueIdProperty()              # app PK (UUID string)
    amount = FloatProperty(required=True) # daily revenue
    date = DateProperty(required=True)    # YYYY-MM-DD

    created_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))

    # belongs to a grocery
    of_grocery = RelationshipFrom("apps.groceries.infrastructure.models.GroceryNode", "REPORTS")

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)