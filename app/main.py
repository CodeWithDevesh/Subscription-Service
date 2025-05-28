from app.config import DEBUG
from fastapi import FastAPI
from app.database import Base

app = FastAPI(debug=DEBUG)

@app.get("/")
async def read_root():
    return{
        "message": "Welcome to the FastAPI application!",
    }
