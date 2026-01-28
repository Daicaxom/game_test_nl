"""
Authentication Pydantic Schemas
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Registration request schema"""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    display_name: Optional[str] = Field(default=None, max_length=100)


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: int = Field(description="Token expiration time in seconds")


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    current_password: str
    new_password: str = Field(min_length=8, max_length=100)


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    email: EmailStr


class ConfirmResetPasswordRequest(BaseModel):
    """Confirm password reset request schema"""
    token: str
    new_password: str = Field(min_length=8, max_length=100)
