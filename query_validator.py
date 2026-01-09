from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class QueryValidator:
    def __init__(self):
        """Initialize the validator with Groq"""
        self.llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1
)
        
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="""You are a query validator. Determine if the following query is a valid web search query.

A VALID query is something that can be searched on Google/DuckDuckGo to find information (facts, places, how-to, news, etc.)
An INVALID query is a command, todo item, or action request (like "walk my pet", "add to grocery list", "remind me", etc.)

Query: {query}

Respond with ONLY one word: "VALID" or "INVALID"

Answer:"""
        )
    
    def is_valid(self, query: str) -> bool:
        """Check if query is valid for web search"""
        try:
            chain = self.prompt | self.llm
            response = chain.invoke({"query": query})
            
            # Extract text content
            result = response.content.strip().upper()
            
            # Parse response
            if "VALID" in result and "INVALID" not in result:
                return True
            return False
        except Exception as e:
            print(f"Validation error: {e}")
            # Default to valid if error to not block legitimate queries
            return True