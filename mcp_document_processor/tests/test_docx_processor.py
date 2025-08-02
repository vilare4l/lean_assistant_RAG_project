import pytest
import base64
import json
from unittest.mock import patch, MagicMock

from mcp_document_processor.src.main import process_docx

# Dummy content
dummy_docx_content = b"dummy docx content"
dummy_docx_base64 = base64.b64encode(dummy_docx_content).decode("utf-8")


# Mock Context class
class MockContext:
    def __init__(self):
        self.request_context = MagicMock()


# Mock the actual parsing function where it's used in main.py
@patch("mcp_document_processor.src.main.parse_docx_file")
@pytest.mark.asyncio
async def test_process_docx_success(mock_parse_docx_file):
    mock_parse_docx_file.return_value.model_dump_json.return_value = json.dumps(
        {
            "source_info": {"source_id": "dummy.docx"},
            "content_chunks": [{"content": "Mocked DOCX content"}],
            "tabular_data": [],
        }
    )

    ctx = MockContext()
    response_json_str = await process_docx(
        ctx, file_name="dummy.docx", file_content_base64=dummy_docx_base64
    )

    payload = json.loads(response_json_str)

    mock_parse_docx_file.assert_called_once_with("dummy.docx", dummy_docx_content)
    assert payload["source_info"]["source_id"] == "dummy.docx"
    assert payload["content_chunks"][0]["content"] == "Mocked DOCX content"


@patch("mcp_document_processor.src.main.parse_docx_file")
@pytest.mark.asyncio
async def test_process_docx_error(mock_parse_docx_file):
    mock_parse_docx_file.side_effect = Exception("DOCX parsing failed")

    ctx = MockContext()
    response_json_str = await process_docx(
        ctx, file_name="dummy.docx", file_content_base64=dummy_docx_base64
    )

    assert "Error processing DOCX: DOCX parsing failed" in response_json_str
    mock_parse_docx_file.assert_called_once_with("dummy.docx", dummy_docx_content)
