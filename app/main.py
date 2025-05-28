from app.config import DEBUG
from fastapi import FastAPI
from app.routers import plans, auth

app = FastAPI(debug=DEBUG)

app.include_router(plans.router)
app.include_router(auth.router)


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the FastAPI application!",
    }
