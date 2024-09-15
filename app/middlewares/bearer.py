"""This module provides `BearerTokenAuthorizationMiddleware`"""

from fastapi import Request, Response, status


class BearerTokenAuthorizationMiddleware:
    """This class contains Bearer token authorization functionality"""

    def __init__(self, token: str):
        """
        Initialization

        :param token: Secret token
        """
        self.__token = token

    async def __call__(self, request: Request, call_next):
        """
        This method checks the request Authorization header

        :param request: Request instance
        :param call_next: Function, that will be called after the middleware completed
        """

        auth_header = request.headers.get('Authorization')

        if auth_header:
            token_type, token = auth_header.split()
            if token_type.lower() == 'bearer' and token == self.__token:
                return await call_next(request)

        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
