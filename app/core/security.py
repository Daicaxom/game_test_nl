"""
Security Utilities - JWT, Password Hashing, Authentication
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import get_settings
from app.core.exceptions import InvalidTokenException, TokenExpiredException

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password
        hashed_password: The hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain password.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject of the token (usually user ID)
        expires_delta: Optional custom expiration time
        additional_claims: Additional claims to include in the token
        
    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "access"
    }
    
    if additional_claims:
        to_encode.update(additional_claims)
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        subject: The subject of the token (usually user ID)
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT refresh token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: The JWT token to decode
        
    Returns:
        Dictionary containing the token payload
        
    Raises:
        TokenExpiredException: If the token has expired
        InvalidTokenException: If the token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except JWTError:
        raise InvalidTokenException()


def verify_access_token(token: str) -> Dict[str, Any]:
    """
    Verify an access token and return its payload.
    
    Args:
        token: The access token to verify
        
    Returns:
        Dictionary containing the token payload
        
    Raises:
        InvalidTokenException: If not an access token or invalid
        TokenExpiredException: If the token has expired
    """
    payload = decode_token(token)
    
    if payload.get("type") != "access":
        raise InvalidTokenException(details={"reason": "Not an access token"})
    
    return payload


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """
    Verify a refresh token and return its payload.
    
    Args:
        token: The refresh token to verify
        
    Returns:
        Dictionary containing the token payload
        
    Raises:
        InvalidTokenException: If not a refresh token or invalid
        TokenExpiredException: If the token has expired
    """
    payload = decode_token(token)
    
    if payload.get("type") != "refresh":
        raise InvalidTokenException(details={"reason": "Not a refresh token"})
    
    return payload


def get_subject_from_token(token: str) -> str:
    """
    Extract the subject (user ID) from a token.
    
    Args:
        token: The JWT token
        
    Returns:
        The subject string from the token
        
    Raises:
        InvalidTokenException: If token is invalid or has no subject
    """
    payload = decode_token(token)
    subject = payload.get("sub")
    
    if not subject:
        raise InvalidTokenException(details={"reason": "Token has no subject"})
    
    return subject
