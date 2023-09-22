"""
    Contains common json response structure
"""
from src.config.http_status_codes import HttpStatusCodes
from src.dtos.response_dto import Response


def create_response(message: str, status: str, data: str = None):
    """function for mapping the response

    Args:
        message (str): Response Message
        status (str): Response Status
        data (str, optional): Response Data. Defaults to None.

    Returns:
        _type_: Final Response
    """
    final_response = Response()
    final_response.message = message
    final_response.status = status
    final_response.data = data
    return final_response


def create_api_response(
    success: bool, result=None, success_message=None, failure_message=None
):
    """Function for API Response

    Args:
        success (bool): Success or Failure
        result (_type_, optional): Result. Defaults to None.
        success_message (_type_, optional): Success message. Defaults to None.
        failure_message (_type_, optional): Failure Message. Defaults to None.

    Returns:
        _type_: create_response function
    """
    if success:
        status_code = HttpStatusCodes.StatusCodes.SUCCESS_OK_200
        status_description = (
            success_message
            if success_message
            else HttpStatusCodes.StatusCodesDescription.SUCCESS_OK_200
        )
    else:
        status_code = HttpStatusCodes.StatusCodes.NOT_FOUND_404
        status_description = (
            failure_message
            if failure_message
            else HttpStatusCodes.StatusCodesDescription.NOT_FOUND_404
        )

    return create_response(status_description, status_code, result)
