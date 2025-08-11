"""
Text Processor
Analyzes personality traits and style patterns from text data
"""

import re
import logging
from typing import Dict, List, Optional, Any
from collections import Counter, defaultdict
import emoji
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import numpy as np

logger = logging.getLogger(__name__)

class TextProcessor:
    """Processes text data to extract personality traits and style patterns"""
    
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
        
        # Personality trait indicators
        self.trait_indicators = {
            "humor": {
                "sarcastic": ["lol", "haha", "😂", "😅", "😆", "sarcasm", "obviously", "duh"],
                "wholesome": ["❤️", "💕", "😊", "aww", "cute", "sweet", "lovely"],
                "dark": ["💀", "😈", "😱", "horror", "scary", "death"],
                "absurdist": ["🤪", "😵‍💫", "random", "wtf", "what", "why"]
            },
            "formality": {
                "casual": ["hey", "hi", "yo", "sup", "cool", "awesome", "nice"],
                "formal": ["sincerely", "regards", "dear", "please", "thank you"],
                "professional": ["regarding", "furthermore", "consequently", "therefore"]
            },
            "energy": {
                "high": ["!!!", "🔥", "💯", "amazing", "incredible", "wow"],
                "low": ["...", "meh", "whatever", "okay", "fine"],
                "chaotic": ["😵‍💫", "🤯", "💥", "explosion", "chaos", "random"]
            }
        }
    
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a Discord message for personality analysis"""
        try:
            content = message.get("content", "")
            if not content or len(content.strip()) < 3:
                return None
            
            # Basic text analysis
            analysis = self._analyze_text(content)
            
            # Extract personality indicators
            personality = self._extract_personality_indicators(content)
            
            # Combine with original message data
            processed = {
                **message,
                "analysis": analysis,
                "personality": personality
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}")
            return None
    
    def process_email(self, email: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process an email for personality analysis"""
        try:
            content = email.get("content", "")
            if not content:
                return None
            
            # Basic text analysis
            analysis = self._analyze_text(content)
            
            # Extract personality indicators
            personality = self._extract_personality_indicators(content)
            
            # Email-specific analysis
            email_analysis = self._analyze_email_structure(email)
            
            processed = {
                **email,
                "analysis": analysis,
                "personality": personality,
                "email_analysis": email_analysis
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Failed to process email: {e}")
            return None
    
    def process_post(self, post: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a social media post for personality analysis"""
        try:
            content = post.get("content", "")
            if not content:
                return None
            
            # Basic text analysis
            analysis = self._analyze_text(content)
            
            # Extract personality indicators
            personality = self._extract_personality_indicators(content)
            
            # Post-specific analysis
            post_analysis = self._analyze_post_engagement(post)
            
            processed = {
                **post,
                "analysis": analysis,
                "personality": personality,
                "post_analysis": post_analysis
            }
            
            return processed
            
        except Exception as e:
            logger.error(f"Failed to process post: {e}")
            return None
    
    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Perform basic text analysis"""
        try:
            blob = TextBlob(text)
            
            # Basic statistics
            sentences = sent_tokenize(text)
            words = word_tokenize(text.lower())
            words_no_stop = [w for w in words if w.isalpha() and w not in self.stop_words]
            
            # Emoji analysis
            emoji_list = emoji.emoji_list(text)
            emoji_count = len(emoji_list)
            
            # Punctuation analysis
            punctuation = re.findall(r'[^\w\s]', text)
            punctuation_count = len(punctuation)
            
            # Capitalization analysis
            caps_count = len(re.findall(r'[A-Z]', text))
            caps_ratio = caps_count / len(text) if text else 0
            
            # Sentiment analysis
            sentiment = blob.sentiment
            
            analysis = {
                "length": {
                    "characters": len(text),
                    "words": len(words),
                    "sentences": len(sentences),
                    "words_no_stop": len(words_no_stop)
                },
                "complexity": {
                    "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
                    "avg_word_length": np.mean([len(w) for w in words]) if words else 0,
                    "unique_words_ratio": len(set(words)) / len(words) if words else 0
                },
                "style": {
                    "emoji_count": emoji_count,
                    "emoji_list": [e['emoji'] for e in emoji_list],
                    "punctuation_count": punctuation_count,
                    "punctuation_types": Counter(punctuation),
                    "caps_ratio": caps_ratio,
                    "exclamation_count": text.count('!'),
                    "question_count": text.count('?'),
                    "ellipsis_count": text.count('...')
                },
                "sentiment": {
                    "polarity": sentiment.polarity,
                    "subjectivity": sentiment.subjectivity
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            return {}
    
    def _extract_personality_indicators(self, text: str) -> Dict[str, Any]:
        """Extract personality indicators from text"""
        text_lower = text.lower()
        
        personality = {
            "humor_type": self._classify_humor(text_lower),
            "formality_level": self._classify_formality(text_lower),
            "energy_level": self._classify_energy(text_lower),
            "communication_style": self._classify_communication_style(text),
            "emoji_usage": self._analyze_emoji_usage(text),
            "punctuation_style": self._analyze_punctuation_style(text)
        }
        
        return personality
    
    def _classify_humor(self, text: str) -> str:
        """Classify the type of humor used"""
        scores = {
            "sarcastic": 0,
            "wholesome": 0,
            "dark": 0,
            "absurdist": 0
        }
        
        for humor_type, indicators in self.trait_indicators["humor"].items():
            for indicator in indicators:
                if indicator.lower() in text:
                    scores[humor_type] += 1
        
        if max(scores.values()) == 0:
            return "neutral"
        
        return max(scores, key=scores.get)
    
    def _classify_formality(self, text: str) -> str:
        """Classify the formality level"""
        scores = {
            "casual": 0,
            "formal": 0,
            "professional": 0
        }
        
        for formality_type, indicators in self.trait_indicators["formality"].items():
            for indicator in indicators:
                if indicator.lower() in text:
                    scores[formality_type] += 1
        
        if max(scores.values()) == 0:
            return "neutral"
        
        return max(scores, key=scores.get)
    
    def _classify_energy(self, text: str) -> str:
        """Classify the energy level"""
        scores = {
            "high": 0,
            "low": 0,
            "chaotic": 0
        }
        
        for energy_type, indicators in self.trait_indicators["energy"].items():
            for indicator in indicators:
                if indicator.lower() in text:
                    scores[energy_type] += 1
        
        # Count exclamation marks and caps
        scores["high"] += text.count('!') * 2
        scores["high"] += len(re.findall(r'[A-Z]{3,}', text))
        
        if max(scores.values()) == 0:
            return "neutral"
        
        return max(scores, key=scores.get)
    
    def _classify_communication_style(self, text: str) -> str:
        """Classify communication style"""
        # Analyze patterns
        if re.search(r'[A-Z]{3,}', text):  # ALL CAPS
            return "emphatic"
        elif text.count('...') > 2:  # Lots of ellipsis
            return "contemplative"
        elif text.count('!') > 3:  # Lots of exclamations
            return "enthusiastic"
        elif len(text) < 50:  # Very short
            return "concise"
        elif len(text) > 500:  # Very long
            return "detailed"
        else:
            return "balanced"
    
    def _analyze_emoji_usage(self, text: str) -> Dict[str, Any]:
        """Analyze emoji usage patterns"""
        emoji_list = emoji.emoji_list(text)
        
        if not emoji_list:
            return {"frequent": False, "types": [], "count": 0}
        
        emoji_types = [e['emoji'] for e in emoji_list]
        
        return {
            "frequent": len(emoji_list) > 2,
            "types": list(set(emoji_types)),
            "count": len(emoji_list),
            "diversity": len(set(emoji_types)) / len(emoji_types) if emoji_types else 0
        }
    
    def _analyze_punctuation_style(self, text: str) -> Dict[str, Any]:
        """Analyze punctuation style"""
        return {
            "exclamation_frequent": text.count('!') > 2,
            "question_frequent": text.count('?') > 2,
            "ellipsis_frequent": text.count('...') > 1,
            "caps_frequent": len(re.findall(r'[A-Z]{3,}', text)) > 0,
            "punctuation_density": len(re.findall(r'[^\w\s]', text)) / len(text) if text else 0
        }
    
    def _analyze_email_structure(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze email structure and formality"""
        subject = email.get("subject", "")
        content = email.get("content", "")
        
        # Analyze greeting and closing
        greetings = ["dear", "hi", "hello", "hey", "good morning", "good afternoon"]
        closings = ["sincerely", "regards", "best", "thanks", "cheers", "bye"]
        
        has_greeting = any(greeting in content.lower()[:100] for greeting in greetings)
        has_closing = any(closing in content.lower()[-100:] for closing in closings)
        
        return {
            "has_greeting": has_greeting,
            "has_closing": has_closing,
            "subject_length": len(subject),
            "formal_structure": has_greeting and has_closing
        }
    
    def _analyze_post_engagement(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze post engagement patterns"""
        return {
            "hashtags": len(re.findall(r'#\w+', post.get("content", ""))),
            "mentions": len(re.findall(r'@\w+', post.get("content", ""))),
            "links": len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post.get("content", ""))),
            "engagement_rate": post.get("engagement_rate", 0)
        }
    
    async def analyze_personality(self, texts: List[str]) -> Dict[str, Any]:
        """Analyze personality traits across multiple texts"""
        if not texts:
            return {}
        
        # Aggregate analysis across all texts
        all_analyses = []
        all_personalities = []
        
        for text in texts:
            analysis = self._analyze_text(text)
            personality = self._extract_personality_indicators(text)
            
            if analysis:
                all_analyses.append(analysis)
            if personality:
                all_personalities.append(personality)
        
        if not all_analyses:
            return {}
        
        # Aggregate statistics
        avg_sentiment = np.mean([a.get("sentiment", {}).get("polarity", 0) for a in all_analyses])
        avg_subjectivity = np.mean([a.get("sentiment", {}).get("subjectivity", 0) for a in all_analyses])
        
        # Most common personality traits
        humor_types = [p.get("humor_type", "neutral") for p in all_personalities]
        formality_levels = [p.get("formality_level", "neutral") for p in all_personalities]
        energy_levels = [p.get("energy_level", "neutral") for p in all_personalities]
        
        # Style patterns
        emoji_usage = [p.get("emoji_usage", {}).get("frequent", False) for p in all_personalities]
        emoji_frequency = sum(emoji_usage) / len(emoji_usage) if emoji_usage else 0
        
        return {
            "overall_sentiment": {
                "polarity": avg_sentiment,
                "subjectivity": avg_subjectivity
            },
            "dominant_traits": {
                "humor": Counter(humor_types).most_common(1)[0][0] if humor_types else "neutral",
                "formality": Counter(formality_levels).most_common(1)[0][0] if formality_levels else "neutral",
                "energy": Counter(energy_levels).most_common(1)[0][0] if energy_levels else "neutral"
            },
            "style_preferences": {
                "emoji_frequent": emoji_frequency > 0.3,
                "emoji_frequency": emoji_frequency,
                "avg_message_length": np.mean([a.get("length", {}).get("words", 0) for a in all_analyses]),
                "avg_sentence_length": np.mean([a.get("complexity", {}).get("avg_sentence_length", 0) for a in all_analyses])
            }
        }
    
    async def extract_style_patterns(self, texts: List[str]) -> Dict[str, Any]:
        """Extract writing style patterns"""
        if not texts:
            return {}
        
        # Analyze common patterns
        all_words = []
        all_emojis = []
        all_punctuation = []
        
        for text in texts:
            words = word_tokenize(text.lower())
            all_words.extend([w for w in words if w.isalpha()])
            
            emoji_list = emoji.emoji_list(text)
            all_emojis.extend([e['emoji'] for e in emoji_list])
            
            punctuation = re.findall(r'[^\w\s]', text)
            all_punctuation.extend(punctuation)
        
        # Most common words (excluding stop words)
        word_freq = Counter(all_words)
        common_words = [word for word, count in word_freq.most_common(20) 
                       if word not in self.stop_words and len(word) > 2]
        
        # Most common emojis
        emoji_freq = Counter(all_emojis)
        common_emojis = [emoji for emoji, count in emoji_freq.most_common(10)]
        
        # Punctuation patterns
        punct_freq = Counter(all_punctuation)
        common_punctuation = [punct for punct, count in punct_freq.most_common(5)]
        
        return {
            "vocabulary": {
                "common_words": common_words,
                "vocabulary_size": len(set(all_words)),
                "word_diversity": len(set(all_words)) / len(all_words) if all_words else 0
            },
            "emoji_patterns": {
                "common_emojis": common_emojis,
                "emoji_diversity": len(set(all_emojis)) / len(all_emojis) if all_emojis else 0,
                "total_emojis": len(all_emojis)
            },
            "punctuation_patterns": {
                "common_punctuation": common_punctuation,
                "punctuation_diversity": len(set(all_punctuation)) / len(all_punctuation) if all_punctuation else 0
            }
        } 