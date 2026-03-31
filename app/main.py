"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.routers import code_practice, lessons, stats

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A minimal typing learning tool with progressive lessons and code practice",
    version="0.1.0",
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(lessons.router, prefix="/api", tags=["lessons"])
app.include_router(code_practice.router, prefix="/api", tags=["code-practice"])
app.include_router(stats.router, prefix="/api", tags=["stats"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main application page."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
