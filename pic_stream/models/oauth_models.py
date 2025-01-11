""" Pydantic data classes for oAuth"""

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings


class GoogleAuth(BaseModel):
    client_id: int
    callback_url: str
    scopes: list[str]


class GoogleSecrets(BaseSettings):
    client_secret: SecretStr
    session_secret: SecretStr
