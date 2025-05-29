from pydantic import BaseModel
from datetime import datetime


class SubscriptionCreate(BaseModel):
    plan_id: int


class SubscriptionDetail(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    status: str

    model_config = {
        "from_attributes": True,
        "validate_by_name": True,
    }


class SubscriptionHistory(BaseModel):
    ok: bool = True
    message: str = "Subscription history retrieved successfully"
    data: list[SubscriptionDetail]


class SubscriptionResponse(BaseModel):
    ok: bool = True
    message: str = "Subscription retrieved successfully"
    data: SubscriptionDetail
