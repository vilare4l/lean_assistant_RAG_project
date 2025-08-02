import pytest
import base64
import json
from unittest.mock import patch, MagicMock

from mcp_document_processor.src.main import process_csv

# Dummy content
dummy_csv_content = b"header1,header2\nvalue1,value2\nvalue3,value4"
dummy_csv_base64 = base64.b64encode(dummy_csv_content).decode("utf-8")


# Mock Context class
class MockContext:
    def __init__(self):
        self.request_context = MagicMock()


# Mock the actual parsing function where it's used in main.py
@patch("mcp_document_processor.src.main.parse_csv_file")
@pytest.mark.asyncio
async def test_process_csv_success(mock_parse_csv_file):
    mock_parse_csv_file.return_value.model_dump_json.return_value = json.dumps(
        {
            "source_info": {"source_id": "dummy.csv"},
            "content_chunks": [],
            "tabular_data": [{"rows": [{"header1": "value1"}]}],
        }
    )

    ctx = MockContext()
    response_json_str = await process_csv(
        ctx, file_name="dummy.csv", file_content_base64=dummy_csv_base64
    )

    payload = json.loads(response_json_str)

    mock_parse_csv_file.assert_called_once_with("dummy.csv", dummy_csv_content)
    assert payload["source_info"]["source_id"] == "dummy.csv"
    assert len(payload["tabular_data"]) > 0


@patch("mcp_document_processor.src.main.parse_csv_file")
@pytest.mark.asyncio
async def test_process_csv_error(mock_parse_csv_file):
    mock_parse_csv_file.side_effect = Exception("CSV parsing failed")

    ctx = MockContext()
    response_json_str = await process_csv(
        ctx, file_name="dummy.csv", file_content_base64=dummy_csv_base64
    )

    assert "Error processing CSV: CSV parsing failed" in response_json_str
    mock_parse_csv_file.assert_called_once_with("dummy.csv", dummy_csv_content)
