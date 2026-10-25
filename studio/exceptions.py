from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.views import exception_handler

ERROR_CODES = {
    status.HTTP_400_BAD_REQUEST: "validation_error",
    status.HTTP_404_NOT_FOUND: "not_found",
    status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
    status.HTTP_409_CONFLICT: "conflict",
}


class ConflictError(APIException):

    status_code = status.HTTP_409_CONFLICT
    default_detail = "Конфлікт із поточним станом даних."
    default_code = "conflict"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    error = {"code": ERROR_CODES.get(response.status_code, "error")}
    if isinstance(exc, ValidationError):
        error["message"] = "Невалідні дані. Деталі в полі details."
        error["details"] = response.data
    else:
        error["message"] = str(exc.detail)
    response.data = {"error": error}
    return response


