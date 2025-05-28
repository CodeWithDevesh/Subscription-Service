from pydantic import BaseModel
from typing import List


class Plan_Schema(BaseModel):
    id: int
    name: str
    price: int
    duration_days: int
    features: List[str]

    class Config:
        from_attributes = True
