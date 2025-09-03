import logging
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status as http
from django.http import Http404
from django.core.exceptions import PermissionDenied

import traceback

logger = logging.getLogger("apps.api")


DEFAULT_TYPES = {
    http.HTTP_400_BAD_REQUEST:  "validation_failed",
    http.HTTP_401_UNAUTHORIZED: "unauthorized",
    http.HTTP_403_FORBIDDEN:    "forbidden",
    http.HTTP_404_NOT_FOUND:    "not_found",
    http.HTTP_409_CONFLICT:     "conflict",
    http.HTTP_422_UNPROCESSABLE_ENTITY: "unprocessable_entity",
    http.HTTP_429_TOO_MANY_REQUESTS: "rate_limited",
    http.HTTP_500_INTERNAL_SERVER_ERROR: "server_error",
}


def problem_response(request, *, status, title, code, detail=None, errors=None, type_slug=None):
    base_url = "https://api.example.com/errors/"
    body = {
        "type": base_url + (type_slug or "server_error"),
        "title": title,
        "status": status,
        "code": code,
        "detail": detail,
        "instance": request.get_full_path() if request else None,
        "errors": errors or {},
        "meta": {"trace_id": getattr(request, "trace_id", None)},
    }
    from rest_framework.response import Response
    return Response(body, status=status)

def drf_exception_handler(exc, context):
    request = context.get("request")

    # Log the exception with trace ID
    logger.error("-" * 70)
    logger.error(f"Trace ID: {getattr(request, 'trace_id', 'N/A')}")
    logger.error(f"Exception: {exc}")
    logger.error(traceback.format_exc())
    logger.error("-" * 70)
    
    # Map common exceptions
    if isinstance(exc, ValidationError):
        return problem_response(request, status=400, title="Validation failed",
                                code="VALIDATION_FAILED", detail="One or more fields are invalid.",
                                errors=exc.detail, type_slug="validation_failed")
    if isinstance(exc, Http404):
        return problem_response(request, status=404, title="Not found",
                                code="NOT_FOUND", detail="Resource not found.")
    if isinstance(exc, PermissionDenied):
        return problem_response(request, status=403, title="Forbidden",
                                code="FORBIDDEN", detail="You are not allowed to perform this action.")

    # Let DRF format other errors first
    response = exception_handler(exc, context)
    if response is not None :
        title = getattr(exc, "default_detail", "Error")
        code = getattr(exc, "default_code", "error").upper()
        return problem_response(request, status=response.status_code, title=str(title),
                                code=code, detail=str(title))

    return problem_response(request, status=500, title="Internal Server Error",
                            code="SERVER_ERROR", detail="An unexpected error occurred.")
