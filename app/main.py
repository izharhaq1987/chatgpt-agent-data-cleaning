from fastapi import FastAPI
from app.routers import validate, health

app = FastAPI(title="ChatGPT Agent Data Cleaning", version="0.1.0")
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(validate.router, tags=["validate"])
@app.get("/")
def index():
    """
    Root endpoint — provides a basic status message
    """
    return {
        "message": "ChatGPT Agent Data Cleaning API running.",
        "version": "0.1.0",
        "endpoints": ["/", "/health", "/validate"]
    }
