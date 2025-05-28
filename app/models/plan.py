from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    price = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    features = Column(JSONB)
    # subscribers = relationship("Subscription", back_populates="plan")
