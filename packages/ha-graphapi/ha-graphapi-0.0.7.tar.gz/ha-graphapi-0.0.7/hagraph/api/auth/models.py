"""Authentication Models."""
from typing import Optional

from pydantic import BaseModel, Field


class OAuth2TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: Optional[str]
