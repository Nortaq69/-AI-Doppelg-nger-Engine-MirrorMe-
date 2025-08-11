"""
Intent Classifier
Classifies the intent of incoming messages
"""

import logging
from typing import Dict, List, Optional, Any
import re

logger = logging.getLogger(__name__)

class IntentClassifier:
    """Classifies the intent of incoming messages"""
    
    def __init__(self):
        # Intent patterns
        self.intent_patterns = {
            "greeting": [
                r"hi", r"hello", r"hey", r"sup", r"what's up", r"howdy",
                r"good morning", r"good afternoon", r"good evening"
            ],
            "question": [
                r"\?", r"what", r"how", r"why", r"when", r"where", r"who",
                r"can you", r"could you", r"would you", r"do you"
            ],
            "request": [
                r"please", r"can you", r"could you", r"would you mind",
                r"i need", r"i want", r"help me", r"assist"
            ],
            "compliment": [
                r"you're great", r"you're awesome", r"you're amazing",
                r"thank you", r"thanks", r"appreciate", r"love it"
            ],
            "complaint": [
                r"problem", r"issue", r"wrong", r"broken", r"doesn't work",
                r"annoying", r"frustrated", r"angry", r"upset"
            ],
            "casual": [
                r"lol", r"haha", r"😄", r"😂", r"cool", r"nice", r"awesome",
                r"yeah", r"sure", r"okay", r"whatever"
            ],
            "urgent": [
                r"asap", r"urgent", r"emergency", r"now", r"quick",
                r"important", r"critical", r"immediately"
            ]
        }
        
    async def classify_intent(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Classify the intent of a message"""
        try:
            content = message.get("content", "").lower()
            sender = message.get("sender", "")
            platform = message.get("platform", "")
            
            # Score each intent
            intent_scores = {}
            for intent, patterns in self.intent_patterns.items():
                score = 0
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        score += 1
                intent_scores[intent] = score
            
            # Get primary intent
            primary_intent = max(intent_scores, key=intent_scores.get) if intent_scores else "unknown"
            
            # Determine confidence
            max_score = max(intent_scores.values()) if intent_scores else 0
            confidence = min(max_score / 3, 1.0)  # Normalize confidence
            
            # Additional context
            context = {
                "is_question": "?" in content,
                "has_emoji": bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000027BF]', content)),
                "is_caps": content.isupper(),
                "length": len(content),
                "platform": platform,
                "sender_known": bool(sender)
            }
            
            return {
                "type": primary_intent,
                "confidence": confidence,
                "scores": intent_scores,
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return {
                "type": "unknown",
                "confidence": 0.0,
                "scores": {},
                "context": {}
            } 