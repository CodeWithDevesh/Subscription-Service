from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.plan import Plan
from app.schemas.plan_schema import PlanSchema, PlanCreate
from app.database import get_db
from fastapi import HTTPException

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/", response_model=List[PlanSchema])
async def get_all_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan))
    plans = result.scalars().all()
    return plans


@router.post("/", response_model=PlanSchema)
async def create_plan(plan_data: PlanCreate, db: AsyncSession = Depends(get_db)):
    try:
        plan_dict = plan_data.model_dump()
    except AttributeError:
        plan_dict = plan_data.dict()
    existing_plan = await db.execute(select(Plan).where(Plan.name == plan_dict["name"]))
    if existing_plan.scalars().first():
        raise HTTPException(
            status_code=400, detail="Plan with this name already exists"
        )
    new_plan = Plan(**plan_dict)
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan


@router.post("/{plan_id}", response_model=PlanSchema)
async def update_plan(
    plan_id: int, plan_data: PlanCreate, db: AsyncSession = Depends(get_db)
):
    existing_plan = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = existing_plan.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    try:
        plan_dict = plan_data.model_dump()
    except AttributeError:
        plan_dict = plan_data.dict()

    for key, value in plan_dict.items():
        setattr(plan, key, value)

    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan
