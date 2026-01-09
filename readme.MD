# 🔍 Web Query Agent

An intelligent web search agent that validates queries, caches results, and provides AI-generated summaries from web content.

## Features

- **Query Validation**: Uses LLM to filter out non-searchable queries
- **Semantic Caching**: ChromaDB vector storage finds similar past queries (50% similarity threshold)
- **Web Scraping**: Playwright-based scraper fetches top 5 search results
- **AI Summarization**: Groq api(llama-3.1-8b-instant)generates concise answers
- **Persistent Storage**: Results saved for future similarity matching

## Architecture

```
User Query → Validator → Cache Check → [Cache Hit: Return] 
                                    ↓
                              [Cache Miss]
                                    ↓
                         Web Scraper (DuckDuckGo + Playwright)
                                    ↓
                            AI Summarization (llama-3.1-8b-instant)
                                    ↓
                          Store in Vector DB (ChromaDB)
```

## Installation

```bash
# Clone repository
git clone <your-repo-url>
cd web-query-agent

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Set up environment
cp .env.example .env
# Add your groq api key to .env
```

## Usage

### Streamlit UI
```bash
streamlit run app.py
```

### CLI
```bash
python cli.py
```

### FastAPI
```bash
python main.py
# API available at http://localhost:8000
```

## Tech Stack

- **LLM**: llama-3.1-8b-instant
- **Framework**: LangChain
- **Vector DB**: ChromaDB with HuggingFace embeddings
- **Web Scraping**: Playwright + DuckDuckGo Search
- **Interfaces**: Streamlit, CLI, FastAPI

## Project Structure

```
├── agent.py            # Main orchestration logic
├── query_validator.py  # LLM-based query validation
├── storage.py          # ChromaDB vector storage
├── scraper.py          # Web scraping with Playwright
├── app.py              # Streamlit interface
├── cli.py              # Command-line interface
├── main.py             # FastAPI backend
└── requirements.txt
```

## Key Design Decisions

1. **ChromaDB**: Lightweight, no separate database server required
2. **HuggingFace Embeddings**: Free, runs locally (all-MiniLM-L6-v2)
3. **Playwright**: Reliable web scraping with JavaScript rendering support
4. **LangChain**: Structured prompt management and LLM integration framework standardizing agentic applications with easy to switch syntaxes for all parts 
5. **50% Similarity Threshold**: Balances cache hits vs. fresh results (This was chosen after testing with 75% 70% 40% and 50% threshold)
6. **Groq api as llm**: provides instant responses known for it's inference speed + generous and reliable free tier 

## Environment Variables

```env
GROQ_API_KEY=your_api_key_here
```


