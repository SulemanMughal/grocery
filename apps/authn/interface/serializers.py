from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenPairOutSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class AccessOutSerializer(serializers.Serializer):
    access = serializers.CharField()