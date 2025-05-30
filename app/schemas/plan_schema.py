from pydantic import BaseModel
from typing import List



class PlanDetail(BaseModel):
    id: int
    name: str
    price: int
    duration_days: int
    features: List[str]


    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
    }

class PlanResponse(BaseModel):
    ok: bool = True
    message: str = "Plan retrieved successfully"
    data: PlanDetail


class PlanListResponse(BaseModel):
    ok: bool = True
    message: str = "Plans retrieved successfully"
    data: List[PlanDetail]



class PlanCreate(BaseModel):
    name: str
    price: int
    duration_days: int
    features: List[str]