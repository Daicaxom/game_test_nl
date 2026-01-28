"""
Authentication Service - Handles user authentication
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import uuid4

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from app.core.exceptions import (
    InvalidCredentialsException,
    DuplicateResourceException,
    TokenExpiredException,
    InvalidTokenException
)
from app.config.settings import get_settings

settings = get_settings()


class AuthService:
    """
    Service for authentication operations.
    
    Handles:
    - User registration
    - User login
    - Token management
    - Password operations
    """
    
    def __init__(self, player_repository=None):
        """
        Initialize the auth service.
        
        Args:
            player_repository: Optional PlayerRepository for database operations
        """
        self.player_repository = player_repository
    
    async def register(
        self,
        username: str,
        email: str,
        password: str,
        display_name: Optional[str] = None
    ) -> dict:
        """
        Register a new player.
        
        Args:
            username: Unique username
            email: Email address
            password: Plain text password
            display_name: Optional display name
            
        Returns:
            Dictionary with new player data
            
        Raises:
            DuplicateResourceException: If username or email exists
        """
        # Check for existing username
        if self.player_repository:
            if await self.player_repository.username_exists(username):
                raise DuplicateResourceException("Player", "username", username)
            
            if await self.player_repository.email_exists(email):
                raise DuplicateResourceException("Player", "email", email)
        
        # Hash password
        password_hash = get_password_hash(password)
        
        # Create player data
        player_data = {
            "id": str(uuid4()),
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "display_name": display_name or username,
            "level": 1,
            "exp": 0,
            "gold": 1000,  # Starting gold
            "gems": 50,    # Starting gems
            "stamina": 100,
            "max_stamina": 100,
            "vip_level": 0,
            "is_active": True,
            "created_at": datetime.utcnow(),
        }
        
        # Save to database if repository is available
        if self.player_repository:
            player = await self.player_repository.create(player_data)
            return {
                "id": str(player.id),
                "username": player.username,
                "email": player.email,
                "display_name": player.display_name,
                "level": player.level,
                "gold": player.gold,
                "gems": player.gems
            }
        
        # Return mock data if no repository
        return {
            "id": player_data["id"],
            "username": player_data["username"],
            "email": player_data["email"],
            "display_name": player_data["display_name"],
            "level": player_data["level"],
            "gold": player_data["gold"],
            "gems": player_data["gems"]
        }
    
    async def login(
        self,
        username: str,
        password: str
    ) -> dict:
        """
        Authenticate a player and return tokens.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            Dictionary with access and refresh tokens
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
        """
        player = None
        
        if self.player_repository:
            player = await self.player_repository.get_by_username(username)
            
            if not player:
                raise InvalidCredentialsException()
            
            if not verify_password(password, player.password_hash):
                raise InvalidCredentialsException()
            
            # Update last login
            await self.player_repository.update_last_login(player.id)
            
            player_id = str(player.id)
        else:
            # DEV ONLY: Mock authentication when repository is not available.
            # This is for development/testing purposes when no database is connected.
            # In production, player_repository should always be provided.
            if username != "test_user" or password != "password":
                raise InvalidCredentialsException()
            player_id = "mock-player-uuid"
        
        # Generate tokens
        access_token = create_access_token(subject=player_id)
        refresh_token = create_refresh_token(subject=player_id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    async def refresh_tokens(
        self,
        refresh_token: str
    ) -> dict:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            Dictionary with new tokens
            
        Raises:
            InvalidTokenException: If refresh token is invalid
            TokenExpiredException: If refresh token is expired
        """
        payload = verify_refresh_token(refresh_token)
        player_id = payload.get("sub")
        
        if not player_id:
            raise InvalidTokenException()
        
        # Verify player still exists
        if self.player_repository:
            player = await self.player_repository.get(player_id)
            if not player or not player.is_active:
                raise InvalidTokenException()
        
        # Generate new tokens
        new_access_token = create_access_token(subject=player_id)
        new_refresh_token = create_refresh_token(subject=player_id)
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "refresh_token": new_refresh_token,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    async def change_password(
        self,
        player_id: str,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change a player's password.
        
        Args:
            player_id: The player ID
            current_password: Current password
            new_password: New password
            
        Returns:
            True if password changed successfully
            
        Raises:
            InvalidCredentialsException: If current password is wrong
        """
        if not self.player_repository:
            return True
        
        player = await self.player_repository.get(player_id)
        
        if not player:
            raise InvalidCredentialsException()
        
        if not verify_password(current_password, player.password_hash):
            raise InvalidCredentialsException()
        
        new_hash = get_password_hash(new_password)
        await self.player_repository.update(player_id, {"password_hash": new_hash})
        
        return True
    
    async def get_current_user(self, player_id: str) -> dict:
        """
        Get current user information.
        
        Args:
            player_id: The player ID from token
            
        Returns:
            Dictionary with user information
        """
        if self.player_repository:
            player = await self.player_repository.get(player_id)
            if player:
                return {
                    "id": str(player.id),
                    "username": player.username,
                    "email": player.email,
                    "display_name": player.display_name,
                    "level": player.level,
                    "gold": player.gold,
                    "gems": player.gems
                }
        
        # Return mock data
        return {
            "id": player_id,
            "username": "test_user",
            "email": "test@example.com",
            "display_name": "Test User",
            "level": 1,
            "gold": 1000,
            "gems": 100
        }
