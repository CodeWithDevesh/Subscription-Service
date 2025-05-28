from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from sqlalchemy import Enum as SqlEnum
import enum


class SubscriptionStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    end_date = Column(DateTime, nullable=True)
    status = Column(
        SqlEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False
    )

    user = relationship("User", back_populates="subscription")
    # plan = relationship("Plan", back_populates="subscriptions")
