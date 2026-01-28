"""
Teams API Endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()


# Request/Response schemas
class PositionSchema(BaseModel):
    """Grid position"""
    x: int = Field(ge=0, le=2)
    y: int = Field(ge=0, le=2)


class TeamMemberResponse(BaseModel):
    """Team member response"""
    hero_id: str
    hero_name: str
    position: PositionSchema
    power: int


class TeamResponse(BaseModel):
    """Team response"""
    id: str
    name: str
    slot_number: int
    members: List[TeamMemberResponse]
    formation_id: Optional[str] = None
    is_default: bool
    total_power: int


class CreateTeamRequest(BaseModel):
    """Create team request"""
    name: str = Field(min_length=1, max_length=50)


class UpdateTeamRequest(BaseModel):
    """Update team request"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    members: Optional[List[dict]] = None


class AddMemberRequest(BaseModel):
    """Add member request"""
    hero_id: str
    position: PositionSchema


class UpdateFormationRequest(BaseModel):
    """Update formation request"""
    formation_id: Optional[str] = None


class FormationBonusResponse(BaseModel):
    """Formation bonus"""
    stat: str
    value: float
    bonus_type: str


class FormationResponse(BaseModel):
    """Formation response"""
    id: str
    name: str
    description: str
    required_members: int
    bonuses: List[FormationBonusResponse]


# Endpoints
@router.get("", response_model=List[TeamResponse])
async def get_teams():
    """
    Get all teams for current player.
    """
    # TODO: Implement with service layer
    return [
        {
            "id": "default-team-uuid",
            "name": "Default Team",
            "slot_number": 1,
            "members": [
                {
                    "hero_id": "hero-1-uuid",
                    "hero_name": "Quan Vũ",
                    "position": {"x": 1, "y": 1},
                    "power": 1500
                }
            ],
            "formation_id": None,
            "is_default": True,
            "total_power": 1500
        }
    ]


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(request: CreateTeamRequest):
    """
    Create a new team.
    
    - **name**: Team name
    """
    # TODO: Implement with service layer
    return {
        "id": "new-team-uuid",
        "name": request.name,
        "slot_number": 2,
        "members": [],
        "formation_id": None,
        "is_default": False,
        "total_power": 0
    }


@router.get("/formations", response_model=List[FormationResponse])
async def get_formations():
    """
    Get all available formations.
    """
    # TODO: Implement with service layer
    return [
        {
            "id": "ngu_hanh_tran",
            "name": "Ngũ Hành Trận",
            "description": "Requires 5 heroes with all different elements",
            "required_members": 5,
            "bonuses": [
                {"stat": "all", "value": 5, "bonus_type": "percent"},
                {"stat": "element_power", "value": 20, "bonus_type": "percent"}
            ]
        },
        {
            "id": "long_dang_ho_khieu",
            "name": "Long Đằng Hổ Khiếu",
            "description": "Offensive formation for 3 heroes",
            "required_members": 3,
            "bonuses": [
                {"stat": "atk", "value": 15, "bonus_type": "percent"},
                {"stat": "spd", "value": 10, "bonus_type": "percent"}
            ]
        }
    ]


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: str):
    """
    Get specific team details.
    
    - **team_id**: Team ID
    """
    # TODO: Implement with service layer
    return {
        "id": team_id,
        "name": "Default Team",
        "slot_number": 1,
        "members": [
            {
                "hero_id": "hero-1-uuid",
                "hero_name": "Quan Vũ",
                "position": {"x": 1, "y": 1},
                "power": 1500
            }
        ],
        "formation_id": None,
        "is_default": True,
        "total_power": 1500
    }


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: str, request: UpdateTeamRequest):
    """
    Update a team.
    
    - **team_id**: Team ID
    - **name**: New team name
    - **members**: New members list
    """
    # TODO: Implement with service layer
    return {
        "id": team_id,
        "name": request.name or "Default Team",
        "slot_number": 1,
        "members": request.members or [],
        "formation_id": None,
        "is_default": True,
        "total_power": 0
    }


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: str):
    """
    Delete a team.
    
    - **team_id**: Team ID
    """
    # TODO: Implement with service layer
    return None


@router.post("/{team_id}/members", response_model=TeamResponse)
async def add_team_member(team_id: str, request: AddMemberRequest):
    """
    Add a hero to a team.
    
    - **team_id**: Team ID
    - **hero_id**: Hero ID to add
    - **position**: Grid position
    """
    # TODO: Implement with service layer
    return {
        "id": team_id,
        "name": "Default Team",
        "slot_number": 1,
        "members": [
            {
                "hero_id": request.hero_id,
                "hero_name": "New Hero",
                "position": request.position.model_dump(),
                "power": 1000
            }
        ],
        "formation_id": None,
        "is_default": True,
        "total_power": 1000
    }


@router.delete("/{team_id}/members/{hero_id}", response_model=TeamResponse)
async def remove_team_member(team_id: str, hero_id: str):
    """
    Remove a hero from a team.
    
    - **team_id**: Team ID
    - **hero_id**: Hero ID to remove
    """
    # TODO: Implement with service layer
    return {
        "id": team_id,
        "name": "Default Team",
        "slot_number": 1,
        "members": [],
        "formation_id": None,
        "is_default": True,
        "total_power": 0
    }


@router.put("/{team_id}/formation", response_model=TeamResponse)
async def update_team_formation(team_id: str, request: UpdateFormationRequest):
    """
    Update team's formation.
    
    - **team_id**: Team ID
    - **formation_id**: Formation ID or null to clear
    """
    # TODO: Implement with service layer
    return {
        "id": team_id,
        "name": "Default Team",
        "slot_number": 1,
        "members": [],
        "formation_id": request.formation_id,
        "is_default": True,
        "total_power": 0
    }
