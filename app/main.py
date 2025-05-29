from app.config import DEBUG
from fastapi import FastAPI
from app.routers import plans, auth, subscription

app = FastAPI(debug=DEBUG)

app.include_router(plans.router)
app.include_router(auth.router)
app.include_router(subscription.router)


@app.get("/health", tags=["Health"])
async def read_root():
    return {
        "status": "ok",
        "message": "API is running",
        "version": "1.0.0",
    }
