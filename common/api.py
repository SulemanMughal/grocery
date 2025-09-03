from rest_framework.response import Response

def ok(data=None, *, code="OK", message="OK", status=200, request=None, meta=None):
    payload = {
        "success": True,
        "code": code,
        "message": message,
        "data": data,
        "meta": {
            "version": getattr(request, "version", "1"),
            "trace_id": getattr(request, "trace_id", None),
        },
    }
    if meta:
        payload["meta"] |= meta
    return Response(payload, status=status)
