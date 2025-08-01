# core/mcp-servers/document-processor/parser.py

from .main import MCPPayload, SourceInfo, Chunk, TabularData
from unstructured.partition.auto import partition
import pandas as pd
import io

def parse_file(file_name: str, file_content: bytes, mime_type: str) -> MCPPayload:
    """
    Route le fichier vers le bon parser en fonction de son type MIME.
    """
    source_info = SourceInfo(source_id=file_name, summary=f"Contenu extrait de {file_name}")

    if mime_type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return _parse_unstructured_document(source_info, file_name, file_content)
    elif mime_type == "text/csv":
        return _parse_tabular_document(source_info, file_name, file_content, "csv")
    elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return _parse_tabular_document(source_info, file_name, file_content, "excel")
    else:
        raise ValueError(f"Unsupported MIME type: {mime_type}")

def _parse_unstructured_document(source_info: SourceInfo, file_name: str, file_content: bytes) -> MCPPayload:
    """Parse les documents comme les PDF et DOCX avec unstructured."""
    
    elements = partition(file=io.BytesIO(file_content), file_filename=file_name)
    
    content_chunks: list[Chunk] = []
    tabular_data: list[TabularData] = []
    
    for element in elements:
        if type(element).__name__ == 'Table':
            try:
                # Unstructured peut fournir le tableau en HTML, pandas peut le lire
                html_table = element.metadata.text_as_html
                df = pd.read_html(io.StringIO(html_table), header=0)[0]
                table_rows = df.to_dict(orient='records')
                
                if table_rows:
                    tabular_data.append(
                        TabularData(
                            table_name=f"{file_name}_table_{len(tabular_data) + 1}",
                            rows=table_rows
                        )
                    )
            except Exception as e:
                print(f"Could not parse table from unstructured element: {e}")
        else:
            content_chunks.append(
                Chunk(
                    chunk_type='text',
                    content=str(element),
                    metadata={'file_name': file_name, 'element_type': type(element).__name__}
                )
            )
            
    source_info.total_word_count = sum(len(c.content.split()) for c in content_chunks)
    
    return MCPPayload(
        source_info=source_info,
        content_chunks=content_chunks,
        tabular_data=tabular_data
    )

def _parse_tabular_document(source_info: SourceInfo, file_name: str, file_content: bytes, file_type: str) -> MCPPayload:
    """Parse les fichiers CSV et Excel avec pandas."""
    
    try:
        if file_type == 'csv':
            df = pd.read_csv(io.BytesIO(file_content))
        else:  # excel
            df = pd.read_excel(io.BytesIO(file_content))
    except Exception as e:
        raise ValueError(f"Could not read {file_type} file: {e}")
        
    # Convertir les types de données non sérialisables en string
    for col in df.columns:
        if df[col].dtype.kind not in 'biufc': # bool, int, uint, float, complex
            df[col] = df[col].astype(str)

    rows = df.to_dict(orient='records')
    
    tabular_data = [TabularData(table_name=file_name, rows=rows)]
    
    return MCPPayload(
        source_info=source_info,
        content_chunks=[],
        tabular_data=tabular_data
    )