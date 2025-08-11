"""
Consent Manager
Manages user consent for AI interactions
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ConsentManager:
    """Manages user consent for AI interactions"""
    
    def __init__(self):
        self.consented_contacts = set()
        self.consent_history = []
        
    async def check_consent(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Check if we have consent to respond to this sender"""
        try:
            sender = message.get("sender", "")
            platform = message.get("platform", "")
            
            # Check if sender has consented
            if sender in self.consented_contacts:
                return {
                    "consented": True,
                    "reason": "Sender has previously consented"
                }
            
            # Check if this is a new contact
            if not sender:
                return {
                    "consented": False,
                    "reason": "Unknown sender"
                }
            
            # For now, assume consent for known platforms
            # In a real implementation, you'd have more sophisticated consent management
            if platform in ["discord", "email", "slack"]:
                return {
                    "consented": True,
                    "reason": "Platform-based consent"
                }
            
            return {
                "consented": False,
                "reason": "No consent on file for this sender"
            }
            
        except Exception as e:
            logger.error(f"Consent check failed: {e}")
            return {
                "consented": False,
                "reason": f"Consent check error: {str(e)}"
            }
    
    def add_consent(self, sender: str, platform: str = ""):
        """Add consent for a sender"""
        self.consented_contacts.add(sender)
        
        consent_record = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "platform": platform,
            "action": "consent_granted"
        }
        
        self.consent_history.append(consent_record)
        logger.info(f"✅ Consent added for {sender}")
    
    def remove_consent(self, sender: str):
        """Remove consent for a sender"""
        self.consented_contacts.discard(sender)
        
        consent_record = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "action": "consent_revoked"
        }
        
        self.consent_history.append(consent_record)
        logger.info(f"❌ Consent removed for {sender}")
    
    def get_consented_contacts(self) -> List[str]:
        """Get list of contacts who have consented"""
        return list(self.consented_contacts)
    
    def get_consent_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get consent history"""
        return self.consent_history[-limit:] 