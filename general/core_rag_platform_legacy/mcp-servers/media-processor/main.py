# core/mcp-servers/media-processor/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from core.shared.schemas.mcp_payload import MCPPayload

from . import processor

app = FastAPI(
    title="MCP Server - Media Processor",
    description="Un serveur MCP pour traiter des fichiers média (images, audio) et les transformer en MCPPayload.",
    version="1.0.0"
)

@app.post("/process-media/", response_model=MCPPayload)
async def process_media_endpoint(file: UploadFile = File(...)):
    """
    Endpoint principal pour traiter un fichier média uploadé.
    """
    try:
        file_content = await file.read()
        payload = await processor.process_media_file(
            file_name=file.filename,
            file_content=file_content,
            mime_type=file.content_type
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", status_code=200)
async def health_check():
    """Vérifie que le service est en ligne."""
    return {"status": "ok"}
