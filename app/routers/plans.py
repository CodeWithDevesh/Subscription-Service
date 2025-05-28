from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.plan import Plan
from app.schemas.plan_schema import Plan_Schema
from app.database import get_db

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/", response_model=List[Plan_Schema])
async def get_all_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan))
    plans = result.scalars().all()
    return plans
