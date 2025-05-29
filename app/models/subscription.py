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
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    start_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(
        SqlEnum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False
    )

    user = relationship("User", back_populates="subscription")
    # plan = relationship("Plan", back_populates="subscriptions")

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.end_date

    @property
    def is_active(self) -> bool:
        return self.status == SubscriptionStatus.ACTIVE and not self.is_expired
