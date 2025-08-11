"""
Style Embedding
Handles style embedding and similarity matching
"""

import logging
from typing import Dict, List, Optional, Any
import numpy as np

logger = logging.getLogger(__name__)

class StyleEmbedding:
    """Handles style embedding and similarity matching"""
    
    def __init__(self):
        self.embeddings = []
        self.texts = []
        
    def add_text(self, text: str, embedding: np.ndarray):
        """Add text and its embedding"""
        self.texts.append(text)
        self.embeddings.append(embedding)
        
    def find_similar(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """Find similar texts based on embedding"""
        if not self.embeddings:
            return []
        
        # Calculate similarities
        similarities = []
        for i, embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding))
            similarities.append((i, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results
        results = []
        for i, similarity in similarities[:top_k]:
            results.append({
                "text": self.texts[i],
                "similarity": float(similarity),
                "index": i
            })
        
        return results 