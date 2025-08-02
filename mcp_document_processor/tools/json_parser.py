from shared.schemas.mcp_payload import MCPPayload, SourceInfo, Chunk
import json


def parse_json_file(file_name: str, file_content: bytes) -> MCPPayload:
    """
    Parses a JSON file and returns an MCPPayload.
    """
    source_info = SourceInfo(
        source_id=file_name,
        summary=f"Contenu extrait de {file_name}",
        total_word_count=0,
    )

    try:
        data = json.loads(file_content.decode("utf-8"))
        extracted_text = json.dumps(data, indent=2)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")
    except Exception as e:
        raise ValueError(f"Could not read JSON file: {e}")

    # For JSON, we'll put the entire content as a single text chunk
    content_chunks = [
        Chunk(
            chunk_type="text",
            content=extracted_text,
            metadata={
                "file_name": file_name,
                "element_type": "json_document",
            },
        )
    ]

    source_info.total_word_count = len(extracted_text.split())

    return MCPPayload(
        source_info=source_info,
        content_chunks=content_chunks,
        tabular_data=[],
    )
