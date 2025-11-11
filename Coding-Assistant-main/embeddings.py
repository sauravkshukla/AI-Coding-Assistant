import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class SemanticSearch:
    def __init__(self):
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.texts = []
        self.metadata = []
    
    def build_index(self, conversations: List[Tuple]):
        """Build FAISS index from conversation history"""
        if not conversations:
            return
        
        self.texts = []
        self.metadata = []
        
        for conv in conversations:
            # conv: (id, timestamp, user_query, ai_response, code_snippet, language)
            text = f"{conv[2]} {conv[3]}"  # Combine query and response
            if conv[4]:  # Add code snippet if exists
                text += f" {conv[4]}"
            self.texts.append(text)
            self.metadata.append(conv)
        
        # Generate embeddings
        vectors = self.embeddings.encode(self.texts)
        vectors_array = np.array(vectors).astype('float32')
        
        # Create FAISS index
        dimension = vectors_array.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(vectors_array)
    
    def search(self, query: str, k: int = 3) -> List[Tuple]:
        """Search for similar conversations"""
        if not self.index or self.index.ntotal == 0:
            return []
        
        query_vector = self.embeddings.encode([query])
        query_array = np.array(query_vector).astype('float32')
        
        distances, indices = self.index.search(query_array, min(k, self.index.ntotal))
        
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        
        return results
