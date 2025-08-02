import pytest
import base64
import json
from unittest.mock import patch, MagicMock

from mcp_document_processor.src.main import process_xlsx

# Dummy content
dummy_xlsx_content = b"dummy xlsx content"
dummy_xlsx_base64 = base64.b64encode(dummy_xlsx_content).decode("utf-8")


# Mock Context class
class MockContext:
    def __init__(self):
        self.request_context = MagicMock()


# Mock the actual parsing function where it's used in main.py
@patch("mcp_document_processor.src.main.parse_xlsx_file")
@pytest.mark.asyncio
async def test_process_xlsx_success(mock_parse_xlsx_file):
    mock_parse_xlsx_file.return_value.model_dump_json.return_value = json.dumps(
        {
            "source_info": {"source_id": "dummy.xlsx"},
            "content_chunks": [],
            "tabular_data": [{"rows": [{"Col1": "Val1"}]}],
        }
    )

    ctx = MockContext()
    response_json_str = await process_xlsx(
        ctx, file_name="dummy.xlsx", file_content_base64=dummy_xlsx_base64
    )

    payload = json.loads(response_json_str)

    mock_parse_xlsx_file.assert_called_once_with("dummy.xlsx", dummy_xlsx_content)
    assert payload["source_info"]["source_id"] == "dummy.xlsx"
    assert len(payload["tabular_data"]) > 0


@patch("mcp_document_processor.src.main.parse_xlsx_file")
@pytest.mark.asyncio
async def test_process_xlsx_error(mock_parse_xlsx_file):
    mock_parse_xlsx_file.side_effect = Exception("XLSX parsing failed")

    ctx = MockContext()
    response_json_str = await process_xlsx(
        ctx, file_name="dummy.xlsx", file_content_base64=dummy_xlsx_base64
    )

    assert "Error processing XLSX: XLSX parsing failed" in response_json_str
    mock_parse_xlsx_file.assert_called_once_with("dummy.xlsx", dummy_xlsx_content)
