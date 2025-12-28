from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Global exception handler for consistent API errors
    """
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                "error": {
                    "code": response.status_code,
                    "message": response.data,
                }
            },
            status=response.status_code,
        )

    # Fallback for unhandled exceptions
    return Response(
        {
            "error": {
                "code": "SERVER_ERROR",
                "message": "Something went wrong. Please try again later.",
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
