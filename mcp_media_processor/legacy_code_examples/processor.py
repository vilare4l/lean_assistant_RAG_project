# core/mcp-servers/media-processor/processor.py

from .main import MCPPayload, SourceInfo, Chunk
from . import clients

async def process_media_file(file_name: str, file_content: bytes, mime_type: str) -> MCPPayload:
    """
    Orchestre le traitement d'un fichier média.
    """
    # 1. Uploader le média pour obtenir une URL stable
    # Pour le MVP, nous allons simuler cette étape et utiliser un placeholder.
    # Dans une vraie implémentation, une fonction comme `clients.s3_upload` serait appelée ici.
    asset_url = f"https://fake-storage.com/{file_name}"
    print(f"Média uploadé (simulation) sur : {asset_url}")
    
    source_info = SourceInfo(
        source_id=f"media_{file_name}",
        summary=f"Contenu extrait du fichier média {file_name} disponible à {asset_url}"
    )
    
    extracted_text = ""
    if "image" in mime_type:
        # 2a. Extraire le texte de l'image en appelant le client
        extracted_text = await clients.get_image_description(asset_url, file_content)
    elif "audio" in mime_type:
        # 2b. Extraire le texte de l'audio en appelant le client
        extracted_text = await clients.get_audio_transcription(asset_url, file_content)
    else:
        raise ValueError(f"Unsupported media type: {mime_type}")

    # 3. Créer le chunk de contenu
    content_chunk = Chunk(
        chunk_type='text',
        content=extracted_text,
        metadata={
            'file_name': file_name,
            'asset_url': asset_url,
            'media_type': mime_type
        }
    )
    
    source_info.total_word_count = len(extracted_text.split())

    # 4. Assembler le payload final
    return MCPPayload(
        source_info=source_info,
        content_chunks=[content_chunk],
        tabular_data=[]
    )