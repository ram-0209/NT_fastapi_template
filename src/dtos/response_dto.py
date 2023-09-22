"""
    Common Schema for mapping response
"""
from sqlmodel import Field, SQLModel


class Response(SQLModel):
    """
    Class for constructing Response schema
    """

    message: str = Field(None, alias="message")
    status: str = Field(None, alias="status")
    data: str = Field(None, alias="data")
