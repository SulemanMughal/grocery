from rest_framework import serializers

class GroceryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120)
    location = serializers.CharField(min_length=2, max_length=200)

class GroceryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=120, required=False)
    location = serializers.CharField(min_length=2, max_length=200, required=False)

class GroceryOutSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    location = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class ItemCreateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=120)
    item_type = serializers.CharField(min_length=1, max_length=60)
    item_location = serializers.CharField(min_length=1, max_length=120)
    price = serializers.FloatField(min_value=0)

class ItemUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=120, required=False)
    item_type = serializers.CharField(min_length=1, max_length=60, required=False)
    item_location = serializers.CharField(min_length=1, max_length=120, required=False)
    price = serializers.FloatField(min_value=0, required=False)

class ItemOutSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    item_type = serializers.CharField()
    item_location = serializers.CharField()
    price = serializers.FloatField()
    is_deleted = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class DailyIncomeCreateSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=0)
    date = serializers.DateField()  # "YYYY-MM-DD"

class DailyIncomeOutSerializer(serializers.Serializer):
    id = serializers.CharField()
    amount = serializers.FloatField()
    date = serializers.DateField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
