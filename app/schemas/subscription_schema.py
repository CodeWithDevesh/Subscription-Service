from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    plan_id: int
