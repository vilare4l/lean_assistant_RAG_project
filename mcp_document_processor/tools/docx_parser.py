from shared.schemas.mcp_payload import MCPPayload, SourceInfo, Chunk, TabularData
from unstructured.partition.auto import partition
import pandas as pd
import io
from typing import Any, Dict, List


def parse_docx_file(file_name: str, file_content: bytes) -> MCPPayload:
    """
    Parses a DOCX file and returns an MCPPayload.
    """
    source_info = SourceInfo(
        source_id=file_name,
        summary=f"Contenu extrait de {file_name}",
        total_word_count=0,
    )

    elements = partition(
        file=io.BytesIO(file_content), file_filename=file_name, strategy="hi_res"
    )

    content_chunks: list[Chunk] = []
    tabular_data: list[TabularData] = []

    for element in elements:
        print(f"Detected element type: {type(element).__name__}")
        if type(element).__name__ == "Table":
            print(
                f"Attempting to parse table. HTML content: {element.metadata.text_as_html}"
            )
            if element.metadata.text_as_html:
                try:
                    html_table = element.metadata.text_as_html
                    df = pd.read_html(io.StringIO(html_table), header=0)[0]
                    df.columns = [str(c) for c in df.columns]

                    table_rows: List[Dict[str, Any]] = [
                        {str(k): v for k, v in row.items()}
                        for row in df.to_dict(orient="records")
                    ]

                    if table_rows:
                        tabular_data.append(
                            TabularData(
                                table_name=f"{file_name}_table_{len(tabular_data) + 1}",
                                rows=table_rows,
                            )
                        )
                except Exception as e:
                    print(f"Could not parse table from unstructured element: {e}")
            else:
                print(
                    f"Warning: Table element found but no HTML content available. Adding as text chunk. Element text: {element.text}"
                )
                content_chunks.append(
                    Chunk(
                        chunk_type="text",
                        content=str(element.text),
                        metadata={
                            "file_name": file_name,
                            "element_type": type(element).__name__,
                            "warning": "No HTML content for table, added as text.",
                        },
                    )
                )
        else:
            content_chunks.append(
                Chunk(
                    chunk_type="text",
                    content=str(element),
                    metadata={
                        "file_name": file_name,
                        "element_type": type(element).__name__,
                    },
                )
            )

    source_info.total_word_count = sum(len(c.content.split()) for c in content_chunks)

    return MCPPayload(
        source_info=source_info,
        content_chunks=content_chunks,
        tabular_data=tabular_data,
    )
