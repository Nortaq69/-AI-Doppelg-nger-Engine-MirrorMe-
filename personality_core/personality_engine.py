"""
Personality Engine
Builds and manages the AI's personality model based on user data
"""

import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
import openai

from .style_embedding import StyleEmbedding
from .belief_matrix import BeliefMatrix

logger = logging.getLogger(__name__)

class PersonalityEngine:
    """Core personality modeling engine for the AI doppelgänger"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.sentence_model = None
        self.style_embedding = StyleEmbedding()
        self.belief_matrix = BeliefMatrix()
        
        # Personality state
        self.personality_profile = {}
        self.style_patterns = {}
        self.trained = False
        
        # Vector database for similarity search
        self.embeddings = []
        self.texts = []
        
        logger.info("🧠 Personality Engine initialized")
    
    async def train_personality(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Train the personality model on user data"""
        logger.info("🎯 Training personality model...")
        
        try:
            # Initialize sentence transformer
            if not self.sentence_model:
                self.sentence_model = SentenceTransformer(self.model_name)
            
            # Extract personality traits
            self.personality_profile = await self._extract_personality_traits(training_data)
            
            # Build style patterns
            self.style_patterns = await self._build_style_patterns(training_data)
            
            # Create belief matrix
            await self.belief_matrix.build_from_data(training_data)
            
            # Build embedding database for similarity search
            await self._build_embedding_database(training_data)
            
            self.trained = True
            logger.info("✅ Personality model training complete")
            
            return {
                "success": True,
                "personality_profile": self.personality_profile,
                "style_patterns": self.style_patterns,
                "training_samples": len(training_data)
            }
            
        except Exception as e:
            logger.error(f"❌ Personality training failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _extract_personality_traits(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract personality traits from training data"""
        traits = {
            "communication_style": {},
            "humor_type": {},
            "formality_level": {},
            "energy_level": {},
            "emotional_patterns": {},
            "interests": {},
            "values": {}
        }
        
        # Aggregate personality indicators from all training data
        all_personalities = []
        for item in training_data:
            if "personality" in item:
                all_personalities.append(item["personality"])
        
        if not all_personalities:
            return traits
        
        # Analyze communication style
        comm_styles = [p.get("communication_style", "balanced") for p in all_personalities]
        traits["communication_style"] = {
            "primary": self._get_most_common(comm_styles),
            "distribution": dict(Counter(comm_styles))
        }
        
        # Analyze humor type
        humor_types = [p.get("humor_type", "neutral") for p in all_personalities]
        traits["humor_type"] = {
            "primary": self._get_most_common(humor_types),
            "distribution": dict(Counter(humor_types))
        }
        
        # Analyze formality level
        formality_levels = [p.get("formality_level", "neutral") for p in all_personalities]
        traits["formality_level"] = {
            "primary": self._get_most_common(formality_levels),
            "distribution": dict(Counter(formality_levels))
        }
        
        # Analyze energy level
        energy_levels = [p.get("energy_level", "neutral") for p in all_personalities]
        traits["energy_level"] = {
            "primary": self._get_most_common(energy_levels),
            "distribution": dict(Counter(energy_levels))
        }
        
        # Analyze emoji usage
        emoji_usage = [p.get("emoji_usage", {}).get("frequent", False) for p in all_personalities]
        traits["emoji_preference"] = {
            "frequent_user": sum(emoji_usage) / len(emoji_usage) > 0.3,
            "frequency": sum(emoji_usage) / len(emoji_usage)
        }
        
        return traits
    
    async def _build_style_patterns(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build style patterns from training data"""
        patterns = {
            "vocabulary": {},
            "sentence_structure": {},
            "punctuation": {},
            "emoji_patterns": {},
            "response_patterns": {}
        }
        
        # Extract all text content
        all_texts = []
        for item in training_data:
            content = item.get("content", "")
            if content:
                all_texts.append(content)
        
        if not all_texts:
            return patterns
        
        # Analyze vocabulary patterns
        all_words = []
        for text in all_texts:
            words = text.lower().split()
            all_words.extend([w for w in words if w.isalpha() and len(w) > 2])
        
        word_freq = Counter(all_words)
        patterns["vocabulary"] = {
            "common_words": [word for word, count in word_freq.most_common(20)],
            "vocabulary_size": len(set(all_words)),
            "word_diversity": len(set(all_words)) / len(all_words) if all_words else 0
        }
        
        # Analyze sentence structure
        sentence_lengths = []
        for text in all_texts:
            sentences = text.split('.')
            sentence_lengths.extend([len(s.split()) for s in sentences if s.strip()])
        
        patterns["sentence_structure"] = {
            "avg_sentence_length": np.mean(sentence_lengths) if sentence_lengths else 0,
            "sentence_length_variance": np.var(sentence_lengths) if sentence_lengths else 0
        }
        
        # Analyze punctuation patterns
        punct_patterns = {}
        for text in all_texts:
            punct_patterns["exclamation"] = punct_patterns.get("exclamation", 0) + text.count('!')
            punct_patterns["question"] = punct_patterns.get("question", 0) + text.count('?')
            punct_patterns["ellipsis"] = punct_patterns.get("ellipsis", 0) + text.count('...')
        
        patterns["punctuation"] = punct_patterns
        
        return patterns
    
    async def _build_embedding_database(self, training_data: List[Dict[str, Any]]):
        """Build embedding database for similarity search"""
        if not self.sentence_model:
            return
        
        texts = []
        for item in training_data:
            content = item.get("content", "")
            if content and len(content.strip()) > 10:
                texts.append(content.strip())
        
        if not texts:
            return
        
        # Generate embeddings
        embeddings = self.sentence_model.encode(texts)
        
        self.embeddings = embeddings
        self.texts = texts
        
        logger.info(f"📚 Built embedding database with {len(texts)} texts")
    
    def _get_most_common(self, items: List[str]) -> str:
        """Get the most common item from a list"""
        if not items:
            return "neutral"
        
        counter = Counter(items)
        return counter.most_common(1)[0][0]
    
    async def generate_response(self, 
                              input_text: str, 
                              context: str = "", 
                              mood: str = "default") -> str:
        """Generate a response in the user's style"""
        if not self.trained:
            return "I'm still learning your personality. Please train me first!"
        
        try:
            # Find similar responses from training data
            similar_responses = await self._find_similar_responses(input_text, context)
            
            # Generate response using OpenAI with personality guidance
            response = await self._generate_with_personality(input_text, context, mood, similar_responses)
            
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "Sorry, I'm having trouble responding right now."
    
    async def _find_similar_responses(self, input_text: str, context: str = "") -> List[str]:
        """Find similar responses from training data"""
        if not self.sentence_model or not self.embeddings.size:
            return []
        
        # Generate embedding for input
        input_embedding = self.sentence_model.encode([input_text])
        
        # Calculate similarities
        similarities = np.dot(self.embeddings, input_embedding.T).flatten()
        
        # Get top similar responses
        top_indices = np.argsort(similarities)[-5:][::-1]  # Top 5
        
        similar_responses = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Similarity threshold
                similar_responses.append(self.texts[idx])
        
        return similar_responses
    
    async def _generate_with_personality(self, 
                                       input_text: str, 
                                       context: str, 
                                       mood: str, 
                                       similar_responses: List[str]) -> str:
        """Generate response using OpenAI with personality guidance"""
        
        # Build personality prompt
        personality_prompt = self._build_personality_prompt(mood)
        
        # Build context from similar responses
        context_examples = "\n".join(similar_responses[:3]) if similar_responses else ""
        
        # Create the full prompt
        prompt = f"""
{personality_prompt}

Your communication style:
- Primary humor: {self.personality_profile.get('humor_type', {}).get('primary', 'neutral')}
- Formality level: {self.personality_profile.get('formality_level', {}).get('primary', 'neutral')}
- Energy level: {self.personality_profile.get('energy_level', {}).get('primary', 'neutral')}
- Emoji usage: {'Frequent' if self.personality_profile.get('emoji_preference', {}).get('frequent_user', False) else 'Occasional'}

Example responses in your style:
{context_examples}

Context: {context}

Input: {input_text}

Respond in your authentic style:
"""
        
        try:
            # Use OpenAI to generate response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are responding as the user's digital twin. Match their exact communication style, humor, and personality."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            # Fallback to simple response
            return self._generate_fallback_response(input_text, mood)
    
    def _build_personality_prompt(self, mood: str) -> str:
        """Build personality prompt based on mood"""
        base_prompt = "You are responding as the user's digital twin. "
        
        mood_modifiers = {
            "default": "",
            "energetic": "Be more enthusiastic and high-energy in your response. ",
            "savage": "Be more sarcastic and witty. Don't hold back. ",
            "unhinged": "Be chaotic and unpredictable. Embrace the chaos. ",
            "professional": "Be more formal and business-like. ",
            "casual": "Be more relaxed and informal. "
        }
        
        return base_prompt + mood_modifiers.get(mood, "")
    
    def _generate_fallback_response(self, input_text: str, mood: str) -> str:
        """Generate a simple fallback response"""
        responses = {
            "default": ["Got it!", "Sure thing!", "Makes sense."],
            "energetic": ["YES! 🔥", "Absolutely! 💯", "Let's go! 🚀"],
            "savage": ["Obviously.", "Duh.", "Sure, whatever."],
            "unhinged": ["😵‍💫", "🤯", "💥"],
            "professional": ["Understood.", "I'll take care of that.", "Noted."],
            "casual": ["Cool!", "Got it!", "Sounds good!"]
        }
        
        mood_responses = responses.get(mood, responses["default"])
        return np.random.choice(mood_responses)
    
    def is_trained(self) -> bool:
        """Check if the personality model is trained"""
        return self.trained
    
    def get_personality_profile(self) -> Dict[str, Any]:
        """Get the current personality profile"""
        return self.personality_profile
    
    def get_style_patterns(self) -> Dict[str, Any]:
        """Get the current style patterns"""
        return self.style_patterns
    
    def update_mood(self, mood: str):
        """Update the current mood setting"""
        self.current_mood = mood
    
    def save_model(self, filepath: str):
        """Save the trained model to disk"""
        if not self.trained:
            logger.warning("Cannot save untrained model")
            return
        
        model_data = {
            "personality_profile": self.personality_profile,
            "style_patterns": self.style_patterns,
            "trained": self.trained,
            "model_name": self.model_name
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(model_data, f, indent=2)
            logger.info(f"💾 Model saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")
    
    def load_model(self, filepath: str):
        """Load a trained model from disk"""
        try:
            with open(filepath, 'r') as f:
                model_data = json.load(f)
            
            self.personality_profile = model_data.get("personality_profile", {})
            self.style_patterns = model_data.get("style_patterns", {})
            self.trained = model_data.get("trained", False)
            self.model_name = model_data.get("model_name", self.model_name)
            
            logger.info(f"📂 Model loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}") 