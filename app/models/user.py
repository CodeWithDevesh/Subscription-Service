from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    subscription = relationship("Subscription", back_populates="user")
    is_admin = Column(Boolean, default=False)

# from app.models.subscription import Subscription  # prevents circular import
