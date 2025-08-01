# core/mcp-servers/web-crawler/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.shared.schemas.mcp_payload import MCPPayload


from . import processor

app = FastAPI(
    title="MCP Server - Web Crawler",
    description="Un serveur MCP pour crawler des pages web et les transformer en MCPPayload.",
    version="1.0.0"
)

class CrawlURLRequest(BaseModel):
    url: str

@app.post("/process-url/", response_model=MCPPayload)
async def process_url_endpoint(request: CrawlURLRequest):
    """
    Endpoint principal pour crawler une URL et la transformer en MCPPayload.
    """
    try:
        payload = await processor.process_url(url=request.url)
        return payload
    except Exception as e:
        # En cas d'erreur durant le crawling, retourner une erreur HTTP claire
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", status_code=200)
async def health_check():
    """Vérifie que le service est en ligne."""
    return {"status": "ok"}
