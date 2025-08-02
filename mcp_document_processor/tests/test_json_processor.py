import pytest
import base64
import json
from unittest.mock import patch, MagicMock

from mcp_document_processor.src.main import process_json

# Dummy content
dummy_json_content = b'{"key": "value", "number": 123}'
dummy_json_base64 = base64.b64encode(dummy_json_content).decode("utf-8")


# Mock Context class
class MockContext:
    def __init__(self):
        self.request_context = MagicMock()


# Mock the actual parsing function where it's used in main.py
@patch("mcp_document_processor.src.main.parse_json_file")
@pytest.mark.asyncio
async def test_process_json_success(mock_parse_json_file):
    mock_parse_json_file.return_value.model_dump_json.return_value = json.dumps(
        {
            "source_info": {"source_id": "dummy.json"},
            "content_chunks": [{"content": "Mocked JSON content"}],
            "tabular_data": [],
        }
    )

    ctx = MockContext()
    response_json_str = await process_json(
        ctx, file_name="dummy.json", file_content_base64=dummy_json_base64
    )

    payload = json.loads(response_json_str)

    mock_parse_json_file.assert_called_once_with("dummy.json", dummy_json_content)
    assert payload["source_info"]["source_id"] == "dummy.json"
    assert payload["content_chunks"][0]["content"] == "Mocked JSON content"


@patch("mcp_document_processor.src.main.parse_json_file")
@pytest.mark.asyncio
async def test_process_json_error(mock_parse_json_file):
    mock_parse_json_file.side_effect = Exception("JSON parsing failed")

    ctx = MockContext()
    response_json_str = await process_json(
        ctx, file_name="dummy.json", file_content_base64=dummy_json_base64
    )

    assert "Error processing JSON: JSON parsing failed" in response_json_str
    mock_parse_json_file.assert_called_once_with("dummy.json", dummy_json_content)
