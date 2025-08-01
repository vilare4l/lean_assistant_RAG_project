# core/mcp-servers/document-processor/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from core.shared.schemas.mcp_payload import MCPPayload

from . import parser

app = FastAPI(
    title="MCP Server - Document Processor",
    description="Un serveur MCP pour traiter des fichiers (PDF, DOCX, CSV...) et les transformer en MCPPayload.",
    version="1.0.0"
)

@app.post("/process-document/", response_model=MCPPayload)
async def process_document_endpoint(file: UploadFile = File(...)):
    """
    Endpoint principal pour traiter un fichier uploadé.
    """
    try:
        file_content = await file.read()
        payload = parser.parse_file(
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
