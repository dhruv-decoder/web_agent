from scraper import WebScraper

# Initialize
scraper = WebScraper()  # ✅ CHANGED THIS LINE

# Test scraping
print("Scraping: 'Python programming'")
results = scraper.search_and_scrape("Python programming", num_results=3)

print(f"\n✅ Scraped {len(results)} pages:")
for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['url']}")
    print(f"   Content preview: {result['content'][:100]}...")