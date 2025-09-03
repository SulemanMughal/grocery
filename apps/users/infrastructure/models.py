from neomodel import StructuredNode, UniqueIdProperty, StringProperty, BooleanProperty, DateTimeProperty, RelationshipTo
from datetime import datetime, timezone


ROLE_CHOICES = {
    "ADMIN": "ADMIN",
    "SUPPLIER": "SUPPLIER",
}

class UserNode(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    email = StringProperty(required=True, unique_index=True, lowercase=True, trim=True)
    password = StringProperty(required=True)         # hashed
    role = StringProperty(required=True, choices=ROLE_CHOICES)
    is_active = BooleanProperty(default=True)

    # Use timezone-aware UTC for defaults
    created_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeProperty(default=lambda: datetime.now(timezone.utc))

    manages = RelationshipTo("apps.groceries.infrastructure.models.GroceryNode", "MANAGES")
    responsible_for = RelationshipTo("apps.groceries.infrastructure.models.GroceryNode", "RESPONSIBLE_FOR")



    def touch(self):
        # Always set timezone-aware UTC
        self.updated_at = datetime.now(timezone.utc)
