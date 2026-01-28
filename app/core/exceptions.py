"""
Custom Exceptions for the application
"""
from typing import Any, Dict, Optional


class BaseAppException(Exception):
    """Base exception for application errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API response"""
        return {
            "code": self.error_code,
            "message": self.message,
            "details": self.details
        }


# Authentication Exceptions
class AuthenticationException(BaseAppException):
    """Exception for authentication failures"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTH_FAILED",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            details=details
        )


class InvalidCredentialsException(AuthenticationException):
    """Exception for invalid login credentials"""
    
    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message="Invalid username or password",
            error_code="INVALID_CREDENTIALS",
            details=details
        )


class TokenExpiredException(AuthenticationException):
    """Exception for expired tokens"""
    
    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message="Token has expired",
            error_code="TOKEN_EXPIRED",
            details=details
        )


class InvalidTokenException(AuthenticationException):
    """Exception for invalid tokens"""
    
    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message="Invalid token",
            error_code="INVALID_TOKEN",
            details=details
        )


# Authorization Exceptions
class AuthorizationException(BaseAppException):
    """Exception for authorization failures"""
    
    def __init__(
        self,
        message: str = "Access denied",
        error_code: str = "ACCESS_DENIED",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=403,
            details=details
        )


class InsufficientPermissionsException(AuthorizationException):
    """Exception for insufficient permissions"""
    
    def __init__(
        self,
        required_permission: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Missing required permission: {required_permission}",
            error_code="INSUFFICIENT_PERMISSIONS",
            details=details or {"required_permission": required_permission}
        )


# Resource Exceptions
class ResourceNotFoundException(BaseAppException):
    """Exception for resource not found"""
    
    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"{resource_type} with id {resource_id} not found",
            error_code=f"{resource_type.upper()}_NOT_FOUND",
            status_code=404,
            details=details or {"resource_type": resource_type, "resource_id": resource_id}
        )


class PlayerNotFoundException(ResourceNotFoundException):
    """Exception for player not found"""
    
    def __init__(self, player_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            resource_type="Player",
            resource_id=player_id,
            details=details
        )


class HeroNotFoundException(ResourceNotFoundException):
    """Exception for hero not found"""
    
    def __init__(self, hero_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            resource_type="Hero",
            resource_id=hero_id,
            details=details
        )


class EquipmentNotFoundException(ResourceNotFoundException):
    """Exception for equipment not found"""
    
    def __init__(self, equipment_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            resource_type="Equipment",
            resource_id=equipment_id,
            details=details
        )


class TeamNotFoundException(ResourceNotFoundException):
    """Exception for team not found"""
    
    def __init__(self, team_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            resource_type="Team",
            resource_id=team_id,
            details=details
        )


class BattleNotFoundException(ResourceNotFoundException):
    """Exception for battle not found"""
    
    def __init__(self, battle_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            resource_type="Battle",
            resource_id=battle_id,
            details=details
        )


class StageNotFoundException(ResourceNotFoundException):
    """Exception for stage not found"""
    
    def __init__(self, stage_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            resource_type="Stage",
            resource_id=stage_id,
            details=details
        )


# Validation Exceptions
class ValidationException(BaseAppException):
    """Exception for validation errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class DuplicateResourceException(ValidationException):
    """Exception for duplicate resources"""
    
    def __init__(
        self,
        resource_type: str,
        field: str,
        value: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"{resource_type} with {field} '{value}' already exists",
            error_code=f"DUPLICATE_{resource_type.upper()}",
            details=details or {"field": field, "value": value}
        )


# Game-specific Exceptions
class InsufficientResourcesException(BaseAppException):
    """Exception for insufficient resources (gold, gems, stamina, etc.)"""
    
    def __init__(
        self,
        resource_type: str,
        required: int,
        available: int,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Insufficient {resource_type}: required {required}, available {available}",
            error_code="INSUFFICIENT_RESOURCES",
            status_code=400,
            details=details or {
                "resource_type": resource_type,
                "required": required,
                "available": available
            }
        )


class InsufficientGoldException(InsufficientResourcesException):
    """Exception for insufficient gold"""
    
    def __init__(self, required: int, available: int):
        super().__init__(
            resource_type="gold",
            required=required,
            available=available
        )


class InsufficientGemsException(InsufficientResourcesException):
    """Exception for insufficient gems"""
    
    def __init__(self, required: int, available: int):
        super().__init__(
            resource_type="gems",
            required=required,
            available=available
        )


class InsufficientStaminaException(InsufficientResourcesException):
    """Exception for insufficient stamina"""
    
    def __init__(self, required: int, available: int):
        super().__init__(
            resource_type="stamina",
            required=required,
            available=available
        )


class BattleException(BaseAppException):
    """Exception for battle-related errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "BATTLE_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class NotPlayerTurnException(BattleException):
    """Exception when player tries to act on enemy turn"""
    
    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message="It is not the player's turn",
            error_code="NOT_PLAYER_TURN",
            details=details
        )


class InvalidActionException(BattleException):
    """Exception for invalid battle actions"""
    
    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Invalid action: {reason}",
            error_code="INVALID_ACTION",
            details=details or {"reason": reason}
        )


class GachaException(BaseAppException):
    """Exception for gacha-related errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "GACHA_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class HeroException(BaseAppException):
    """Exception for hero-related errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "HERO_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class HeroAlreadyMaxLevelException(HeroException):
    """Exception when hero is already at max level"""
    
    def __init__(self, hero_id: str, current_level: int, max_level: int):
        super().__init__(
            message=f"Hero is already at max level ({max_level})",
            error_code="HERO_MAX_LEVEL",
            details={
                "hero_id": hero_id,
                "current_level": current_level,
                "max_level": max_level
            }
        )


class EquipmentException(BaseAppException):
    """Exception for equipment-related errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "EQUIPMENT_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class TeamException(BaseAppException):
    """Exception for team-related errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "TEAM_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details
        )


class TeamFullException(TeamException):
    """Exception when team is at max capacity"""
    
    def __init__(self, team_id: str, max_members: int = 5):
        super().__init__(
            message=f"Team is at maximum capacity ({max_members} members)",
            error_code="TEAM_FULL",
            details={"team_id": team_id, "max_members": max_members}
        )
