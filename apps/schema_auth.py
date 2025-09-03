# schema.py
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

class GlobalHeaderAuthSchema(AutoSchema):
    def get_override_parameters(self):
        params = super().get_override_parameters() or []
        params.append(
            OpenApiParameter(
                name="Authorization",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='JWT access token header. Example: **Bearer eyJhbGciOi...**',
                required=False,  # keep False so it doesn't mark every op as required
            )
        )
        return params
