import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from w.exceptions import WError

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """

    Args:
        exc(Exception|CommonError): exception
        context:

    Returns:

    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = drf_exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is None:
        if isinstance(exc, WError):
            response = Response(exc.get_message(), status=exc.get_code())
        else:
            logger.error(str(exc))
            response = Response(str(exc), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
