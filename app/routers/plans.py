from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.models.plan import Plan
from app.schemas.plan_schema import (
    PlanResponse,
    PlanCreate,
    PlanListResponse,
)
from app.database import get_db
from fastapi import HTTPException
from app.auth.dependencies import get_current_admin
from app.models.user import User
from app.services.plan_service import (
    delete_plan as delete_plan_service,
    get_all_plans as get_all_plans_service,
    get_plan_by_id as get_plan_by_id_service,
    create_plan as create_plan_service,
    update_plan as update_plan_service,
)

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/", response_model=PlanListResponse)
async def get_all_plans(db: AsyncSession = Depends(get_db)) -> PlanListResponse:
    """Retrieve all plans."""
    return await get_all_plans_service(db)


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan_by_id(
    plan_id: int, db: AsyncSession = Depends(get_db)
) -> PlanResponse:
    """Retrieve a plan by ID."""
    return await get_plan_by_id_service(plan_id, db)


@router.post("/", response_model=PlanResponse)
async def create_plan(
    plan_data: PlanCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin),
) -> PlanResponse:
    """Create a new plan."""
    return await create_plan_service(plan_data, db)


@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    plan_data: PlanCreate,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin),
) -> PlanResponse:
    """Update a plan by ID."""
    return await update_plan_service(plan_id, plan_data, db)


@router.delete("/{plan_id}", response_model=PlanResponse)
async def delete_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin),
) -> PlanResponse:
    """Delete a plan by ID."""
    return await delete_plan_service(plan_id, db)
