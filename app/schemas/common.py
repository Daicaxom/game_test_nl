"""
Common Pydantic Schemas - Shared response models
"""
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class MetaInfo(BaseModel):
    """Metadata for API responses"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class ErrorDetail(BaseModel):
    """Error detail schema"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response wrapper"""
    success: bool = True
    data: T
    meta: MetaInfo = Field(default_factory=MetaInfo)


class ErrorResponse(BaseModel):
    """Generic error response wrapper"""
    success: bool = False
    error: ErrorDetail
    meta: MetaInfo = Field(default_factory=MetaInfo)


class PaginationInfo(BaseModel):
    """Pagination metadata"""
    page: int = Field(ge=1)
    per_page: int = Field(ge=1, le=100)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""
    success: bool = True
    data: List[T]
    pagination: PaginationInfo
    meta: MetaInfo = Field(default_factory=MetaInfo)


class ResourceIdResponse(BaseModel):
    """Response containing just a resource ID"""
    id: str


class MessageResponse(BaseModel):
    """Response containing a message"""
    message: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: Optional[str] = None


class StatsBase(BaseModel):
    """Base stats schema"""
    hp: int = Field(ge=0)
    atk: int = Field(ge=0)
    def_: int = Field(ge=0, alias="def")
    spd: int = Field(ge=0)
    crit: int = Field(ge=0)
    dex: int = Field(ge=0)
    
    class Config:
        populate_by_name = True


class PositionSchema(BaseModel):
    """Grid position schema"""
    x: int = Field(ge=0, le=2)
    y: int = Field(ge=0, le=2)


class ItemQuantity(BaseModel):
    """Item with quantity schema"""
    item_id: str
    quantity: int = Field(ge=1)


class RewardSchema(BaseModel):
    """Reward schema for various rewards"""
    exp: int = Field(default=0, ge=0)
    gold: int = Field(default=0, ge=0)
    gems: int = Field(default=0, ge=0)
    items: List[ItemQuantity] = Field(default_factory=list)


class ResourceAmount(BaseModel):
    """Resource amount schema"""
    gold: int = Field(default=0, ge=0)
    gems: int = Field(default=0, ge=0)
    stamina: int = Field(default=0, ge=0)
