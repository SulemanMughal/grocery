from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.users.infrastructure.models import UserNode
from apps.groceries.infrastructure.models import GroceryNode
from apps.groceries.infrastructure.repositories import Neo4jItemRepository

class SupplierOwnsTargetOrAdmin(BasePermission):
    """
    - SAFE methods: allow (any authenticated user will be enforced at view level).
    - CREATE under /groceries/{grocery_uid}/items: Supplier must be responsible for that grocery OR Admin.
    - PATCH/DELETE /items/{item_uid}: Supplier must own that item's grocery OR Admin.
    """
    def has_permission(self, request, view):
        role = getattr(request.user, "role", None)
        if request.method in SAFE_METHODS:
            return True  # read allowed to all authed users

        if role == "ADMIN":
            return True

        if role != "SUPPLIER":
            return False

        # Supplier write: verify ownership
        user_uid = getattr(request.user, "id", None)
        if not user_uid:  # no principal
            return False

        # Create: grocery_uid in URL kwarg
        grocery_uid = view.kwargs.get("grocery_uid")
        if grocery_uid:
            u = UserNode.nodes.get_or_none(uid=user_uid, is_active=True)
            g = GroceryNode.nodes.get_or_none(uid=grocery_uid, is_active=True)
            return bool(u and g and u.responsible_for.is_connected(g))

        # Update/Delete: we have item uid (pk)
        item_uid = view.kwargs.get("pk")
        if item_uid:
            repo = Neo4jItemRepository()
            g_uid = repo.get_item_grocery_uid(item_uid=item_uid)
            if not g_uid:
                return False
            u = UserNode.nodes.get_or_none(uid=user_uid, is_active=True)
            g = GroceryNode.nodes.get_or_none(uid=g_uid, is_active=True)
            return bool(u and g and u.responsible_for.is_connected(g))

        return False



class AdminOrOwningSupplierOnGrocery(BasePermission):
    """
    Applies to income endpoints that include grocery_uid in path.
    - Admin: always allowed
    - Supplier: allowed only if they are RESPONSIBLE_FOR that grocery
    """
    def has_permission(self, request, view):
        role = getattr(request.user, "role", None)
        grocery_uid = view.kwargs.get("grocery_uid")
        if not grocery_uid:
            return False

        if role == "ADMIN":
            return True

        if role != "SUPPLIER":
            return False

        user_uid = getattr(request.user, "id", None)
        if not user_uid:
            return False

        u = UserNode.nodes.get_or_none(uid=user_uid, is_active=True)
        g = GroceryNode.nodes.get_or_none(uid=grocery_uid, is_active=True)
        return bool(u and g and u.responsible_for.is_connected(g))
