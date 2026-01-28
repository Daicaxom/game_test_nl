"""
Authentication API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

router = APIRouter()


# Request/Response schemas
class RegisterRequest(BaseModel):
    """Registration request schema"""
    username: str
    email: EmailStr
    password: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    username: str
    email: str
    display_name: str | None
    level: int
    gold: int
    gems: int


# Endpoints
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new player account.
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (min 8 characters)
    - **display_name**: Optional display name
    """
    # TODO: Implement with service layer
    return {
        "id": "placeholder-uuid",
        "username": request.username,
        "email": request.email,
        "display_name": request.display_name or request.username,
        "level": 1,
        "gold": 0,
        "gems": 0
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login to get access token.
    
    - **username**: Your username
    - **password**: Your password
    """
    # TODO: Implement with service layer
    return {
        "access_token": "placeholder-token",
        "token_type": "bearer",
        "refresh_token": "placeholder-refresh-token"
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token():
    """Refresh access token using refresh token"""
    # TODO: Implement with service layer
    return {
        "access_token": "new-placeholder-token",
        "token_type": "bearer",
        "refresh_token": "new-placeholder-refresh-token"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current logged-in user information"""
    # TODO: Implement with service layer and authentication
    return {
        "id": "placeholder-uuid",
        "username": "test_user",
        "email": "test@example.com",
        "display_name": "Test User",
        "level": 1,
        "gold": 1000,
        "gems": 100
    }
