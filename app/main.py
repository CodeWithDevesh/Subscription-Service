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


@app.get("/", tags=["Root"])
async def root():
    return {
        "title": "Subscription Backend API",
        "description": "A robust API for managing subscription plans, authentication, and user subscriptions.",
        "documentation_url": "/docs",
        "health_check": "/health",
        "version": "1.0.0",
    }
