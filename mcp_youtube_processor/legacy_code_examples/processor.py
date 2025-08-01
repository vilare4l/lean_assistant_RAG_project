# core/mcp-servers/youtube-processor/processor.py

from .main import MCPPayload, SourceInfo, Chunk
from youtube_transcript_api import YouTubeTranscriptApi
import re

def _get_video_id(url: str) -> str | None:
    """Extrait l'ID de la vidéo d'une URL YouTube."""
    regex = r"(?:v=|\/|embed\/|watch\?v=|\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

def process_youtube_url(url: str) -> MCPPayload:
    """
    Récupère et traite la transcription d'une vidéo YouTube.
    """
    video_id = _get_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise RuntimeError(f"Could not retrieve transcript for video {video_id}: {e}")

    source_info = SourceInfo(
        source_id=f"youtube_{video_id}",
        summary=f"Transcription de la vidéo YouTube {url}"
    )

    content_chunks: list[Chunk] = []
    
    # Logique de chunking: regrouper les segments par 10
    chunk_size = 10 
    for i in range(0, len(transcript_list), chunk_size):
        chunk_segments = transcript_list[i:i + chunk_size]
        
        text = " ".join([segment['text'] for segment in chunk_segments])
        start_time = chunk_segments[0]['start']
        end_time = chunk_segments[-1]['start'] + chunk_segments[-1]['duration']
        
        content_chunks.append(
            Chunk(
                chunk_type='text',
                content=text,
                metadata={
                    'video_id': video_id,
                    'url': url,
                    'start_time_seconds': start_time,
                    'end_time_seconds': end_time
                }
            )
        )
        
    source_info.total_word_count = sum(len(c.content.split()) for c in content_chunks)

    return MCPPayload(
        source_info=source_info,
        content_chunks=content_chunks,
        tabular_data=[]
    )
