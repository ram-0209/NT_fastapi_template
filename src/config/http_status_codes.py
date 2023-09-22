"""
    Enums for HTTP Status CodesS
"""
from enum import Enum


class HttpStatusCodes:
    """
    Nested Classes for StatusCodes response and StatusCodesDesription response
    """

    def __init__(self):
        # Empty init class
        pass

    class StatusCodes(Enum):
        """
        Enums for StatusCodes
        """

        SUCCESS_OK_200: int = 200
        BAD_REQUEST_400: int = 400
        UNAUTHORIZED_401: int = 401
        INCORRECT_FILE_FORMAT_301: int = 301
        CONTENT_NOT_FOUND_204: int = 204
        FORBIDDEN_403: int = 403
        NOT_FOUND_404: int = 404
        INTERNAL_SERVER_ERROR_500: int = 500
        NOT_IMPLEMENTED_501: int = 501

    class StatusCodesDescription(Enum):
        """
        Enums for StatusCodesDescription
        """

        SUCCESS_OK_200: str = "Ok"
        BAD_REQUEST_400: str = "Bad Request"
        UNAUTHORIZED_401: str = "Unauthorized"
        INCORRECT_FILE_FORMAT_301: str = "File is not of correct format"
        FORBIDDEN_403: str = "Forbidden"
        CONTENT_NOT_FOUND_204: str = "Content Not Found"
        NOT_FOUND_404: str = "Not Found"
        INTERNAL_SERVER_ERROR_500: str = "Internal Server Error"
        NOT_IMPLEMENTED_501: str = "Not Implemented"
