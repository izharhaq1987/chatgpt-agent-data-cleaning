from fastapi import FastAPI
from app.routers import validate, health

app = FastAPI(title="ChatGPT Agent Data Cleaning", version="0.1.0")
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(validate.router, tags=["validate"])
