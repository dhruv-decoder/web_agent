from storage import QueryStorage

# Initialize
storage = QueryStorage()

# Test 1: Store something
print("Storing query: 'Best pizza in NYC'")
storage.store_result(
    query="Best pizza in NYC",
    summary="Great pizza places include Joe's Pizza, Prince Street Pizza...",
    urls=["example.com/pizza1", "example.com/pizza2"]
)
print("✅ Stored!")
print()

# Test 2: Search for similar
print("Searching for: 'Top pizza places in New York'")
found, result = storage.search_similar("Top pizza places in New York")

if found:
    print(f"✅ Found similar! (Similarity: {result['similarity']:.2%})")
    print(f"Original: {result['query']}")
    print(f"Summary: {result['summary']}")
else:
    print("❌ Not found")