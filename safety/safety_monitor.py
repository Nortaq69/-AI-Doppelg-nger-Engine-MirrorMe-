"""
Safety Monitor
Ensures ethical and safe AI behavior
"""

import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from .content_filter import ContentFilter
from .consent_manager import ConsentManager

logger = logging.getLogger(__name__)

class SafetyMonitor:
    """Monitors AI behavior for safety and ethical concerns"""
    
    def __init__(self):
        self.content_filter = ContentFilter()
        self.consent_manager = ConsentManager()
        
        # Safety settings
        self.safety_mode = "strict"  # strict, moderate, lenient
        self.redlines = set()
        self.sensitive_topics = set()
        
        # Safety history
        self.safety_events = []
        
        # Load default safety settings
        self._load_default_settings()
        
        logger.info("🛡️ Safety Monitor initialized")
    
    def _load_default_settings(self):
        """Load default safety settings"""
        
        # Default redlines - things the AI should never say
        self.redlines = {
            "passwords", "credit cards", "social security", "bank account",
            "personal address", "phone number", "family secrets",
            "confidential information", "trade secrets", "private keys"
        }
        
        # Sensitive topics that require extra caution
        self.sensitive_topics = {
            "politics", "religion", "money", "health", "relationships",
            "work conflicts", "legal issues", "family problems"
        }
    
    async def check_response(self, 
                           response: str, 
                           original_message: Dict[str, Any]) -> Dict[str, Any]:
        """Check if a response is safe to send"""
        
        try:
            safety_result = {
                "safe": True,
                "reason": "",
                "confidence": 1.0,
                "flags": []
            }
            
            # Check for redlines
            redline_check = self._check_redlines(response)
            if not redline_check["safe"]:
                safety_result["safe"] = False
                safety_result["reason"] = f"Redline violation: {redline_check['reason']}"
                safety_result["flags"].append("redline")
            
            # Check content filter
            content_check = await self.content_filter.check_content(response)
            if not content_check["safe"]:
                safety_result["safe"] = False
                safety_result["reason"] = f"Content filter: {content_check['reason']}"
                safety_result["flags"].append("content")
            
            # Check consent
            consent_check = await self.consent_manager.check_consent(original_message)
            if not consent_check["consented"]:
                safety_result["safe"] = False
                safety_result["reason"] = f"Consent issue: {consent_check['reason']}"
                safety_result["flags"].append("consent")
            
            # Check for relationship risks
            relationship_check = self._check_relationship_risks(response, original_message)
            if not relationship_check["safe"]:
                safety_result["safe"] = False
                safety_result["reason"] = f"Relationship risk: {relationship_check['reason']}"
                safety_result["flags"].append("relationship")
            
            # Log safety event
            self._log_safety_event(response, original_message, safety_result)
            
            return safety_result
            
        except Exception as e:
            logger.error(f"Safety check failed: {e}")
            return {
                "safe": False,
                "reason": f"Safety check error: {str(e)}",
                "confidence": 0.0,
                "flags": ["error"]
            }
    
    def _check_redlines(self, response: str) -> Dict[str, Any]:
        """Check if response violates any redlines"""
        
        response_lower = response.lower()
        
        for redline in self.redlines:
            if redline in response_lower:
                return {
                    "safe": False,
                    "reason": f"Contains redline term: {redline}"
                }
        
        # Check for potential personal information patterns
        patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
            r'\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b',  # Phone number
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
        ]
        
        for pattern in patterns:
            if re.search(pattern, response):
                return {
                    "safe": False,
                    "reason": "Contains potential personal information"
                }
        
        return {"safe": True, "reason": ""}
    
    def _check_relationship_risks(self, 
                                response: str, 
                                original_message: Dict[str, Any]) -> Dict[str, Any]:
        """Check for potential relationship-damaging content"""
        
        # High-risk phrases that could damage relationships
        risk_phrases = [
            "i hate you", "you're stupid", "you're wrong", "i don't care",
            "whatever", "i don't want to talk to you", "leave me alone",
            "you're annoying", "i'm done with you", "goodbye forever"
        ]
        
        response_lower = response.lower()
        
        for phrase in risk_phrases:
            if phrase in response_lower:
                return {
                    "safe": False,
                    "reason": f"Contains relationship risk phrase: {phrase}"
                }
        
        # Check for overly aggressive tone
        aggressive_indicators = [
            response.count('!') > 3,  # Too many exclamations
            response.count('CAPS') > 0,  # ALL CAPS
            len(re.findall(r'\b[A-Z]{3,}\b', response)) > 0  # Multiple caps words
        ]
        
        if any(aggressive_indicators):
            return {
                "safe": False,
                "reason": "Aggressive tone detected"
            }
        
        return {"safe": True, "reason": ""}
    
    def _log_safety_event(self, 
                         response: str, 
                         original_message: Dict[str, Any], 
                         safety_result: Dict[str, Any]):
        """Log safety events for monitoring"""
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "response": response[:200] + "..." if len(response) > 200 else response,
            "original_message": original_message.get("content", "")[:100] + "..." if len(original_message.get("content", "")) > 100 else original_message.get("content", ""),
            "sender": original_message.get("sender", "unknown"),
            "platform": original_message.get("platform", "unknown"),
            "safe": safety_result["safe"],
            "reason": safety_result["reason"],
            "flags": safety_result["flags"]
        }
        
        self.safety_events.append(event)
        
        # Keep only last 1000 events
        if len(self.safety_events) > 1000:
            self.safety_events = self.safety_events[-1000:]
        
        # Log to file if safety issue
        if not safety_result["safe"]:
            logger.warning(f"🚨 Safety issue: {safety_result['reason']}")
    
    def add_redline(self, term: str):
        """Add a new redline term"""
        self.redlines.add(term.lower())
        logger.info(f"🔴 Added redline: {term}")
    
    def remove_redline(self, term: str):
        """Remove a redline term"""
        self.redlines.discard(term.lower())
        logger.info(f"🟢 Removed redline: {term}")
    
    def add_sensitive_topic(self, topic: str):
        """Add a sensitive topic"""
        self.sensitive_topics.add(topic.lower())
        logger.info(f"⚠️ Added sensitive topic: {topic}")
    
    def set_safety_mode(self, mode: str):
        """Set safety mode (strict, moderate, lenient)"""
        valid_modes = ["strict", "moderate", "lenient"]
        if mode in valid_modes:
            self.safety_mode = mode
            logger.info(f"🛡️ Safety mode set to: {mode}")
        else:
            logger.warning(f"Invalid safety mode: {mode}")
    
    def get_safety_stats(self) -> Dict[str, Any]:
        """Get safety monitoring statistics"""
        if not self.safety_events:
            return {"total_events": 0}
        
        total_events = len(self.safety_events)
        unsafe_events = sum(1 for event in self.safety_events if not event["safe"])
        
        # Flag breakdown
        flag_counts = {}
        for event in self.safety_events:
            for flag in event.get("flags", []):
                flag_counts[flag] = flag_counts.get(flag, 0) + 1
        
        # Platform breakdown
        platform_counts = {}
        for event in self.safety_events:
            platform = event.get("platform", "unknown")
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        return {
            "total_events": total_events,
            "unsafe_events": unsafe_events,
            "safety_rate": (total_events - unsafe_events) / total_events if total_events > 0 else 1.0,
            "flag_breakdown": flag_counts,
            "platform_breakdown": platform_counts,
            "current_mode": self.safety_mode,
            "redlines_count": len(self.redlines),
            "sensitive_topics_count": len(self.sensitive_topics)
        }
    
    def get_recent_safety_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent safety events"""
        return self.safety_events[-limit:]
    
    def get_mode(self) -> str:
        """Get current safety mode"""
        return self.safety_mode
    
    def clear_safety_history(self):
        """Clear safety event history"""
        self.safety_events = []
        logger.info("🗑️ Safety history cleared") 