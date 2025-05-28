from dotenv import load_dotenv
import os


print("Loading environment variables from .env file...")
load_dotenv()

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
DATABASE_URI = os.getenv("DATABASE_URI")