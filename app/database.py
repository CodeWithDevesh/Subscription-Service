from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import DATABASE_URI
from sqlalchemy import create_engine
from app.utils.logger import get_logger
logger = get_logger(__name__)

logger.info("Creating async database engine...")
engine = create_async_engine(DATABASE_URI, echo=True)

logger.info("Creating sync database engine for legacy operations...")
sync_engine = create_engine(
    DATABASE_URI.replace("postgresql+asyncpg", "postgresql"), echo=True
)

logger.info("Creating session local for async database operations...")
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

logger.info("Creating session local for sync database operations...")
SyncSessionLocal = sessionmaker(
    bind=sync_engine, class_=Session, expire_on_commit=False
)

logger.info("Creating declarative base for ORM models...")
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    with SyncSessionLocal() as session:
        yield session
