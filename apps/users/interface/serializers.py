from rest_framework import serializers

class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.ChoiceField(choices=["ADMIN", "SUPPLIER"])


class SupplierCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    grocery_uid = serializers.CharField()

class UserOutSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120, required=False)
    role = serializers.ChoiceField(choices=["ADMIN", "SUPPLIER"], required=False)
