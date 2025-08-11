"""
Content Filter
Filters inappropriate or harmful content
"""

import logging
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

class ContentFilter:
    """Filters inappropriate or harmful content"""
    
    def __init__(self):
        # Harmful content patterns
        self.harmful_patterns = [
            r"kill yourself", r"commit suicide", r"self harm",
            r"i hate you", r"you're worthless", r"you're stupid",
            r"racist", r"sexist", r"homophobic", r"transphobic",
            r"nazi", r"hitler", r"white supremacy"
        ]
        
        # Inappropriate content patterns
        self.inappropriate_patterns = [
            r"porn", r"sex", r"nude", r"explicit",
            r"drugs", r"cocaine", r"heroin", r"weed",
            r"violence", r"murder", r"assault"
        ]
        
    async def check_content(self, content: str) -> Dict[str, Any]:
        """Check if content is appropriate"""
        try:
            content_lower = content.lower()
            
            # Check for harmful content
            harmful_found = []
            for pattern in self.harmful_patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    harmful_found.append(pattern)
            
            # Check for inappropriate content
            inappropriate_found = []
            for pattern in self.inappropriate_patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    inappropriate_found.append(pattern)
            
            # Determine if content is safe
            is_safe = len(harmful_found) == 0 and len(inappropriate_found) == 0
            
            return {
                "safe": is_safe,
                "reason": self._get_reason(harmful_found, inappropriate_found),
                "harmful_patterns": harmful_found,
                "inappropriate_patterns": inappropriate_found
            }
            
        except Exception as e:
            logger.error(f"Content filtering failed: {e}")
            return {
                "safe": False,
                "reason": f"Content filtering error: {str(e)}",
                "harmful_patterns": [],
                "inappropriate_patterns": []
            }
    
    def _get_reason(self, harmful: List[str], inappropriate: List[str]) -> str:
        """Get reason for content being flagged"""
        if harmful:
            return f"Harmful content detected: {', '.join(harmful)}"
        elif inappropriate:
            return f"Inappropriate content detected: {', '.join(inappropriate)}"
        else:
            return "" 