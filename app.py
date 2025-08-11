#!/usr/bin/env python3
"""
AI Doppelgänger Engine - Main Application
Your digital twin that lives on the internet while you nap in a hoodie
"""

import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from dotenv import load_dotenv

# Import our modules
from data_ingestion.ingestion_manager import DataIngestionManager
from personality_core.personality_engine import PersonalityEngine
from response_engine.response_generator import ResponseGenerator
from api.platform_integrations import PlatformManager
from safety.safety_monitor import SafetyMonitor
from dashboard.dashboard_routes import router as dashboard_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mirrorme.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Doppelgänger Engine",
    description="Your digital twin that lives on the internet",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
data_manager = None
personality_engine = None
response_generator = None
platform_manager = None
safety_monitor = None

@app.on_event("startup")
async def startup_event():
    """Initialize all core components on startup"""
    global data_manager, personality_engine, response_generator, platform_manager, safety_monitor
    
    logger.info("🚀 Starting AI Doppelgänger Engine...")
    
    try:
        # Initialize core components
        data_manager = DataIngestionManager()
        personality_engine = PersonalityEngine()
        response_generator = ResponseGenerator()
        platform_manager = PlatformManager()
        safety_monitor = SafetyMonitor()
        
        logger.info("✅ All components initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard"""
    dashboard_path = Path("dashboard/dist/index.html")
    if dashboard_path.exists():
        return dashboard_path.read_text()
    else:
        return """
        <html>
            <head><title>AI Doppelgänger Engine</title></head>
            <body>
                <h1>🧠 AI Doppelgänger Engine</h1>
                <p>Your digital twin is starting up...</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "data_manager": data_manager is not None,
            "personality_engine": personality_engine is not None,
            "response_generator": response_generator is not None,
            "platform_manager": platform_manager is not None,
            "safety_monitor": safety_monitor is not None
        }
    }

@app.get("/api/status")
async def get_status():
    """Get detailed system status"""
    return {
        "system": "AI Doppelgänger Engine",
        "version": "1.0.0",
        "status": "operational",
        "personality_trained": personality_engine.is_trained() if personality_engine else False,
        "platforms_connected": platform_manager.get_connected_platforms() if platform_manager else [],
        "safety_mode": safety_monitor.get_mode() if safety_monitor else "unknown"
    }

# Include dashboard routes
app.include_router(dashboard_router, prefix="/api/dashboard")

# Mount static files for dashboard
if Path("dashboard/dist").exists():
    app.mount("/static", StaticFiles(directory="dashboard/dist"), name="static")

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 