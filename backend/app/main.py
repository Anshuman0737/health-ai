from fastapi import FastAPI
from app.routes import report_routes

app = FastAPI(
    title="AI Preventive Health Platform",
    version="0.2.0",
    description="Advanced Preventive Multi-System Risk Intelligence API"
)

app.include_router(report_routes.router)
