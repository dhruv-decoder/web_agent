from query_validator import QueryValidator
from storage import QueryStorage
from scraper import WebScraper
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class WebQueryAgent:
    def __init__(self):
        """Initialize all components"""
        print("Initializing Web Query Agent...")
        
        self.validator = QueryValidator()
        self.storage = QueryStorage()
        self.scraper = WebScraper()
        
        # LLM for summarization using Gemini
        self.llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1
)
        
        
        self.summarize_prompt = PromptTemplate(
            input_variables=["content", "query"],
            template="""Based on the following web content, provide a comprehensive summary that answers the query: "{query}"

Web Content:
{content}

Summary (be concise but informative, 3-5 sentences):"""
        )
        
        print("Agent initialized successfully!")
    
    def process_query(self, query: str):
        """Main agent workflow"""
        
        # Step 1: Validate query
        print(f"\n🔍 Processing query: '{query}'")
        print("Step 1: Validating query...")
        
        if not self.validator.is_valid(query):
            return {
                "status": "invalid",
                "message": "This is not a valid web search query. Please ask something that can be searched online.",
                "query": query
            }
        
        print("✅ Query is valid")
        
        # Step 2: Check for similar past queries
        print("Step 2: Checking for similar past queries...")
        
        found, cached_result = self.storage.search_similar(query)
        
        if found:
            print(f"✅ Found similar query from cache (similarity: {cached_result['similarity']:.2%})")
            return {
                "status": "cached",
                "message": "Found similar query from past results",
                "query": query,
                "original_query": cached_result["query"],
                "summary": cached_result["summary"],
                "timestamp": cached_result["timestamp"],
                "similarity": cached_result["similarity"]
            }
        
        print("No similar queries found, proceeding with web search...")
        
        # Step 3: Scrape web
        print("Step 3: Scraping web results...")
        
        scraped_data = self.scraper.search_and_scrape(query, num_results=5)
        
        if not scraped_data:
            return {
                "status": "error",
                "message": "Failed to scrape any results",
                "query": query
            }
        
        print(f"✅ Scraped {len(scraped_data)} pages")
        
        # Step 4: Summarize
        print("Step 4: Generating summary...")
        
        # Combine all scraped content
        combined_content = "\n\n".join([
            f"Source {i+1} ({data['url']}):\n{data['content']}" 
            for i, data in enumerate(scraped_data)
        ])
        
        # Generate summary
        chain = self.summarize_prompt | self.llm
        response = chain.invoke({
            "query": query,
            "content": combined_content[:8000]  # Limit to avoid token limits
        })
        summary = response.content.strip()
        
        print("✅ Summary generated")
        
        # Step 5: Store results
        print("Step 5: Storing results for future queries...")
        
        urls = [data["url"] for data in scraped_data]
        self.storage.store_result(query, summary, urls)
        
        print("✅ Results stored")
        
        return {
            "status": "success",
            "message": "Successfully processed query",
            "query": query,
            "summary": summary,
            "sources": urls,
            "num_sources": len(scraped_data)
        }