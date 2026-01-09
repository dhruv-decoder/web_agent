from agent import WebQueryAgent
import sys

def main():
    """CLI interface for the agent"""
    print("=" * 60)
    print("🌐 WEB QUERY AGENT - CLI Interface")
    print("=" * 60)
    print()
    
    agent = WebQueryAgent()
    
    print("\nAgent ready! Enter your queries (type 'exit' to quit)")
    print("-" * 60)
    
    while True:
        print()
        query = input("Your query: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye! 👋")
            break
        
        if not query:
            continue
        
        # Process query
        result = agent.process_query(query)
        
        # Display results
        print("\n" + "=" * 60)
        print(f"STATUS: {result['status'].upper()}")
        print("=" * 60)
        
        if result['status'] == 'invalid':
            print(f"\n❌ {result['message']}")
        
        elif result['status'] == 'cached':
            print(f"\n✅ {result['message']}")
            print(f"\nOriginal Query: {result['original_query']}")
            print(f"Similarity: {result['similarity']:.2%}")
            print(f"\n📝 SUMMARY:\n{result['summary']}")
        
        elif result['status'] == 'success':
            print(f"\n✅ {result['message']}")
            print(f"\n📝 SUMMARY:\n{result['summary']}")
            print(f"\n🔗 SOURCES ({result['num_sources']}):")
            for i, url in enumerate(result['sources'], 1):
                print(f"  {i}. {url}")
        
        else:
            print(f"\n❌ {result['message']}")
        
        print("\n" + "-" * 60)

if __name__ == "__main__":
    main()