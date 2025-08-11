"""
Belief Matrix
Manages user beliefs and values for personality modeling
"""

import logging
from typing import Dict, List, Optional, Any
from collections import defaultdict

logger = logging.getLogger(__name__)

class BeliefMatrix:
    """Manages user beliefs and values"""
    
    def __init__(self):
        self.beliefs = defaultdict(dict)
        self.values = defaultdict(float)
        
    async def build_from_data(self, training_data: List[Dict[str, Any]]):
        """Build belief matrix from training data"""
        try:
            # Extract beliefs from training data
            for item in training_data:
                content = item.get("content", "")
                if content:
                    await self._extract_beliefs_from_text(content)
            
            logger.info(f"🧠 Built belief matrix with {len(self.beliefs)} belief categories")
            
        except Exception as e:
            logger.error(f"Failed to build belief matrix: {e}")
    
    async def _extract_beliefs_from_text(self, text: str):
        """Extract beliefs from text content"""
        # This is a simplified implementation
        # In practice, you'd use more sophisticated NLP techniques
        
        text_lower = text.lower()
        
        # Political beliefs
        if any(word in text_lower for word in ["liberal", "progressive", "left"]):
            self.beliefs["politics"]["liberal"] = self.beliefs["politics"].get("liberal", 0) + 1
        if any(word in text_lower for word in ["conservative", "republican", "right"]):
            self.beliefs["politics"]["conservative"] = self.beliefs["politics"].get("conservative", 0) + 1
        
        # Social beliefs
        if any(word in text_lower for word in ["equality", "justice", "rights"]):
            self.beliefs["social"]["equality"] = self.beliefs["social"].get("equality", 0) + 1
        if any(word in text_lower for word in ["tradition", "family", "values"]):
            self.beliefs["social"]["traditional"] = self.beliefs["social"].get("traditional", 0) + 1
        
        # Economic beliefs
        if any(word in text_lower for word in ["capitalism", "free market", "business"]):
            self.beliefs["economics"]["capitalist"] = self.beliefs["economics"].get("capitalist", 0) + 1
        if any(word in text_lower for word in ["socialism", "welfare", "government"]):
            self.beliefs["economics"]["socialist"] = self.beliefs["economics"].get("socialist", 0) + 1
    
    def get_beliefs(self) -> Dict[str, Any]:
        """Get current beliefs"""
        return dict(self.beliefs)
    
    def get_dominant_beliefs(self) -> Dict[str, str]:
        """Get dominant beliefs in each category"""
        dominant = {}
        for category, beliefs in self.beliefs.items():
            if beliefs:
                dominant[category] = max(beliefs, key=beliefs.get)
        return dominant 