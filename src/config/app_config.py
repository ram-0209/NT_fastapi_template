"""Contains config defined in core"""
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    """Base Settings Class"""

    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """assemble_cors_origins

        Args:
            v (Union[str, List[str]])

        Raises:
            ValueError: ValueError(v)

        Returns:
            Union[List[str], str]: v
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        """Config Class"""

        case_sensitive = True
        env_file = ".env"


settings = Settings(PROJECT_NAME="TEMPLATE_SERVICE")
SCHEMA = "test"
