from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URI

print("Creating async database engine...")
engine = create_async_engine(DATABASE_URI, echo=True)

print("Creating session local for async database operations...")
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

print("Creating declarative base for ORM models...")
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
