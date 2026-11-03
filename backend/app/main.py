import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import logger
from app.api import auth, overview, analytics, savings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="OHMies — Smart Electricity Monitoring and Conservation Platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_ORIGIN,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging and timing middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        "METHOD=%s PATH=%s STATUS=%s DURATION=%.3fs",
        request.method,
        request.url.path,
        response.status_code,
        duration
    )
    return response

# Register routers under /api
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(overview.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(savings.router, prefix=settings.API_V1_STR)

@app.get("/api/health")
async def health_check():
    """Application health and readiness check."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "active_tab": "Tab 1 — Overview (Phase 1)"
    }

