from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.plan import Plan
from app.schemas.plan_schema import PlanResponse, PlanCreate, PlanListResponse
from app.database import get_db
from fastapi import HTTPException
from app.auth.dependencies import get_current_admin
from app.models.user import User
from app.utils.retry import retry_on_db_error

@retry_on_db_error
async def get_all_plans(db: AsyncSession) -> List[Plan]:
    result = await db.execute(select(Plan))
    plans = result.scalars().all()
    if not plans:
        return PlanListResponse(ok=False, message="no plans found", data=[])
    return PlanListResponse(data=plans)

@retry_on_db_error
async def get_plan_by_id(plan_id: int, db: AsyncSession) -> PlanResponse:
    existing_plan = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = existing_plan.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return PlanResponse(ok=True, message="Plan retrieved successfully", data=plan)

@retry_on_db_error
async def create_plan(plan_data: PlanCreate, db: AsyncSession) -> PlanResponse:
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
    return PlanResponse(ok=True, message="Plan created successfully", data=new_plan)


async def update_plan(
    plan_id: int, plan_data: PlanCreate, db: AsyncSession
) -> PlanResponse:
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
    return PlanResponse(ok=True, message="Plan updated successfully", data=plan)

@retry_on_db_error
async def delete_plan(plan_id: int, db: AsyncSession) -> PlanResponse:
    existing_plan = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = existing_plan.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    await db.delete(plan)
    await db.commit()
    return PlanResponse(ok=True, message="Plan deleted successfully", data=plan)
