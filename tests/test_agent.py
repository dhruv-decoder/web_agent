from agent import WebQueryAgent

# Initialize
agent = WebQueryAgent()

# Test 1: Invalid query
print("=" * 60)
print("TEST 1: Invalid Query")
print("=" * 60)
result = agent.process_query("walk my pet")
print(f"Status: {result['status']}")
print(f"Message: {result['message']}")
print()

# Test 2: Valid new query
print("=" * 60)
print("TEST 2: Valid New Query")
print("=" * 60)
result = agent.process_query("Best places to visit in Delhi")
print(f"Status: {result['status']}")
if result['status'] == 'success':
    print(f"Summary: {result['summary'][:200]}...")
    print(f"Sources: {len(result['sources'])} URLs")
elif result['status'] == 'cached':
    print(f"Similarity: {result['similarity']:.2%}")
    print(f"Summary: {result['summary'][:200]}...")
print()

# Test 3: Similar query (should use cache now!)
print("=" * 60)
print("TEST 3: Similar Query (Cache Test)")
print("=" * 60)
result = agent.process_query("Top tourist attractions in Delhi")
print(f"Status: {result['status']}")

# ✅ FIXED: Handle both cached and new results
if result['status'] == 'cached':
    print(f"✅ CACHE HIT!")
    print(f"Original Query: {result['original_query']}")
    print(f"Similarity: {result['similarity']:.2%}")
    print(f"Summary: {result['summary'][:200]}...")
elif result['status'] == 'success':
    print(f"⚠️ CACHE MISS (scraped new results)")
    print(f"Summary: {result['summary'][:200]}...")
    print(f"Sources: {len(result['sources'])} URLs")
print()

# Test 4: Repeat exact same query (should definitely cache)
print("=" * 60)
print("TEST 4: Exact Repeat Query")
print("=" * 60)
result = agent.process_query("Best places to visit in Delhi")
print(f"Status: {result['status']}")
if result['status'] == 'cached':
    print(f"✅ CACHE HIT!")
    print(f"Similarity: {result['similarity']:.2%}")
else:
    print(f"⚠️ Unexpected: Should have been cached")