from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import os
import base64

from shared.schemas.mcp_payload import MCPPayload
from mcp_document_processor.tools.pdf_parser import parse_pdf_file
from mcp_document_processor.tools.docx_parser import parse_docx_file
from mcp_document_processor.tools.csv_parser import parse_csv_file
from mcp_document_processor.tools.xlsx_parser import parse_xlsx_file
from mcp_document_processor.tools.json_parser import parse_json_file

# Load environment variables from .env file
load_dotenv()


# Define a context for your MCP server
@dataclass
class DocumentProcessorContext:
    """Context for the Document Processor MCP server."""

    # Add any resources your MCP needs to initialize once at startup
    # For example: database_client: Any
    pass


@asynccontextmanager
async def mcp_lifespan(server: FastMCP) -> AsyncIterator[DocumentProcessorContext]:
    """
    Manages the lifecycle of resources for this MCP server.
    """
    # Example: Initialize a document storage client
    # document_storage_client = initialize_document_storage()

    try:
        yield DocumentProcessorContext()  # Pass initialized resources here if any
    finally:
        # Clean up resources here when the server shuts down
        # Example: await document_storage_client.close()
        pass


# Initialize FastMCP server
mcp = FastMCP(
    "mcp-document-processor",
    lifespan=mcp_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050"),
)


@mcp.tool()
async def process_pdf(ctx: Context, file_name: str, file_content_base64: str) -> str:
    """
    Processes a PDF file and returns its MCPPayload.

    Args:
        ctx: The MCP server provided context.
        file_name: The original name of the PDF file (e.g., "document.pdf").
        file_content_base64: The Base64 encoded content of the PDF file.
    """
    try:
        file_content_bytes = base64.b64decode(file_content_base64)
        payload: MCPPayload = parse_pdf_file(file_name, file_content_bytes)
        return payload.model_dump_json()
    except Exception as e:
        return f"Error processing PDF: {str(e)}"


@mcp.tool()
async def process_docx(ctx: Context, file_name: str, file_content_base64: str) -> str:
    """
    Processes a DOCX file and returns its MCPPayload.

    Args:
        ctx: The MCP server provided context.
        file_name: The original name of the DOCX file (e.g., "document.docx").
        file_content_base64: The Base64 encoded content of the DOCX file.
    """
    try:
        file_content_bytes = base64.b64decode(file_content_base64)
        payload: MCPPayload = parse_docx_file(file_name, file_content_bytes)
        return payload.model_dump_json()
    except Exception as e:
        return f"Error processing DOCX: {str(e)}"


@mcp.tool()
async def process_csv(ctx: Context, file_name: str, file_content_base64: str) -> str:
    """
    Processes a CSV file and returns its MCPPayload.

    Args:
        ctx: The MCP server provided context.
        file_name: The original name of the CSV file (e.g., "data.csv").
        file_content_base64: The Base64 encoded content of the CSV file.
    """
    try:
        file_content_bytes = base64.b64decode(file_content_base64)
        payload: MCPPayload = parse_csv_file(file_name, file_content_bytes)
        return payload.model_dump_json()
    except Exception as e:
        return f"Error processing CSV: {str(e)}"


@mcp.tool()
async def process_xlsx(ctx: Context, file_name: str, file_content_base64: str) -> str:
    """
    Processes an XLSX file and returns its MCPPayload.

    Args:
        ctx: The MCP server provided context.
        file_name: The original name of the XLSX file (e.g., "spreadsheet.xlsx").
        file_content_base64: The Base64 encoded content of the XLSX file.
    """
    try:
        file_content_bytes = base64.b64decode(file_content_base64)
        payload: MCPPayload = parse_xlsx_file(file_name, file_content_bytes)
        return payload.model_dump_json()
    except Exception as e:
        return f"Error processing XLSX: {str(e)}"


@mcp.tool()
async def process_json(ctx: Context, file_name: str, file_content_base64: str) -> str:
    """
    Processes a JSON file and returns its MCPPayload.

    Args:
        ctx: The MCP server provided context.
        file_name: The original name of the JSON file (e.g., "data.json").
        file_content_base64: The Base64 encoded content of the JSON file.
    """
    try:
        file_content_bytes = base64.b64decode(file_content_base64)
        payload: MCPPayload = parse_json_file(file_name, file_content_bytes)
        return payload.model_dump_json()
    except Exception as e:
        return f"Error processing JSON: {str(e)}"


# Main function to run the MCP server
async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == "sse":
        # Run the MCP server with SSE transport (HTTP endpoint)
        print(
            f"Starting MCP server with SSE on http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8050')}/sse"
        )
        await mcp.run_sse_async()
    else:
        # Run the MCP server with Stdio transport (CLI-based)
        print("Starting MCP server with Stdio transport.")
        await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
