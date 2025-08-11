"""
Dashboard Routes
API endpoints for the web dashboard
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Global references to main components (set by main app)
data_manager = None
personality_engine = None
response_generator = None
platform_manager = None
safety_monitor = None

def set_components(dm, pe, rg, pm, sm):
    """Set component references from main app"""
    global data_manager, personality_engine, response_generator, platform_manager, safety_monitor
    data_manager = dm
    personality_engine = pe
    response_generator = rg
    platform_manager = pm
    safety_monitor = sm

# Dashboard endpoints
@router.get("/status")
async def get_dashboard_status():
    """Get overall system status for dashboard"""
    return {
        "system": "AI Doppelgänger Engine",
        "status": "operational",
        "components": {
            "data_manager": data_manager is not None,
            "personality_engine": personality_engine is not None,
            "response_generator": response_generator is not None,
            "platform_manager": platform_manager is not None,
            "safety_monitor": safety_monitor is not None
        },
        "personality_trained": personality_engine.is_trained() if personality_engine else False,
        "auto_reply_enabled": response_generator.auto_reply_enabled if response_generator else False,
        "safety_mode": safety_monitor.get_mode() if safety_monitor else "unknown"
    }

@router.get("/personality")
async def get_personality_profile():
    """Get current personality profile"""
    if not personality_engine:
        raise HTTPException(status_code=503, detail="Personality engine not available")
    
    return {
        "profile": personality_engine.get_personality_profile(),
        "style_patterns": personality_engine.get_style_patterns(),
        "trained": personality_engine.is_trained()
    }

@router.post("/train")
async def train_personality(config: Dict[str, Any]):
    """Train the personality model"""
    if not data_manager:
        raise HTTPException(status_code=503, detail="Data manager not available")
    
    try:
        results = await data_manager.ingest_all_sources(config)
        return {"success": True, "results": results}
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@router.get("/stats")
async def get_system_stats():
    """Get comprehensive system statistics"""
    stats = {
        "personality": {},
        "responses": {},
        "safety": {},
        "platforms": {}
    }
    
    # Personality stats
    if personality_engine:
        stats["personality"] = {
            "trained": personality_engine.is_trained(),
            "profile": personality_engine.get_personality_profile()
        }
    
    # Response stats
    if response_generator:
        stats["responses"] = response_generator.get_response_stats()
    
    # Safety stats
    if safety_monitor:
        stats["safety"] = safety_monitor.get_safety_stats()
    
    # Platform stats
    if platform_manager:
        stats["platforms"] = {
            "connected": platform_manager.get_connected_platforms()
        }
    
    return stats

@router.post("/test-response")
async def test_response(request: Dict[str, Any]):
    """Generate a test response without sending it"""
    if not response_generator:
        raise HTTPException(status_code=503, detail="Response generator not available")
    
    try:
        test_input = request.get("input", "")
        context = request.get("context", "")
        mood = request.get("mood", None)
        
        response = await response_generator.generate_test_response(
            test_input=test_input,
            context=context,
            mood=mood
        )
        
        return {
            "input": test_input,
            "response": response,
            "mood": mood or response_generator.current_mood
        }
    except Exception as e:
        logger.error(f"Test response failed: {e}")
        raise HTTPException(status_code=500, detail=f"Test response failed: {str(e)}")

@router.post("/settings/auto-reply")
async def set_auto_reply(enabled: bool):
    """Enable or disable auto-reply"""
    if not response_generator:
        raise HTTPException(status_code=503, detail="Response generator not available")
    
    response_generator.enable_auto_reply(enabled)
    return {"success": True, "auto_reply_enabled": enabled}

@router.post("/settings/override")
async def set_override_required(required: bool):
    """Set whether manual override is required"""
    if not response_generator:
        raise HTTPException(status_code=503, detail="Response generator not available")
    
    response_generator.require_override(required)
    return {"success": True, "override_required": required}

@router.post("/settings/mood")
async def set_mood(mood: str):
    """Set the current response mood"""
    if not response_generator:
        raise HTTPException(status_code=503, detail="Response generator not available")
    
    response_generator.set_mood(mood)
    return {"success": True, "mood": mood}

@router.post("/settings/safety-mode")
async def set_safety_mode(mode: str):
    """Set the safety mode"""
    if not safety_monitor:
        raise HTTPException(status_code=503, detail="Safety monitor not available")
    
    safety_monitor.set_safety_mode(mode)
    return {"success": True, "safety_mode": mode}

@router.get("/history/responses")
async def get_response_history(limit: int = 10):
    """Get recent response history"""
    if not response_generator:
        raise HTTPException(status_code=503, detail="Response generator not available")
    
    return response_generator.get_recent_responses(limit)

@router.get("/history/safety")
async def get_safety_history(limit: int = 10):
    """Get recent safety events"""
    if not safety_monitor:
        raise HTTPException(status_code=503, detail="Safety monitor not available")
    
    return safety_monitor.get_recent_safety_events(limit)

@router.post("/safety/redlines")
async def add_redline(term: str):
    """Add a redline term"""
    if not safety_monitor:
        raise HTTPException(status_code=503, detail="Safety monitor not available")
    
    safety_monitor.add_redline(term)
    return {"success": True, "redline_added": term}

@router.delete("/safety/redlines")
async def remove_redline(term: str):
    """Remove a redline term"""
    if not safety_monitor:
        raise HTTPException(status_code=503, detail="Safety monitor not available")
    
    safety_monitor.remove_redline(term)
    return {"success": True, "redline_removed": term}

@router.post("/safety/sensitive-topics")
async def add_sensitive_topic(topic: str):
    """Add a sensitive topic"""
    if not safety_monitor:
        raise HTTPException(status_code=503, detail="Safety monitor not available")
    
    safety_monitor.add_sensitive_topic(topic)
    return {"success": True, "sensitive_topic_added": topic}

@router.post("/clear/history")
async def clear_history(history_type: str):
    """Clear specific history"""
    if history_type == "responses":
        if response_generator:
            response_generator.clear_history()
            return {"success": True, "message": "Response history cleared"}
    elif history_type == "safety":
        if safety_monitor:
            safety_monitor.clear_safety_history()
            return {"success": True, "message": "Safety history cleared"}
    else:
        raise HTTPException(status_code=400, detail="Invalid history type")
    
    raise HTTPException(status_code=503, detail="Component not available")

@router.get("/live-feed")
async def get_live_feed():
    """Get live activity feed (for WebSocket implementation)"""
    # This would be implemented with WebSockets for real-time updates
    return {
        "message": "Live feed endpoint - implement with WebSockets",
        "timestamp": "2024-01-01T00:00:00Z"
    } 