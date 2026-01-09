from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from ddgs import DDGS  
import time

class WebScraper:
    def __init__(self):
        """Initialize scraper"""
        self.ddgs = DDGS()
    
    def search_and_scrape(self, query: str, num_results: int = 5):
        """Search query and scrape top N results"""
        print(f"Searching for: {query}")
        
        # Step 1: Get URLs from DuckDuckGo
        urls = self._get_search_urls(query, num_results)
        
        if not urls:
            print("No search results found")
            return []
        
        print(f"Found {len(urls)} URLs")
        
        # Step 2: Scrape content from each URL
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            scraped_data = []
            for i, url in enumerate(urls):
                print(f"Scraping {i+1}/{len(urls)}: {url}")
                content = self._scrape_page(page, url)
                if content:
                    scraped_data.append({
                        "url": url,
                        "content": content
                    })
                time.sleep(1)  
            
            browser.close()
        
        return scraped_data
    
    def _get_search_urls(self, query: str, num_results: int):
        """Get search result URLs using DuckDuckGo library"""
        try:
            results = self.ddgs.text(query, max_results=num_results)
            urls = [result['href'] for result in results if 'href' in result]
            return urls
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _scrape_page(self, page, url: str):
        """Scrape content from a single page"""
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            time.sleep(1)
            
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            lines = (line.strip() for line in text.splitlines())
            text = ' '.join(line for line in lines if line)
            
            return text[:3000]
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None