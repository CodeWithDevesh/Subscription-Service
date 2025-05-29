from dotenv import load_dotenv
import os
from app.utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Loading environment variables from .env file...")
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
DATABASE_URI = os.getenv("DATABASE_URI")
JWT_SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")