# core/mcp-servers/neo4j-processor/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.shared.schemas.mcp_payload import MCPPayload

from . import parser

app = FastAPI(
    title="MCP Server - Neo4j Processor",
    description="Un serveur MCP pour analyser des dépôts de code et peupler un graphe de connaissances Neo4j.",
    version="1.0.0"
)

class RepoRequest(BaseModel):
    url: str

@app.post("/process-repository/", response_model=MCPPayload)
async def process_repository_endpoint(request: RepoRequest):
    """
    Endpoint principal pour analyser un dépôt et peupler Neo4j.
    """
    try:
        payload = await parser.parse_repository(repo_url=request.url)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", status_code=200)
async def health_check():
    """Vérifie que le service est en ligne."""
    return {"status": "ok"}
