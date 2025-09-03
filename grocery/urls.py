from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)



# import views
from apps.authn.interface.views import LoginView, RefreshView
from apps.groceries.interface.views import (
    GroceryAdminViewSet, GroceryItemViewSet, ItemDetailViewSet, GroceryIncomeViewSet
)
from apps.users.interface.views import SupplierAdminViewSet

# DRF router
router = DefaultRouter()
router.register(r"v1/groceries", GroceryAdminViewSet, basename="groceries")
router.register(r"v1/suppliers", SupplierAdminViewSet, basename="suppliers")

urlpatterns = [
    # auth endpoints
    path("api/v1/auth/login/", LoginView.as_view(), name="auth-login"),
    path("api/v1/auth/refresh/", RefreshView.as_view(), name="auth-refresh"),

    # groceries + suppliers (via router)
    path("api/", include(router.urls)),

    # items (explicit paths, not router)
    path(
        "api/v1/groceries/<str:grocery_uid>/items/",
        GroceryItemViewSet.as_view({"get": "list", "post": "create"}),
        name="grocery-items",
    ),
    path(
        "api/v1/items/<str:pk>/",
        ItemDetailViewSet.as_view({"patch": "partial_update", "delete": "destroy"}),
        name="item-detail",
    ),

    path(
        "api/v1/groceries/<str:grocery_uid>/income/",
        GroceryIncomeViewSet.as_view({"post": "create", "get": "list"}),
    ),



    # API Documentation Routes
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
