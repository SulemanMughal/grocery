from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.groceries.application.use_cases import CreateGrocery, UpdateGrocery, DeleteGrocery
from apps.groceries.application.validators import GroceryCreateDTO, GroceryUpdateDTO
from apps.groceries.infrastructure.repositories import Neo4jGroceryRepository
from .serializers import GroceryCreateSerializer, GroceryUpdateSerializer, GroceryOutSerializer, ItemCreateSerializer, ItemUpdateSerializer, ItemOutSerializer
from apps.groceries.interface.serializers import (
    DailyIncomeCreateSerializer, DailyIncomeOutSerializer
)
from apps.users.interface.permissions import IsAdminRole  # reuse from users app
from apps.groceries.infrastructure.repositories import Neo4jItemRepository, Neo4jDailyIncomeRepository
from common.api import ok
from common.exceptions import problem_response
from .permissions import SupplierOwnsTargetOrAdmin, AdminOrOwningSupplierOnGrocery
from common.api import ok

from drf_spectacular.utils import extend_schema, OpenApiResponse,OpenApiParameter
from common.schemas import Envelope, Problem


class GroceryAdminViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminRole]
    repo = Neo4jGroceryRepository()

    def get_serializer_class(self):
        if self.action in ("partial_update",):
            return GroceryUpdateSerializer
        if self.action in ("create",):
            return GroceryCreateSerializer
        return GroceryOutSerializer

    @extend_schema(
        tags=["Groceries"],
        summary="List groceries (Admin only)",
        description="Return all active grocery accounts. Not part of assessment core, but useful for admin QA/debug.",
        responses={
            200: OpenApiResponse(Envelope(GroceryOutSerializer(many=True)), description="Groceries list."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
        },
    )
    def list(self, request):
        data = list(self.repo.list_active())
        return ok(GroceryOutSerializer(data, many=True).data,
                  code="GROCERIES_LIST", message="Groceries fetched.", request=request)


    @extend_schema(
        tags=["Groceries"],
        summary="Retrieve grocery (Admin only)",
        description="Get details of a single grocery by UID.",
        responses={
            200: OpenApiResponse(Envelope(GroceryOutSerializer), description="Grocery details."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def retrieve(self, request, pk=None):
        g = self.repo.get_by_id(pk)
        if not g:
            return problem_response(
                request,
                status=status.HTTP_404_NOT_FOUND,
                title="Grocery not found.",
                code="GROCERY_NOT_FOUND",
                detail="Grocery not found or inactive.",
                errors={"id": ["Grocery not found or inactive."]},
                type_slug="not_found"
            )
        return ok(GroceryOutSerializer(g).data,
                  code="GROCERY_DETAIL", message="Grocery detail.", request=request)

    @extend_schema(
        tags=["Groceries"],
        summary="Create a new grocery (Admin)",
        request=GroceryCreateSerializer,
        responses={
            201: OpenApiResponse(Envelope(GroceryOutSerializer), description="Grocery created."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
        },
    )
    def create(self, request):
        ser = GroceryCreateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        dto = GroceryCreateDTO(**ser.validated_data)
        try:
            g = CreateGrocery(self.repo)(dto)
        except ValueError as e:
            return problem_response(
                request,
                status=status.HTTP_400_BAD_REQUEST,
                title="Validation failed.",
                code="VALIDATION_FAILED",
                detail=str(e),
                errors={"non_field_errors": [str(e)]},
                type_slug="validation_failed"
            )
        return ok(GroceryOutSerializer(g).data,
                  code="GROCERY_CREATED", message="Grocery created.", status=status.HTTP_201_CREATED, request=request)

    
    @extend_schema(
        tags=["Groceries"],
        summary="Update grocery (Admin, partial)",
        request=GroceryUpdateSerializer,
        responses={
            200: OpenApiResponse(Envelope(GroceryOutSerializer), description="Grocery updated."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def partial_update(self, request, pk=None):
        ser = GroceryUpdateSerializer(data=request.data, partial=True); ser.is_valid(raise_exception=True)
        dto = GroceryUpdateDTO(**ser.validated_data)
        try:
            g = UpdateGrocery(self.repo)(pk, dto)
        except ValueError as e:
            return problem_response(
                request,
                status=status.HTTP_400_BAD_REQUEST,
                title="Validation failed.",
                code="VALIDATION_FAILED",
                detail=str(e),
                errors={"non_field_errors": [str(e)]},
                type_slug="validation_failed"
            )
        return ok(GroceryOutSerializer(g).data,
                  code="GROCERY_UPDATED", message="Grocery updated.", request=request)

    
    @extend_schema(
        tags=["Groceries"],
        summary="Soft-delete grocery (Admin)",
        responses={
            204: OpenApiResponse(description="Grocery soft-deleted."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def destroy(self, request, pk=None):
        DeleteGrocery(self.repo)(pk)
        return ok(None, code="GROCERY_DELETED", message="Grocery deleted (soft).",
                  status=status.HTTP_204_NO_CONTENT, request=request)
    

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        pass



class GroceryItemViewSet(viewsets.ViewSet):
    """
    Routes:
      GET  /api/v1/groceries/{grocery_uid}/items/       -> list
      POST /api/v1/groceries/{grocery_uid}/items/       -> create
    """
    permission_classes = [IsAuthenticated, SupplierOwnsTargetOrAdmin]
    repo = Neo4jItemRepository()

    @extend_schema(
        tags=["Items"],
        summary="List items for a grocery (any authenticated)",
        responses={
            200: OpenApiResponse(Envelope(ItemOutSerializer(many=True)), description="Items list."),
            401: Problem("unauthorized"),
        },
    )
    def list(self, request, grocery_uid=None):
        items = list(self.repo.list_by_grocery(grocery_uid=grocery_uid, include_deleted=False))
        return ok(ItemOutSerializer(items, many=True).data,
                  code="ITEMS_LIST", message="Items fetched.", request=request)

    @extend_schema(
        tags=["Items"],
        summary="Create item for a grocery (Admin or owning Supplier)",
        request=ItemCreateSerializer,
        responses={
            201: OpenApiResponse(Envelope(ItemOutSerializer), description="Item created."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def create(self, request, grocery_uid=None):
        ser = ItemCreateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        try:
            item = self.repo.create(grocery_uid=grocery_uid, **ser.validated_data)
        except ValueError as e:
            return problem_response(
                request,
                status=status.HTTP_400_BAD_REQUEST,
                title="Validation failed.",
                code="VALIDATION_FAILED",
                detail=str(e),
                errors={"non_field_errors": [str(e)]},
                type_slug="validation_failed"
            )
        return ok(ItemOutSerializer(item).data,
                  code="ITEM_CREATED", message="Item created.",
                  status=status.HTTP_201_CREATED, request=request)

class ItemDetailViewSet(viewsets.ViewSet):
    """
      PATCH /api/v1/items/{item_uid}/
      DELETE /api/v1/items/{item_uid}/
    """
    permission_classes = [IsAuthenticated, SupplierOwnsTargetOrAdmin]
    repo = Neo4jItemRepository()


    @extend_schema(
        tags=["Items"],
        summary="Update item (Admin or owning Supplier, partial)",
        request=ItemUpdateSerializer,
        responses={
            200: OpenApiResponse(Envelope(ItemOutSerializer), description="Item updated."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def partial_update(self, request, pk=None):
        ser = ItemUpdateSerializer(data=request.data, partial=True); ser.is_valid(raise_exception=True)
        try:
            updated = self.repo.update_fields(uid=pk, **ser.validated_data)
        except ValueError as e:
            return problem_response(
                request,
                status=status.HTTP_400_BAD_REQUEST,
                title="Validation failed.",
                code="VALIDATION_FAILED",
                detail=str(e),
                errors={"non_field_errors": [str(e)]},
                type_slug="validation_failed"
            )
        return ok(ItemOutSerializer(updated).data,
                  code="ITEM_UPDATED", message="Item updated.", request=request)


    @extend_schema(
        tags=["Items"],
        summary="Soft-delete item (Admin or owning Supplier)",
        responses={
            204: OpenApiResponse(description="Item soft-deleted."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def destroy(self, request, pk=None):
        self.repo.soft_delete(uid=pk)
        return ok(None, code="ITEM_DELETED", message="Item deleted (soft).",
                  status=status.HTTP_204_NO_CONTENT, request=request)



class GroceryIncomeViewSet(viewsets.ViewSet):
    """
    Routes:
      POST /api/v1/groceries/{grocery_uid}/income/   -> create (Admin or owning Supplier)
      GET  /api/v1/groceries/{grocery_uid}/income/   -> list  (Admin; Supplier only for their grocery)
        optional query params: ?start=YYYY-MM-DD&end=YYYY-MM-DD
    """
    permission_classes = [IsAuthenticated, AdminOrOwningSupplierOnGrocery]
    repo = Neo4jDailyIncomeRepository()


    @extend_schema(
        tags=["Income"],
        summary="Add daily income (Admin or owning Supplier)",
        request=DailyIncomeCreateSerializer,
        responses={
            201: OpenApiResponse(Envelope(DailyIncomeOutSerializer), description="Income recorded."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def create(self, request, grocery_uid=None):
        ser = DailyIncomeCreateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        try:
            rec = self.repo.create(grocery_uid=grocery_uid, **ser.validated_data)
        except ValueError as e:
            return problem_response(
                request,
                status=status.HTTP_400_BAD_REQUEST,
                title="Validation failed.",
                code="VALIDATION_FAILED",
                detail=str(e),
                errors={"non_field_errors": [str(e)]},
                type_slug="validation_failed"
            )
        return ok(DailyIncomeOutSerializer(rec).data,
                  code="INCOME_ADDED", message="Income recorded.",
                  status=status.HTTP_201_CREATED, request=request)


    @extend_schema(
        tags=["Income"],
        summary="List daily income (Admin any grocery; Supplier only their grocery)",
        parameters=[
            OpenApiParameter(name="start", location=OpenApiParameter.QUERY, required=False, description="YYYY-MM-DD"),
            OpenApiParameter(name="end",   location=OpenApiParameter.QUERY, required=False, description="YYYY-MM-DD"),
        ],
        responses={
            200: OpenApiResponse(Envelope(DailyIncomeOutSerializer(many=True)), description="Income list."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
        },
    )
    def list(self, request, grocery_uid=None):
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        data = list(self.repo.list_by_grocery(grocery_uid=grocery_uid, start=start, end=end))
        return ok(DailyIncomeOutSerializer(data, many=True).data,
                  code="INCOME_LIST", message="Income fetched.", request=request)