# core/mcp-servers/query-handler/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from . import processor

app = FastAPI(title="MCP Server - Query Handler")

class QueryRequest(BaseModel):
    query: str
    source_id: str | None = None
    chunk_type: str = "text"

class QueryResponse(BaseModel):
    answer: str
    context: list[dict]

@app.post("/query/", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Endpoint principal pour interroger la plateforme.
    """
    answer, context = await processor.process_query(request)
    return QueryResponse(answer=answer, context=context)

@app.get("/health", status_code=200)
async def health_check():
    """Vérifie que le service est en ligne."""
    return {"status": "ok"}