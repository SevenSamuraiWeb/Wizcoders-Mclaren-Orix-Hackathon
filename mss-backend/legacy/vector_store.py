import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class PageVectorStore:
    """
    Manages embedding generation and vector search for PDF pages.
    """
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the sentence transformer model and FAISS index.
        """
        self.model = SentenceTransformer(model_name)
        # 384 dimensions for all-MiniLM-L6-v2
        self.dimension = 384 
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = [] # List to store {page, text} corresponding to index IDs

    def add_pages(self, pages: list):
        """
        Generates embeddings for pages and adds them to the FAISS index.
        
        Args:
            pages (list): List of dicts [{'page': n, 'text': '...'}, ...]
        """
        if not pages:
            return

        texts = [p['text'] for p in pages]
        
        # Generate embeddings
        embeddings = self.model.encode(texts)
        
        # Convert to float32 for FAISS
        embeddings_np = np.array(embeddings).astype('float32')
        
        # Add to index
        self.index.add(embeddings_np)
        
        # Store metadata
        self.metadata.extend(pages)

    def search(self, query: str, top_k: int = 3):
        """
        Searches the vector store for the most relevant pages.
        
        Args:
            query (str): The search query.
            top_k (int): Number of results to return.
            
        Returns:
            list: List of dicts [{'page': n, 'text': '...'}, ...]
        """
        # Generate query embedding
        query_embedding = self.model.encode([query])
        query_embedding_np = np.array(query_embedding).astype('float32')
        
        # Search index
        # D is distances, I is indices
        D, I = self.index.search(query_embedding_np, top_k)
        
        results = []
        for idx in I[0]:
            if idx != -1 and idx < len(self.metadata):
                results.append(self.metadata[idx])
                
        return results
