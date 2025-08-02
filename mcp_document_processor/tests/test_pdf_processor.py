import pytest
import base64
import json
from unittest.mock import patch, MagicMock

# Import the MCP tool functions directly
from mcp_document_processor.src.main import process_pdf

# Dummy content
dummy_pdf_content = b"dummy pdf content"
dummy_pdf_base64 = base64.b64encode(dummy_pdf_content).decode("utf-8")


# Mock Context class
class MockContext:
    def __init__(self):
        self.request_context = MagicMock()


# Mock the actual parsing function where it's used in main.py
@patch("mcp_document_processor.src.main.parse_pdf_file")
@pytest.mark.asyncio
async def test_process_pdf_success(mock_parse_pdf_file):
    # Configure mock to return a dummy MCPPayload
    mock_parse_pdf_file.return_value.model_dump_json.return_value = json.dumps(
        {
            "source_info": {"source_id": "dummy.pdf"},
            "content_chunks": [{"content": "Mocked PDF content"}],
            "tabular_data": [],
        }
    )

    ctx = MockContext()
    response_json_str = await process_pdf(
        ctx, file_name="dummy.pdf", file_content_base64=dummy_pdf_base64
    )

    payload = json.loads(response_json_str)

    mock_parse_pdf_file.assert_called_once_with("dummy.pdf", dummy_pdf_content)
    assert payload["source_info"]["source_id"] == "dummy.pdf"
    assert payload["content_chunks"][0]["content"] == "Mocked PDF content"


@patch("mcp_document_processor.src.main.parse_pdf_file")
@pytest.mark.asyncio
async def test_process_pdf_error(mock_parse_pdf_file):
    mock_parse_pdf_file.side_effect = Exception("PDF parsing failed")

    ctx = MockContext()
    response_json_str = await process_pdf(
        ctx, file_name="dummy.pdf", file_content_base64=dummy_pdf_base64
    )

    assert "Error processing PDF: PDF parsing failed" in response_json_str
    mock_parse_pdf_file.assert_called_once_with("dummy.pdf", dummy_pdf_content)
