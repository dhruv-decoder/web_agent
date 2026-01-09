from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import chromadb
from chromadb.config import Settings
import os

class QueryStorage:
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB with HuggingFace embeddings"""
        self.persist_directory = persist_directory
        
        # Use free HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize or get collection
        try:
            self.collection = self.client.get_collection("query_results")
        except:
            self.collection = self.client.create_collection(
                name="query_results",
                metadata={"hnsw:space": "cosine"}
            )
        
        # Initialize Langchain vector store
        self.vectorstore = Chroma(
            client=self.client,
            collection_name="query_results",
            embedding_function=self.embeddings
        )
    
    def search_similar(self, query: str, threshold: float = 0.50):  # ✅ CHANGED to 50%
        """Search for similar queries. Returns (is_found, results)"""
        try:
            # Search for similar documents
            results = self.vectorstore.similarity_search_with_score(
                query, 
                k=1
            )
            
            if not results:
                return False, None
            
            doc, score = results[0]
            
            # ChromaDB returns distance (lower is better)
            # Convert to similarity: similarity = 1 - distance
            similarity = 1 - score
            
            print(f"Similarity score: {similarity:.3f}")
            
            if similarity >= threshold:
                return True, {
                    "query": doc.metadata.get("query"),
                    "summary": doc.page_content,
                    "timestamp": doc.metadata.get("timestamp"),
                    "similarity": similarity
                }
            
            return False, None
        
        except Exception as e:
            print(f"Search error: {e}")
            return False, None
    
    def store_result(self, query: str, summary: str, urls: list):
        """Store query results for future retrieval"""
        try:
            from datetime import datetime
            
            doc = Document(
                page_content=summary,
                metadata={
                    "query": query,
                    "urls": str(urls),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            self.vectorstore.add_documents([doc])
            print(f"Stored results for query: {query}")
            return True
        
        except Exception as e:
            print(f"Storage error: {e}")
            return False