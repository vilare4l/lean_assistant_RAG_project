# core/mcp-servers/youtube-processor/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.shared.schemas.mcp_payload import MCPPayload

from . import processor

app = FastAPI(
    title="MCP Server - YouTube Processor",
    description="Un serveur MCP pour traiter des URLs YouTube et les transformer en MCPPayload.",
    version="1.0.0"
)

class YouTubeRequest(BaseModel):
    url: str

@app.post("/process-youtube/", response_model=MCPPayload)
async def process_youtube_endpoint(request: YouTubeRequest):
    """
    Endpoint principal pour traiter une URL YouTube.
    """
    try:
        payload = processor.process_youtube_url(url=request.url)
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", status_code=200)
async def health_check():
    """Vérifie que le service est en ligne."""
    return {"status": "ok"}
