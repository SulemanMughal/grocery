import uuid
from common.logging_filters import trace_id_var  # see step 2

class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # allow client-provided ID, else generate one
        trace_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.trace_id = trace_id

        # push into ContextVar so logging can read it
        token = trace_id_var.set(trace_id)
        try:
            response = self.get_response(request)
        finally:
            trace_id_var.reset(token)

        response["X-Request-ID"] = trace_id
        return response


