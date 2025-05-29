from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    plan_id: int

class SubscriptionDetail(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: str
    end_date: str
    status: str

    class Config:
        from_attributes = True

class SubscriptionHistory(BaseModel):
    ok: bool = True
    message: str = "Subscription history retrieved successfully"
    data: list[SubscriptionDetail]

class SubscriptionResponse(BaseModel):
    ok: bool = True
    message: str = "Subscription retrieved successfully"
    data: SubscriptionDetail