from rest_framework import serializers

class MetaSerializer(serializers.Serializer):
    version = serializers.CharField()
    trace_id = serializers.CharField(allow_null=True)

def Envelope(inner):
    class _Env(serializers.Serializer):
        success = serializers.BooleanField()
        code = serializers.CharField()
        message = serializers.CharField()
        data = inner() if isinstance(inner, type) else inner
        meta = MetaSerializer()
    return _Env

class ProblemSerializer(serializers.Serializer):
    type = serializers.CharField()
    title = serializers.CharField()
    status = serializers.IntegerField()
    code = serializers.CharField()
    detail = serializers.CharField(required=False, allow_blank=True)
    instance = serializers.CharField(required=False)
    errors = serializers.DictField(required=False)
    meta = MetaSerializer()

def Problem(_slug: str = "server_error"):
    return ProblemSerializer



