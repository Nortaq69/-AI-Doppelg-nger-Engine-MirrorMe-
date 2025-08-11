"""
Personality Core Module
Handles AI personality modeling and style transfer
"""

from .personality_engine import PersonalityEngine
from .style_embedding import StyleEmbedding
from .belief_matrix import BeliefMatrix

__all__ = [
    'PersonalityEngine',
    'StyleEmbedding', 
    'BeliefMatrix'
] 