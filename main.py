from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import WebQueryAgent
import uvicorn

app = FastAPI(title="Web Query Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = WebQueryAgent()

# Request model
class QueryRequest(BaseModel):
    query: str

# Response models
class QueryResponse(BaseModel):
    status: str
    message: str
    query: str
    summary: str = None
    sources: list = None
    similarity: float = None

@app.get("/")
def root():
    return {"message": "Web Query Agent API", "status": "running"}

@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    """Process a web query"""
    try:
        result = agent.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)