from pydantic import BaseModel
from typing import List


class PlanSchema(BaseModel):
    id: int
    name: str
    price: int
    duration_days: int
    features: List[str]

    class Config:
        from_attributes = True


class PlanCreate(BaseModel):
    name: str
    price: int
    duration_days: int
    features: List[str]