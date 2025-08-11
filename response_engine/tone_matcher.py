"""
Tone Matcher
Matches and adjusts response tone based on context
"""

import logging
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

class ToneMatcher:
    """Matches and adjusts response tone based on context"""
    
    def __init__(self):
        self.tone_patterns = {
            "formal": {
                "indicators": ["sir", "madam", "please", "thank you", "regards"],
                "adjustments": ["add formality", "use proper grammar", "be respectful"]
            },
            "casual": {
                "indicators": ["hey", "sup", "cool", "awesome", "lol"],
                "adjustments": ["be relaxed", "use contractions", "be friendly"]
            },
            "professional": {
                "indicators": ["meeting", "project", "deadline", "business"],
                "adjustments": ["be professional", "be concise", "be clear"]
            },
            "friendly": {
                "indicators": ["friend", "buddy", "pal", "😊", "❤️"],
                "adjustments": ["be warm", "be supportive", "be encouraging"]
            },
            "urgent": {
                "indicators": ["asap", "urgent", "emergency", "now"],
                "adjustments": ["be quick", "be direct", "be responsive"]
            }
        }
        
    async def determine_tone(self, 
                           intent: Dict[str, Any], 
                           context: str, 
                           sender: str) -> str:
        """Determine appropriate tone based on intent and context"""
        try:
            # Analyze intent
            intent_type = intent.get("type", "unknown")
            intent_context = intent.get("context", {})
            
            # Default tone
            tone = "neutral"
            
            # Adjust based on intent
            if intent_type == "greeting":
                tone = "friendly"
            elif intent_type == "question":
                tone = "helpful"
            elif intent_type == "request":
                tone = "professional"
            elif intent_type == "complaint":
                tone = "empathetic"
            elif intent_type == "urgent":
                tone = "urgent"
            elif intent_type == "casual":
                tone = "casual"
            
            # Adjust based on context
            if "work" in context.lower() or "business" in context.lower():
                tone = "professional"
            elif "friend" in context.lower() or "family" in context.lower():
                tone = "friendly"
            
            # Adjust based on sender relationship
            if sender in ["boss", "manager", "supervisor"]:
                tone = "professional"
            elif sender in ["friend", "family", "close"]:
                tone = "casual"
            
            return tone
            
        except Exception as e:
            logger.error(f"Tone determination failed: {e}")
            return "neutral"
    
    async def apply_tone(self, response: str, tone: str) -> str:
        """Apply tone adjustments to a response"""
        try:
            if tone == "neutral":
                return response
            
            # Get tone adjustments
            tone_config = self.tone_patterns.get(tone, {})
            adjustments = tone_config.get("adjustments", [])
            
            # Apply adjustments (simplified for now)
            adjusted_response = response
            
            if "formal" in adjustments:
                # Add formality
                if not response.startswith(("Dear", "Hello", "Hi")):
                    adjusted_response = f"Hello, {response}"
            
            elif "casual" in adjustments:
                # Make more casual
                adjusted_response = response.replace("Hello", "Hey").replace("Thank you", "Thanks")
            
            elif "professional" in adjustments:
                # Make more professional
                if "lol" in adjusted_response.lower():
                    adjusted_response = adjusted_response.replace("lol", "").replace("LOL", "")
            
            elif "friendly" in adjustments:
                # Add warmth
                if not any(emoji in adjusted_response for emoji in ["😊", "❤️", "👍"]):
                    adjusted_response += " 😊"
            
            elif "urgent" in adjustments:
                # Make more urgent
                if "!" not in adjusted_response:
                    adjusted_response += "!"
            
            return adjusted_response
            
        except Exception as e:
            logger.error(f"Tone application failed: {e}")
            return response 