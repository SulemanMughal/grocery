from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.application.use_cases import CreateUser, UpdateUser, SoftDeleteUser, CreateSupplierAndAssign
from apps.users.application.validators import UserCreateDTO
from apps.users.infrastructure.repositories import Neo4jUserRepository
from .serializers import UserCreateSerializer, UserOutSerializer, UserUpdateSerializer,SupplierCreateSerializer
from .permissions import IsAdminRole
from rest_framework.exceptions import ValidationError
from common.api import ok
from common.exceptions import problem_response

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample,OpenApiParameter, OpenApiTypes
from common.schemas import Envelope, Problem


class UserAdminViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = [IsAdminRole]
    repo = Neo4jUserRepository()

    def list(self, request):
        items = list(self.repo.list())
        data = UserOutSerializer(items, many=True).data
        return ok(
            data,
            code="USER_LIST",
            message="User list retrieved.",
            status=status.HTTP_200_OK,
            request=request
        )

    def retrieve(self, request, pk=None):
        u = self.repo.get_by_id(pk)
        if not u:
            
            return problem_response(
                request,
                status=status.HTTP_404_NOT_FOUND,
                title="User not found.",
                code="USER_NOT_FOUND",
                detail="No user found with the given ID.",
                type_slug="not_found"
            )
        return ok(
            UserOutSerializer(u).data,
            code="USER_RETRIEVED",
            message="User retrieved.",
            status=status.HTTP_200_OK,
            request=request
        )

    @extend_schema(
        tags=["Suppliers"],
        summary="Create supplier & assign to grocery (Admin)",
        request=SupplierCreateSerializer,
        examples=[
            OpenApiExample("Create supplier",
                           value={"name":"Sam","email":"sam@supply.com","password":"StrongP@ss1","grocery_uid":"<gid>"},
                           request_only=True)
        ],
        responses={
            201: OpenApiResponse(Envelope(UserOutSerializer), description="Supplier created & assigned."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def create(self, request, *args, **kwargs):
        ser = UserCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        dto = UserCreateDTO(**ser.validated_data)
        try:
            u = CreateUser(self.repo)(dto)
        except ValueError as e:
            # Domain validation → 400
            return problem_response(
                request,
                status=status.HTTP_400_BAD_REQUEST,
                title="Validation failed.",
                code="VALIDATION_FAILED",
                detail=str(e),
                errors={"non_field_errors": [str(e)]},
                type_slug="validation_failed"
            )
        return ok(UserOutSerializer(u).data,
                  code="USER_CREATED", message="User created.", status=status.HTTP_201_CREATED, request=request)


    @extend_schema(
        tags=["Suppliers"],
        summary="Update supplier (Admin, partial)",
        request=UserUpdateSerializer,
        responses={
            200: OpenApiResponse(Envelope(UserOutSerializer), description="Supplier updated."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def partial_update(self, request, pk=None):
        ser = UserUpdateSerializer(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        u = UpdateUser(self.repo)(pk, **ser.validated_data)
        return ok(
            UserOutSerializer(u).data,
            code="USER_UPDATED",
            message="User updated.",
            status=status.HTTP_200_OK,
            request=request
        )


    @extend_schema(
        tags=["Suppliers"],
        summary="Soft-delete supplier (Admin)",
        responses={
            204: OpenApiResponse(description="Supplier soft-deleted."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def destroy(self, request, pk=None):
        SoftDeleteUser(self.repo)(pk)
        return ok(
            {},
            code="USER_DELETED",
            message="User deleted.",
            status=status.HTTP_204_NO_CONTENT,
            request=request
        )



class SupplierAdminViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsAdminRole]
    repo = Neo4jUserRepository()

    def get_serializer_class(self):
        return SupplierCreateSerializer if self.action == "create" else UserUpdateSerializer


    @extend_schema(
        tags=["Suppliers"],
        summary="Create supplier & assign to grocery (Admin only)",
        description="Create a new supplier account, hash the password, and assign them as responsible for a grocery via a `RESPONSIBLE_FOR` relationship.",
        request=SupplierCreateSerializer,
        responses={
            201: OpenApiResponse(Envelope(UserOutSerializer), description="Supplier created & assigned."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def create(self, request, *args, **kwargs):
        ser = SupplierCreateSerializer(data=request.data); ser.is_valid(raise_exception=True)
        try:
            u = CreateSupplierAndAssign(self.repo)(
                name=ser.validated_data["name"],
                email=ser.validated_data["email"],
                password=ser.validated_data["password"],
                grocery_uid=ser.validated_data["grocery_uid"],
            )
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
        return ok(UserOutSerializer(u).data,
                  code="SUPPLIER_CREATED", message="Supplier created and assigned.",
                  status=status.HTTP_201_CREATED, request=request)


    @extend_schema(
        tags=["Suppliers"],
        summary="Update supplier (Admin only, partial)",
        description="Update fields like name or role for a supplier. Automatically refreshes `updated_at`.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="The **UID of the Supplier** (Neo4j `UserNode.uid`) to update."
            )
        ],
        request=UserUpdateSerializer,
        responses={
            200: OpenApiResponse(Envelope(UserOutSerializer), description="Supplier updated."),
            400: Problem("validation_error"),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def partial_update(self, request, pk=None):
        ser = UserUpdateSerializer(data=request.data, partial=True); ser.is_valid(raise_exception=True)
        try:
            u = UpdateUser(self.repo)(pk, **ser.validated_data)
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
        return ok(UserOutSerializer(u).data,
                  code="SUPPLIER_UPDATED", message="Supplier updated.", request=request)


    @extend_schema(
        tags=["Suppliers"],
        summary="Soft-delete supplier (Admin only)",
        description="Mark a supplier as inactive (`is_active=false`). Account is not removed from Neo4j, preserving history.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="The **UID of the Supplier** (Neo4j `UserNode.uid`) to delete."
            )
        ],
        responses={
            204: OpenApiResponse(description="Supplier soft-deleted."),
            401: Problem("unauthorized"),
            403: Problem("forbidden"),
            404: Problem("not_found"),
        },
    )
    def destroy(self, request, pk=None):
        SoftDeleteUser(self.repo)(pk)
        return ok(None, code="SUPPLIER_DELETED", message="Supplier deleted (soft).",
                  status=status.HTTP_204_NO_CONTENT, request=request)
    


    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        pass