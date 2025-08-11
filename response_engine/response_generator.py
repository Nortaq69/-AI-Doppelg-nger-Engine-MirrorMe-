"""
Response Generator
Coordinates message generation and routing for the AI doppelgänger
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

from .intent_classifier import IntentClassifier
from .tone_matcher import ToneMatcher

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Main response generation and routing engine"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.tone_matcher = ToneMatcher()
        self.personality_engine = None
        self.safety_monitor = None
        
        # Response settings
        self.auto_reply_enabled = False
        self.override_required = False
        self.current_mood = "default"
        
        # Response history
        self.response_history = []
        
        logger.info("💬 Response Generator initialized")
    
    def set_personality_engine(self, personality_engine):
        """Set the personality engine reference"""
        self.personality_engine = personality_engine
    
    def set_safety_monitor(self, safety_monitor):
        """Set the safety monitor reference"""
        self.safety_monitor = safety_monitor
    
    async def process_incoming_message(self, 
                                     message: Dict[str, Any], 
                                     platform: str) -> Dict[str, Any]:
        """Process an incoming message and generate appropriate response"""
        
        try:
            # Classify intent
            intent = await self.intent_classifier.classify_intent(message)
            
            # Check if auto-reply is enabled
            if not self.auto_reply_enabled:
                return {
                    "action": "manual_review",
                    "reason": "Auto-reply disabled",
                    "intent": intent,
                    "message": message
                }
            
            # Generate response
            response = await self._generate_response(message, intent, platform)
            
            # Safety check
            if self.safety_monitor:
                safety_check = await self.safety_monitor.check_response(response, message)
                if not safety_check["safe"]:
                    return {
                        "action": "manual_review",
                        "reason": f"Safety concern: {safety_check['reason']}",
                        "intent": intent,
                        "response": response,
                        "message": message
                    }
            
            # Check if override is required
            if self.override_required:
                return {
                    "action": "manual_approval",
                    "intent": intent,
                    "response": response,
                    "message": message
                }
            
            # Send response
            await self._send_response(response, platform, message)
            
            # Log response
            self._log_response(message, response, intent, platform)
            
            return {
                "action": "sent",
                "intent": intent,
                "response": response,
                "message": message
            }
            
        except Exception as e:
            logger.error(f"Message processing failed: {e}")
            return {
                "action": "error",
                "error": str(e),
                "message": message
            }
    
    async def _generate_response(self, 
                               message: Dict[str, Any], 
                               intent: Dict[str, Any], 
                               platform: str) -> str:
        """Generate a response based on message and intent"""
        
        if not self.personality_engine:
            return "I'm still learning how to respond like you!"
        
        # Extract message content
        content = message.get("content", "")
        sender = message.get("sender", "")
        context = message.get("context", "")
        
        # Determine appropriate tone based on intent and context
        tone = await self.tone_matcher.determine_tone(intent, context, sender)
        
        # Generate response using personality engine
        response = await self.personality_engine.generate_response(
            input_text=content,
            context=context,
            mood=self.current_mood
        )
        
        # Apply tone adjustments
        adjusted_response = await self.tone_matcher.apply_tone(response, tone)
        
        return adjusted_response
    
    async def _send_response(self, 
                           response: str, 
                           platform: str, 
                           original_message: Dict[str, Any]):
        """Send the response through the appropriate platform"""
        
        # This would integrate with the platform manager
        # For now, just log the response
        logger.info(f"📤 Sending response via {platform}: {response[:100]}...")
        
        # In a real implementation, this would call the platform manager
        # await self.platform_manager.send_message(platform, response, original_message)
    
    def _log_response(self, 
                     original_message: Dict[str, Any], 
                     response: str, 
                     intent: Dict[str, Any], 
                     platform: str):
        """Log the response for analysis and improvement"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "original_message": original_message,
            "response": response,
            "intent": intent,
            "mood": self.current_mood,
            "auto_reply": self.auto_reply_enabled
        }
        
        self.response_history.append(log_entry)
        
        # Keep only last 1000 responses
        if len(self.response_history) > 1000:
            self.response_history = self.response_history[-1000:]
    
    def enable_auto_reply(self, enabled: bool = True):
        """Enable or disable automatic responses"""
        self.auto_reply_enabled = enabled
        logger.info(f"🔄 Auto-reply {'enabled' if enabled else 'disabled'}")
    
    def require_override(self, required: bool = True):
        """Set whether manual override is required for all responses"""
        self.override_required = required
        logger.info(f"🔄 Manual override {'required' if required else 'optional'}")
    
    def set_mood(self, mood: str):
        """Set the current response mood"""
        valid_moods = ["default", "energetic", "savage", "unhinged", "professional", "casual"]
        if mood in valid_moods:
            self.current_mood = mood
            logger.info(f"😊 Mood set to: {mood}")
        else:
            logger.warning(f"Invalid mood: {mood}. Using default.")
            self.current_mood = "default"
    
    def get_response_stats(self) -> Dict[str, Any]:
        """Get statistics about generated responses"""
        if not self.response_history:
            return {"total_responses": 0}
        
        total = len(self.response_history)
        platforms = {}
        intents = {}
        moods = {}
        
        for entry in self.response_history:
            # Platform stats
            platform = entry.get("platform", "unknown")
            platforms[platform] = platforms.get(platform, 0) + 1
            
            # Intent stats
            intent_type = entry.get("intent", {}).get("type", "unknown")
            intents[intent_type] = intents.get(intent_type, 0) + 1
            
            # Mood stats
            mood = entry.get("mood", "default")
            moods[mood] = moods.get(mood, 0) + 1
        
        return {
            "total_responses": total,
            "platforms": platforms,
            "intents": intents,
            "moods": moods,
            "auto_reply_rate": sum(1 for e in self.response_history if e.get("auto_reply", False)) / total
        }
    
    def get_recent_responses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent response history"""
        return self.response_history[-limit:]
    
    async def generate_test_response(self, 
                                   test_input: str, 
                                   context: str = "", 
                                   mood: str = None) -> str:
        """Generate a test response without sending it"""
        
        if not self.personality_engine:
            return "Personality engine not available"
        
        # Use specified mood or current mood
        response_mood = mood if mood else self.current_mood
        
        # Generate response
        response = await self.personality_engine.generate_response(
            input_text=test_input,
            context=context,
            mood=response_mood
        )
        
        return response
    
    def clear_history(self):
        """Clear response history"""
        self.response_history = []
        logger.info("🗑️ Response history cleared") 