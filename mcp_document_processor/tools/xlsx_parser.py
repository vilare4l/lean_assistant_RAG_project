from shared.schemas.mcp_payload import MCPPayload, SourceInfo, TabularData
import pandas as pd
import io
from typing import Any, Dict, List


def parse_xlsx_file(file_name: str, file_content: bytes) -> MCPPayload:
    """
    Parses an XLSX file and returns an MCPPayload.
    """
    source_info = SourceInfo(
        source_id=file_name,
        summary=f"Contenu extrait de {file_name}",
        total_word_count=0,
    )

    try:
        df = pd.read_excel(io.BytesIO(file_content))
    except Exception as e:
        raise ValueError(f"Could not read XLSX file: {e}")

    # Convertir les types de données non sérialisables en string
    for col in df.columns:
        if df[col].dtype.kind not in "biufc":  # bool, int, uint, float, complex
            df[col] = df[col].astype(str)

    df.columns = [str(c) for c in df.columns]

    rows: List[Dict[str, Any]] = [
        {str(k): v for k, v in row.items()} for row in df.to_dict(orient="records")
    ]

    tabular_data = [TabularData(table_name=file_name, rows=rows)]

    return MCPPayload(
        source_info=source_info, content_chunks=[], tabular_data=tabular_data
    )
